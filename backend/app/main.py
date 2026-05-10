import hashlib
import hmac as _hmac
import json
import os
import random
import time
from datetime import datetime, timezone, timedelta
from urllib.parse import parse_qsl

import requests as _req
from openai import OpenAI
from fastapi import Body, Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Optional

from . import models, schemas
from .bot import start_polling
from .seed_data import READING_TESTS
from .database import Base, SessionLocal, engine, get_db
from .seed_ielts import seed as seed_ielts_content
from .security import create_access_token, decode_access_token, hash_password, verify_password

app = FastAPI(title="IELTS Mock Test API", version="0.1.0")
security = HTTPBearer()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://atashasd.vercel.app",
    "https://atashasd-git-main-jaqqon9-6154s-projects.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# ── Telegram config ───────────────────────────────────────────────────────────
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
FRONTEND_URL: str = os.getenv("FRONTEND_URL", "https://atashasd.vercel.app")


def _migrate_add_role_column(db: Session) -> None:
    """Add role column to existing users table if it doesn't exist yet."""
    try:
        db.execute(text("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'student'"))
        db.commit()
    except Exception:
        db.rollback()


def _generate_pin_raw(db: Session) -> str:
    """Generate a unique 6-digit PIN using raw SQL.
    Used during startup migration — ORM queries cannot be used there because
    not all model columns may exist in the DB yet.
    """
    while True:
        pin = str(random.randint(100000, 999999))
        count = db.execute(
            text("SELECT COUNT(*) FROM teacher_tests WHERE pin_code = :pin"),
            {"pin": pin}
        ).scalar()
        if not count:
            return pin


def _generate_pin(db: Session) -> str:
    """Generate a unique 6-digit PIN using ORM (used in request handlers only)."""
    while True:
        pin = str(random.randint(100000, 999999))
        exists = db.query(models.TeacherTest).filter(models.TeacherTest.pin_code == pin).first()
        if not exists:
            return pin


def _migrate_teacher_tests_pin(db: Session) -> None:
    """Add pin_code and is_active to teacher_tests; backfill PINs for existing rows.

    Two critical rules for this migration:
    1. Use DEFAULT TRUE (not DEFAULT 1) — PostgreSQL requires a boolean literal.
    2. Use raw SQL for all queries — ORM generates SELECT * which includes every
       column defined in the model, so if is_active doesn't exist yet the ORM
       SELECT crashes before we get a chance to add it.
    """
    for col, definition in [
        ("pin_code",  "VARCHAR(10)"),
        ("is_active", "BOOLEAN DEFAULT TRUE"),   # TRUE not 1 — works on both SQLite & PostgreSQL
    ]:
        try:
            db.execute(text(f"ALTER TABLE teacher_tests ADD COLUMN {col} {definition}"))
            db.commit()
        except Exception:
            db.rollback()  # column already exists — safe to ignore

    # Backfill: assign a PIN to every test that doesn't have one yet.
    # Raw SQL only — never use ORM here (see rule 2 above).
    try:
        rows = db.execute(
            text("SELECT id FROM teacher_tests WHERE pin_code IS NULL")
        ).fetchall()
        for row in rows:
            pin = _generate_pin_raw(db)
            db.execute(
                text("UPDATE teacher_tests SET pin_code = :pin WHERE id = :id"),
                {"pin": pin, "id": row[0]}
            )
        if rows:
            db.commit()
    except Exception:
        db.rollback()


def _migrate_users_telegram(db: Session) -> None:
    """Add telegram_id and telegram_username to users table if not present.
    Safe to call multiple times — ALTER TABLE errors are silently swallowed.
    """
    for col, defn in [
        ("telegram_id",       "BIGINT"),
        ("telegram_username", "VARCHAR(100)"),
    ]:
        try:
            db.execute(text(f"ALTER TABLE users ADD COLUMN {col} {defn}"))
            db.commit()
        except Exception:
            db.rollback()


# ── Telegram helpers ──────────────────────────────────────────────────────────

def _tg_api(method: str, payload: dict) -> dict:
    """POST to Telegram Bot API. Returns parsed JSON or empty dict on error."""
    if not TELEGRAM_BOT_TOKEN:
        return {}
    try:
        res = _req.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}",
            json=payload,
            timeout=8,
        )
        return res.json()
    except Exception:
        return {}


def _tg_get(method: str) -> dict:
    """GET to Telegram Bot API (for parameter-less methods like getMe)."""
    if not TELEGRAM_BOT_TOKEN:
        return {}
    try:
        res = _req.get(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/{method}",
            timeout=8,
        )
        return res.json()
    except Exception:
        return {}


def _tg_verify_hash(data: dict) -> bool:
    """
    Verify the hash produced by Telegram Login Widget.
    Algorithm:
      secret = SHA256(bot_token)
      check_string = key=value\\n  sorted alphabetically (excluding hash)
      hash = HMAC-SHA256(secret, check_string)
    """
    if not TELEGRAM_BOT_TOKEN:
        return False
    check_hash = str(data.get("hash", ""))
    fields = {k: str(v) for k, v in data.items() if k != "hash" and v is not None}
    data_str = "\n".join(f"{k}={v}" for k, v in sorted(fields.items()))
    secret = hashlib.sha256(TELEGRAM_BOT_TOKEN.encode()).digest()
    computed = _hmac.new(secret, data_str.encode(), hashlib.sha256).hexdigest()
    return _hmac.compare_digest(computed, check_hash)


def _tg_is_fresh(auth_date: int, max_age_seconds: int = 86400) -> bool:
    """Return True if auth_date is within max_age_seconds of now (default 24 h)."""
    return (time.time() - auth_date) < max_age_seconds


def _tg_validate_init_data(init_data: str) -> dict | None:
    """
    Validate Telegram Mini App initData string.
    Secret derivation differs from Login Widget:
      secret = HMAC-SHA256("WebAppData", bot_token)   ← Mini App
      secret = SHA256(bot_token)                       ← Login Widget
    Returns parsed params dict on success, None on failure.
    """
    if not TELEGRAM_BOT_TOKEN:
        return None
    try:
        params = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = params.pop("hash", None)
        if not received_hash:
            return None
        check_string = "\n".join(f"{k}={v}" for k, v in sorted(params.items()))
        secret = _hmac.new(b"WebAppData", TELEGRAM_BOT_TOKEN.encode(), hashlib.sha256).digest()
        computed = _hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()
        if not _hmac.compare_digest(computed, received_hash):
            return None
        return params
    except Exception:
        return None


def _tg_send(chat_id: int, text_body: str, reply_markup: dict | None = None, parse_mode: str = "Markdown") -> None:
    payload: dict = {"chat_id": chat_id, "text": text_body, "parse_mode": parse_mode}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    _tg_api("sendMessage", payload)


def _register_telegram_webhook() -> None:
    """Auto-register the webhook URL with Telegram on server startup."""
    if not TELEGRAM_BOT_TOKEN:
        return
    base_url = (
        os.getenv("WEBHOOK_URL")             # manually set override
        or os.getenv("RENDER_EXTERNAL_URL", "").rstrip("/")
    )
    if not base_url:
        return
    webhook_url = f"{base_url}/telegram/webhook"
    _tg_api("setWebhook", {"url": webhook_url, "drop_pending_updates": True})


# ── Telegram bot command handlers ─────────────────────────────────────────────

def _bot_start(chat_id: int, first_name: str) -> None:
    text_body = (
        f"👋 Привет, *{first_name}*\\!\n\n"
        f"🎯 *IELTS Mock Test Platform*\n\n"
        f"Практикуй IELTS Reading, Listening и Writing с AI\\-фидбэком\\.\n\n"
        f"📌 *Что умеет платформа:*\n"
        f"• 🔑 Вступить в тест по PIN от учителя\n"
        f"• 📊 Смотреть свои результаты\n"
        f"• ✏️ Writing с AI\\-оценкой\n"
        f"• 👨‍🏫 Учителям: создавать тесты и видеть аналитику\n\n"
        f"👇 Нажми кнопку, чтобы открыть платформу:"
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "🚀 Открыть IELTS Mock", "web_app": {"url": FRONTEND_URL}}],
            [{"text": "🔗 Связать аккаунт с Telegram", "url": f"{FRONTEND_URL}/telegram-connect.html"}],
        ]
    }
    _tg_api("sendMessage", {"chat_id": chat_id, "text": text_body, "parse_mode": "MarkdownV2", "reply_markup": keyboard})


def _bot_help(chat_id: int) -> None:
    _tg_send(chat_id, (
        "📚 *Доступные команды:*\n\n"
        "/start — Главное меню и открыть платформу\n"
        "/help — Список команд\n"
        "/link — Связать Telegram с аккаунтом\n"
        "/status — Твой текущий статус\n"
        "/progress — Твоя статистика и прогресс\n"
        "/latestscore — Последний результат теста\n"
        "/starttest — Начать тест\n"
        "/dashboard — Открыть дашборд"
    ))


def _bot_link(chat_id: int) -> None:
    keyboard = {"inline_keyboard": [[
        {"text": "🔗 Связать аккаунт", "web_app": {"url": f"{FRONTEND_URL}/telegram-connect.html"}}
    ]]}
    _tg_send(
        chat_id,
        "Чтобы связать Telegram с аккаунтом на платформе, нажми кнопку ниже.",
        reply_markup=keyboard,
    )


def _bot_status(chat_id: int, telegram_id: int, db) -> None:
    user = db.query(models.User).filter(models.User.telegram_id == telegram_id).first()
    if user:
        _tg_send(chat_id, f"✅ Ты связан с аккаунтом *{user.name}* \\({user.email}\\)\\.", parse_mode="MarkdownV2")
    else:
        _tg_send(chat_id, "❌ Твой Telegram ещё не связан с аккаунтом на платформе\\.\n\nИспользуй /link чтобы связать\\.", parse_mode="MarkdownV2")


def _bot_progress(chat_id: int, tg_id: int, db) -> None:
    user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
    if not user:
        _tg_send(chat_id, "❌ Аккаунт не связан. Открой платформу: /start")
        return
    results = (db.query(models.TeacherTestResult)
               .filter(models.TeacherTestResult.student_id == user.id)
               .order_by(models.TeacherTestResult.created_at.desc())
               .limit(5).all())
    writing = (db.query(models.WritingResult)
               .filter(models.WritingResult.user_id == user.id)
               .order_by(models.WritingResult.created_at.desc())
               .first())
    if not results and not writing:
        _tg_send(chat_id, "📊 Нет результатов ещё.\n\nНачни тест: /starttest")
        return
    text = f"📊 *Прогресс — {user.name}*\n\n"
    if results:
        bands = [r.band for r in results]
        text += f"🎯 Лучший band: *{max(bands)}*\n"
        text += f"📈 Средний: *{round(sum(bands)/len(bands), 1)}*\n"
        text += f"📝 Попыток: *{len(results)}*\n"
    if writing:
        text += f"\n✏️ Последний Writing: *{writing.band_score}* band\n"
    text += f"\n[Открыть дашборд]({FRONTEND_URL}/tg-app.html)"
    _tg_send(chat_id, text)


def _bot_latestscore(chat_id: int, tg_id: int, db) -> None:
    user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
    if not user:
        _tg_send(chat_id, "❌ Аккаунт не связан. Открой платформу: /start")
        return
    r = (db.query(models.TeacherTestResult)
         .filter(models.TeacherTestResult.student_id == user.id)
         .order_by(models.TeacherTestResult.created_at.desc())
         .first())
    if not r:
        _tg_send(chat_id, "❌ Нет результатов. Пройди тест: /starttest")
        return
    test = db.query(models.TeacherTest).filter(models.TeacherTest.id == r.test_id).first()
    _tg_send(chat_id, (
        f"🏆 *Последний результат*\n\n"
        f"📝 {test.title if test else 'Test'}\n"
        f"🎯 Band: *{r.band}*\n"
        f"✔️ {r.correct}/{r.total} правильных\n"
        f"📅 {r.created_at.strftime('%d.%m.%Y')}\n\n"
        f"[Все результаты]({FRONTEND_URL}/tg-app.html)"
    ))


def _bot_open_app(chat_id: int, command: str) -> None:
    url = f"{FRONTEND_URL}/tg-app.html"
    label = "📊 Мой Дашборд" if command == "/dashboard" else "🚀 Начать тест"
    _tg_api("sendMessage", {
        "chat_id": chat_id,
        "text": "Открываю платформу...",
        "parse_mode": "HTML",
        "reply_markup": {"inline_keyboard": [[{"text": label, "web_app": {"url": url}}]]},
    })


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    email = decode_access_token(credentials.credentials)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


def get_teacher_user(current_user: models.User = Depends(get_current_user)):
    """Dependency: only allows teachers through — returns 403 for students."""
    if current_user.role != "teacher":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Teacher access required"
        )
    return current_user


from fastapi.security import HTTPBearer as _HTTPBearer
_optional_bearer = _HTTPBearer(auto_error=False)

def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(_optional_bearer),
    db: Session = Depends(get_db),
):
    """Like get_current_user but returns None instead of 401 when no/invalid token."""
    if not credentials:
        return None
    email = decode_access_token(credentials.credentials)
    if not email:
        return None
    return db.query(models.User).filter(models.User.email == email).first()


def _band_to_level(overall: float) -> str:
    if overall >= 7.5:
        return "Advanced"
    if overall >= 6.0:
        return "Upper-Intermediate"
    if overall >= 5.0:
        return "Intermediate"
    return "Beginner"


def _calculate_band(correct: int, total: int) -> float:
    """Convert raw score to IELTS band (0–9 scale, 0.5 increments)."""
    if total == 0:
        return 0.0
    ratio = correct / total
    if ratio >= 1.0:  return 9.0
    if ratio >= 0.9:  return 8.5
    if ratio >= 0.8:  return 7.5
    if ratio >= 0.7:  return 7.0
    if ratio >= 0.6:  return 6.5
    if ratio >= 0.5:  return 6.0
    if ratio >= 0.4:  return 5.5
    if ratio >= 0.3:  return 5.0
    if ratio >= 0.2:  return 4.0
    if ratio >= 0.1:  return 3.5
    return 3.0


def _seed_questions(db: Session) -> None:
    """Populate the DB with a reading test on first startup."""
    if db.query(models.Test).filter(models.Test.type == "reading").first():
        return  # Already seeded — skip

    passage = (
        "The concept of remote work - the practice of employees working from locations "
        "other than a traditional office - has existed for decades, but it was once considered "
        "a privilege reserved for a select few. Advances in technology and the global disruption "
        "caused by the COVID-19 pandemic in 2020 dramatically accelerated its adoption. By mid-2020, "
        "surveys indicated that more than half of the American workforce was working remotely, "
        "a figure unthinkable just years earlier.\n\n"
        "Proponents of remote work argue that it offers considerable benefits for both employers "
        "and employees. Workers gain flexibility, eliminating daily commutes that can account for "
        "dozens of hours per month. Studies have shown that many employees report higher job satisfaction "
        "and better work-life balance when given the option to work from home. For employers, remote work "
        "can reduce overhead costs significantly - companies like Twitter and Dropbox have permanently "
        "downsized their office spaces, citing annual savings in the millions.\n\n"
        "However, remote work is not without its drawbacks. Critics point to the erosion of workplace "
        "culture and the challenges of maintaining team cohesion when colleagues rarely meet face-to-face. "
        "Research from Stanford University found that while individual productivity often increases for "
        "remote workers, collaborative tasks can suffer. Additionally, not all employees have adequate "
        "home environments: limited space, unreliable internet connections, and the presence of young "
        "children can turn a home into a challenging workspace.\n\n"
        "The future of work appears to be a hybrid model - a blend of remote and in-office arrangements. "
        "Major corporations including Google, Microsoft, and Apple have announced flexible working policies "
        "that allow employees to split time between home and office. Advocates of this model argue that "
        "it captures the best of both worlds: the focus and flexibility of remote work combined with the "
        "spontaneous collaboration that physical presence enables. Whether this balance proves sustainable "
        "in the long term remains to be seen, as companies continue to experiment and adapt to the "
        "evolving expectations of the modern workforce."
    )

    test = models.Test(type="reading", passage=passage)
    db.add(test)
    db.flush()  # Assigns test.id without full commit

    questions_data = [
        {
            "question_text": "What primarily accelerated the adoption of remote work?",
            "option_a": "Advances in transportation",
            "option_b": "The COVID-19 pandemic and technological advances",
            "option_c": "Government policies mandating work from home",
            "option_d": "High office rental costs",
            "correct_answer": "B",
        },
        {
            "question_text": "By mid-2020, what portion of the American workforce was working remotely?",
            "option_a": "Less than a quarter",
            "option_b": "About a third",
            "option_c": "More than half",
            "option_d": "Almost the entire workforce",
            "correct_answer": "C",
        },
        {
            "question_text": "According to the passage, what is one benefit of remote work for employees?",
            "option_a": "Higher salaries",
            "option_b": "Elimination of daily commutes",
            "option_c": "Better healthcare",
            "option_d": "Guaranteed promotions",
            "correct_answer": "B",
        },
        {
            "question_text": "Which companies are mentioned as permanently downsizing their offices?",
            "option_a": "Google and Microsoft",
            "option_b": "Apple and Amazon",
            "option_c": "Twitter and Dropbox",
            "option_d": "Stanford and MIT",
            "correct_answer": "C",
        },
        {
            "question_text": "What does Stanford University research suggest about remote work?",
            "option_a": "Individual productivity decreases for remote workers",
            "option_b": "Collaborative tasks improve with remote work",
            "option_c": "Individual productivity can increase, but collaborative tasks may suffer",
            "option_d": "All aspects of work improve when done remotely",
            "correct_answer": "C",
        },
        {
            "question_text": "Which of the following is listed as a challenge of working from home?",
            "option_a": "Too much interaction with colleagues",
            "option_b": "Unreliable internet connections",
            "option_c": "High commuting costs",
            "option_d": "Limited access to technology at the office",
            "correct_answer": "B",
        },
        {
            "question_text": "What does the passage suggest is the future model of work?",
            "option_a": "Fully remote work for all employees",
            "option_b": "Return to traditional office-only arrangements",
            "option_c": "A hybrid model combining remote and in-office work",
            "option_d": "Four-day working weeks",
            "correct_answer": "C",
        },
        {
            "question_text": "Which companies are mentioned as announcing flexible working policies?",
            "option_a": "Twitter, Dropbox, and Amazon",
            "option_b": "Google, Microsoft, and Apple",
            "option_c": "Stanford, MIT, and Harvard",
            "option_d": "Facebook, Netflix, and Spotify",
            "correct_answer": "B",
        },
        {
            "question_text": "What do advocates of the hybrid model claim it achieves?",
            "option_a": "Lower costs than fully remote work",
            "option_b": "Complete elimination of office spaces",
            "option_c": "The benefits of both remote flexibility and in-person collaboration",
            "option_d": "Improved employee health outcomes",
            "correct_answer": "C",
        },
        {
            "question_text": "What does the passage say about the long-term sustainability of the hybrid model?",
            "option_a": "It is guaranteed to succeed",
            "option_b": "It has already proven effective across all industries",
            "option_c": "It remains to be seen as companies continue to experiment",
            "option_d": "It will eventually be replaced by fully remote work",
            "correct_answer": "C",
        },
    ]

    for q_data in questions_data:
        db.add(models.Question(test_id=test.id, **q_data))

    db.commit()


def _seed_reading_tests(db: Session) -> None:
    """Populate reading_tests / reading_passages / reading_questions on first startup."""
    if db.query(models.ReadingTest).first():
        return  # Already seeded

    for test_data in READING_TESTS:
        test = models.ReadingTest(title=test_data["title"])
        db.add(test)
        db.flush()

        for p_data in test_data["passages"]:
            passage = models.ReadingPassage(
                test_id=test.id,
                order=p_data["order"],
                title=p_data["title"],
                text=p_data["text"],
            )
            db.add(passage)
            db.flush()

            for q_data in p_data["questions"]:
                db.add(models.ReadingQuestion(
                    passage_id=passage.id,
                    question_text=q_data["question_text"],
                    option_a=q_data["option_a"],
                    option_b=q_data["option_b"],
                    option_c=q_data["option_c"],
                    option_d=q_data["option_d"],
                    correct_answer=q_data["correct_answer"],
                ))

    db.commit()


@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        _migrate_add_role_column(db)
        _migrate_teacher_tests_pin(db)
        _migrate_users_telegram(db)     # Phase 6
        _seed_questions(db)
        _seed_reading_tests(db)
        try:
            seed_ielts_content(db)
        except Exception as _seed_err:
            print(f"[startup] IELTS seed skipped: {_seed_err}")
    finally:
        db.close()
    # Start Telegram bot polling (replaces the old webhook approach).
    start_polling()


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = models.User(
        name=payload.name.strip(),
        email=payload.email.lower(),
        password=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    token = create_access_token(subject=user.email)
    return schemas.Token(access_token=token)


@app.post("/login", response_model=schemas.Token)
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(subject=user.email)
    return schemas.Token(access_token=token)


@app.get("/me", response_model=schemas.UserOut)
def me(current_user: models.User = Depends(get_current_user)):
    return current_user


@app.post("/results", response_model=schemas.ResultOut, status_code=status.HTTP_201_CREATED)
def create_result(
    payload: schemas.ResultCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    result = models.Result(
        user_id=current_user.id,
        reading_score=payload.reading_score,
        listening_score=payload.listening_score,
        writing_score=payload.writing_score,
        overall=payload.overall,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@app.get("/dashboard", response_model=schemas.DashboardOut)
def dashboard(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    latest_results = (
        db.query(models.Result)
        .filter(models.Result.user_id == current_user.id)
        .order_by(models.Result.created_at.desc())
        .limit(5)
        .all()
    )

    level = _band_to_level(latest_results[0].overall if latest_results else 0.0)

    return schemas.DashboardOut(user=current_user, level=level, latest_results=latest_results)


@app.get("/questions", response_model=schemas.TestOut)
def get_questions(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    test = db.query(models.Test).filter(models.Test.type == "reading").first()
    if not test:
        raise HTTPException(status_code=404, detail="Reading test not found")
    return test


@app.post("/submit-test", response_model=schemas.SubmitResultOut)
def submit_test(
    payload: schemas.SubmitTestIn,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    questions = (
        db.query(models.Question)
        .filter(models.Question.test_id == payload.test_id)
        .all()
    )
    if not questions:
        raise HTTPException(status_code=404, detail="Test not found")

    correct = 0
    for q in questions:
        user_answer = payload.answers.get(str(q.id), "")
        if user_answer.upper() == q.correct_answer:
            correct += 1

    total = len(questions)
    band = _calculate_band(correct, total)

    return schemas.SubmitResultOut(correct=correct, total=total, band=band)


# ── Writing Module ─────────────────────────────────────────────────────────────

# The prompt sent to Claude for IELTS evaluation
_WRITING_PROMPT = """You are an experienced IELTS examiner. Evaluate this IELTS Writing Task 2 essay.

ESSAY (word count: {word_count}):
{essay}

Return ONLY valid JSON with no extra text or code blocks:
{{
  "band_score": <float 0-9 in 0.5 steps>,
  "task_achievement": {{
    "score": <float 0-9>,
    "feedback": "<specific feedback on task response and argument>"
  }},
  "coherence_cohesion": {{
    "score": <float 0-9>,
    "feedback": "<specific feedback on structure, paragraphing, and linking words>"
  }},
  "lexical_resource": {{
    "score": <float 0-9>,
    "feedback": "<specific feedback on vocabulary range and accuracy>"
  }},
  "grammatical_range": {{
    "score": <float 0-9>,
    "feedback": "<specific feedback on grammar accuracy and sentence variety>"
  }},
  "strengths": [
    "<specific strength 1>",
    "<specific strength 2>",
    "<specific strength 3>"
  ],
  "improvements": [
    "<specific actionable improvement 1>",
    "<specific actionable improvement 2>",
    "<specific actionable improvement 3>"
  ],
  "overall_feedback": "<2-3 sentence overall assessment and encouragement>"
}}"""


def _get_mock_feedback(word_count: int) -> dict:
    """Rule-based IELTS feedback used when no AI API key is configured."""
    if word_count >= 350:
        band = 6.5
    elif word_count >= 280:
        band = 6.0
    elif word_count >= 230:
        band = 5.5
    elif word_count >= 180:
        band = 5.0
    else:
        band = 4.5

    return {
        "band_score": band,
        "task_achievement": {
            "score": band,
            "feedback": "Your essay addresses the task. Ensure all parts of the question are fully covered with well-developed arguments and relevant examples."
        },
        "coherence_cohesion": {
            "score": band,
            "feedback": "Your essay shows basic organisation. Use a wider variety of cohesive devices to improve the flow between paragraphs and ideas."
        },
        "lexical_resource": {
            "score": band,
            "feedback": "You demonstrate adequate vocabulary for the task. Try to use more precise academic vocabulary and avoid unnecessary repetition."
        },
        "grammatical_range": {
            "score": band,
            "feedback": "Your grammar shows reasonable control. Work on using a wider range of sentence structures to demonstrate grammatical range."
        },
        "strengths": [
            "Essay attempts to address the given question",
            "Shows basic paragraph structure with introduction and conclusion",
            "Demonstrates understanding of the topic"
        ],
        "improvements": [
            "Develop arguments with more specific examples and evidence",
            "Use a wider range of vocabulary and academic expressions",
            "Vary sentence structures to demonstrate greater grammatical range"
        ],
        "overall_feedback": (
            f"Your essay of {word_count} words shows a working knowledge of English. "
            "Regular practice and focused study on academic writing conventions will "
            "help you achieve a higher band score. AI-powered feedback will be available soon."
        )
    }


def _get_ai_feedback(essay: str, word_count: int) -> dict:
    """Return structured IELTS feedback. Uses OpenAI when API key is set, otherwise rule-based."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return _get_mock_feedback(word_count)

    client = OpenAI(api_key=api_key)
    prompt = _WRITING_PROMPT.format(essay=essay, word_count=word_count)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an experienced IELTS examiner. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="AI returned invalid response. Please try again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@app.post("/submit-writing", response_model=schemas.WritingSubmitOut, status_code=status.HTTP_201_CREATED)
def submit_writing(
    payload: schemas.SubmitWritingIn,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    word_count = len(payload.essay.split())

    # Get IELTS feedback from OpenAI
    feedback_dict = _get_ai_feedback(payload.essay, word_count)

    band_score = float(feedback_dict.get("band_score", 0))
    if not (0 <= band_score <= 9):
        band_score = 0.0

    result = models.WritingResult(
        user_id=current_user.id,
        essay_text=payload.essay,
        feedback=json.dumps(feedback_dict),   # store as JSON string
        band_score=band_score,
        word_count=word_count,
    )
    db.add(result)
    db.commit()
    db.refresh(result)
    return result


@app.get("/writing-history", response_model=List[schemas.WritingHistoryItemOut])
def writing_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.WritingResult)
        .filter(models.WritingResult.user_id == current_user.id)
        .order_by(models.WritingResult.created_at.desc())
        .limit(5)
        .all()
    )


# ── Exam Session endpoints ─────────────────────────────────────────────────────

@app.post("/exam-session", response_model=schemas.ExamSessionOut, status_code=status.HTTP_201_CREATED)
def create_exam_session(
    payload: schemas.ExamSessionCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = models.ExamSession(
        user_id=current_user.id,
        reading_band=payload.reading_band,
        listening_band=payload.listening_band,
        writing_band=payload.writing_band,
        overall_band=payload.overall_band,
        duration_minutes=payload.duration_minutes,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


@app.get("/exam-history", response_model=List[schemas.ExamSessionOut])
def exam_history(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.ExamSession)
        .filter(models.ExamSession.user_id == current_user.id)
        .order_by(models.ExamSession.created_at.desc())
        .limit(20)
        .all()
    )


# ── Multiple Reading Tests Routes ──────────────────────────────────────────────

@app.get("/reading-tests", response_model=List[schemas.ReadingTestListItem])
def list_reading_tests(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(models.ReadingTest).all()


@app.get("/reading-test/{test_id}", response_model=schemas.ReadingTestOut)
def get_reading_test(
    test_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    test = db.query(models.ReadingTest).filter(models.ReadingTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Reading test not found")
    return test


@app.get("/random-reading-test", response_model=schemas.ReadingTestOut)
def get_random_reading_test(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    tests = db.query(models.ReadingTest).all()
    if not tests:
        raise HTTPException(status_code=404, detail="No reading tests available")
    return random.choice(tests)


@app.post("/submit-reading-test", response_model=schemas.ReadingResultOut)
def submit_reading_test(
    payload: schemas.SubmitReadingIn,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    passages = (
        db.query(models.ReadingPassage)
        .filter(models.ReadingPassage.test_id == payload.test_id)
        .all()
    )
    if not passages:
        raise HTTPException(status_code=404, detail="Reading test not found")

    all_questions = []
    for p in passages:
        all_questions.extend(p.questions)

    correct = sum(
        1 for q in all_questions
        if payload.answers.get(str(q.id), "").upper() == q.correct_answer
    )
    total = len(all_questions)
    band = _calculate_band(correct, total)

    return schemas.ReadingResultOut(correct=correct, total=total, band=band)


# ── Teacher Routes ─────────────────────────────────────────────────────────────

@app.get("/teacher/stats")
def teacher_stats(
    current_user: models.User = Depends(get_teacher_user),
    db: Session = Depends(get_db),
):
    """Teacher stats: students/completions scoped to this teacher's tests."""
    teacher_test_ids = [
        t.id for t in db.query(models.TeacherTest)
        .filter(models.TeacherTest.teacher_id == current_user.id).all()
    ]

    enrolled_students = 0
    total_completions = 0
    if teacher_test_ids:
        enrolled_students = (
            db.query(models.StudentTestEnrollment.student_id)
            .filter(models.StudentTestEnrollment.test_id.in_(teacher_test_ids))
            .distinct().count()
        )
        total_completions = (
            db.query(models.TeacherTestResult)
            .filter(models.TeacherTestResult.test_id.in_(teacher_test_ids))
            .count()
        )

    return {
        "teacher_name": current_user.name,
        "enrolled_students": enrolled_students,
        "total_completions": total_completions,
        # kept for backward compat, unused by updated dashboard
        "total_students": db.query(models.User).filter(models.User.role == "student").count(),
        "total_exam_sessions": db.query(models.ExamSession).count(),
    }


@app.post("/teacher/create-test", response_model=schemas.TeacherTestOut, status_code=status.HTTP_201_CREATED)
def create_teacher_test(
    payload: schemas.TeacherTestIn,
    current_user: models.User = Depends(get_teacher_user),
    db: Session = Depends(get_db),
):
    if not payload.passages:
        raise HTTPException(status_code=400, detail="At least one passage is required")

    test = models.TeacherTest(
        teacher_id=current_user.id,
        title=payload.title.strip(),
        description=payload.description.strip(),
        test_type=payload.test_type,
        pin_code=_generate_pin(db),
        is_active=True,
    )
    db.add(test)
    db.flush()

    for p_data in payload.passages:
        if not p_data.questions:
            raise HTTPException(status_code=400, detail=f"Passage '{p_data.title}' must have at least one question")
        passage = models.TeacherPassage(
            test_id=test.id,
            order=p_data.order,
            title=p_data.title.strip(),
            text=p_data.text.strip(),
        )
        db.add(passage)
        db.flush()

        for q_data in p_data.questions:
            db.add(models.TeacherQuestion(
                passage_id=passage.id,
                question_text=q_data.question_text.strip(),
                option_a=q_data.option_a.strip(),
                option_b=q_data.option_b.strip(),
                option_c=q_data.option_c.strip(),
                option_d=q_data.option_d.strip(),
                correct_answer=q_data.correct_answer.upper(),
            ))

    db.commit()
    db.refresh(test)
    return test


@app.get("/teacher/tests", response_model=List[schemas.TeacherTestSummary])
def list_teacher_tests(
    current_user: models.User = Depends(get_teacher_user),
    db: Session = Depends(get_db),
):
    tests = (
        db.query(models.TeacherTest)
        .filter(models.TeacherTest.teacher_id == current_user.id)
        .order_by(models.TeacherTest.created_at.desc())
        .all()
    )
    result = []
    for t in tests:
        passage_count = len(t.passages)
        question_count = sum(len(p.questions) for p in t.passages)
        enrolled_count = len(t.enrollments)
        result.append(schemas.TeacherTestSummary(
            id=t.id,
            title=t.title,
            description=t.description,
            test_type=t.test_type,
            pin_code=t.pin_code,
            is_active=bool(t.is_active) if t.is_active is not None else True,
            created_at=t.created_at,
            passage_count=passage_count,
            question_count=question_count,
            enrolled_count=enrolled_count,
        ))
    return result


@app.get("/teacher/test/{test_id}", response_model=schemas.TeacherTestOut)
def get_teacher_test(
    test_id: int,
    current_user: models.User = Depends(get_teacher_user),
    db: Session = Depends(get_db),
):
    test = (
        db.query(models.TeacherTest)
        .filter(models.TeacherTest.id == test_id, models.TeacherTest.teacher_id == current_user.id)
        .first()
    )
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


@app.delete("/teacher/test/{test_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher_test(
    test_id: int,
    current_user: models.User = Depends(get_teacher_user),
    db: Session = Depends(get_db),
):
    test = (
        db.query(models.TeacherTest)
        .filter(models.TeacherTest.id == test_id, models.TeacherTest.teacher_id == current_user.id)
        .first()
    )
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    db.delete(test)
    db.commit()


@app.patch("/teacher/test/{test_id}/toggle")
def toggle_teacher_test(
    test_id: int,
    current_user: models.User = Depends(get_teacher_user),
    db: Session = Depends(get_db),
):
    """Teacher can activate or deactivate a test (prevents students from accessing it)."""
    test = (
        db.query(models.TeacherTest)
        .filter(models.TeacherTest.id == test_id, models.TeacherTest.teacher_id == current_user.id)
        .first()
    )
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    test.is_active = not bool(test.is_active)
    db.commit()
    return {"id": test_id, "is_active": test.is_active}


# ── PIN / Student Test Access Routes ──────────────────────────────────────────

@app.post("/join-test")
def join_test(
    payload: schemas.JoinTestIn,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Student joins a teacher test using a PIN code. Idempotent — safe to call multiple times."""
    test = db.query(models.TeacherTest).filter(
        models.TeacherTest.pin_code == payload.pin.strip()
    ).first()

    if not test:
        raise HTTPException(status_code=404, detail="Invalid PIN code. No test found.")

    if not bool(test.is_active):
        raise HTTPException(status_code=403, detail="This test is not currently active.")

    existing = db.query(models.StudentTestEnrollment).filter(
        models.StudentTestEnrollment.student_id == current_user.id,
        models.StudentTestEnrollment.test_id == test.id,
    ).first()

    already_joined = existing is not None
    if not already_joined:
        db.add(models.StudentTestEnrollment(student_id=current_user.id, test_id=test.id))
        db.commit()

    teacher = db.query(models.User).filter(models.User.id == test.teacher_id).first()
    return {
        "test_id": test.id,
        "title": test.title,
        "teacher_name": teacher.name if teacher else "Unknown",
        "already_joined": already_joined,
    }


@app.get("/student/joined-tests")
def get_joined_tests(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns all teacher tests this student has joined."""
    enrollments = (
        db.query(models.StudentTestEnrollment)
        .filter(models.StudentTestEnrollment.student_id == current_user.id)
        .order_by(models.StudentTestEnrollment.joined_at.desc())
        .all()
    )

    result = []
    for e in enrollments:
        t = e.test
        teacher = db.query(models.User).filter(models.User.id == t.teacher_id).first()
        result.append({
            "test_id": t.id,
            "title": t.title,
            "description": t.description,
            "test_type": t.test_type,
            "teacher_name": teacher.name if teacher else "Unknown",
            "passage_count": len(t.passages),
            "question_count": sum(len(p.questions) for p in t.passages),
            "is_active": bool(t.is_active) if t.is_active is not None else True,
            "joined_at": e.joined_at.isoformat(),
        })
    return result


@app.get("/student/teacher-test/{test_id}", response_model=schemas.TeacherTestOut)
def get_student_teacher_test(
    test_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns the full test content — only if the student is enrolled."""
    enrollment = db.query(models.StudentTestEnrollment).filter(
        models.StudentTestEnrollment.student_id == current_user.id,
        models.StudentTestEnrollment.test_id == test_id,
    ).first()

    if not enrollment:
        raise HTTPException(
            status_code=403,
            detail="You are not enrolled in this test. Join with a PIN code first."
        )

    test = db.query(models.TeacherTest).filter(models.TeacherTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    if not bool(test.is_active):
        raise HTTPException(status_code=403, detail="This test is currently inactive.")

    return test


@app.post("/submit-teacher-test", response_model=schemas.ReadingResultOut)
def submit_teacher_test(
    payload: schemas.SubmitReadingIn,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Grade a teacher test submission. Student must be enrolled."""
    enrollment = db.query(models.StudentTestEnrollment).filter(
        models.StudentTestEnrollment.student_id == current_user.id,
        models.StudentTestEnrollment.test_id == payload.test_id,
    ).first()

    if not enrollment:
        raise HTTPException(status_code=403, detail="Not enrolled in this test")

    test = db.query(models.TeacherTest).filter(models.TeacherTest.id == payload.test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    all_questions = []
    for p in test.passages:
        all_questions.extend(p.questions)

    correct = sum(
        1 for q in all_questions
        if payload.answers.get(str(q.id), "").upper() == q.correct_answer
    )
    total = len(all_questions)
    band = _calculate_band(correct, total)

    # Persist every submission so the teacher can see results
    db.add(models.TeacherTestResult(
        student_id=current_user.id,
        test_id=payload.test_id,
        correct=correct,
        total=total,
        band=band,
    ))
    db.commit()

    # Telegram notification — only if this student linked their account
    if current_user.telegram_id:
        _tg_send(
            current_user.telegram_id,
            f"✅ *Тест завершён!*\n\n"
            f"📝 {test.title}\n"
            f"🎯 Band Score: *{band}*\n"
            f"✔️ Правильных: {correct}/{total}\n\n"
            f"[Открыть дашборд]({FRONTEND_URL}/tg-app.html)",
        )

    return schemas.ReadingResultOut(correct=correct, total=total, band=band)


# ── Teacher: per-test student results ────────────────────────────────────────

@app.get("/teacher/test/{test_id}/results", response_model=List[schemas.TeacherStudentResult])
def get_test_student_results(
    test_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return latest result per student for a specific teacher test, sorted by band desc."""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teachers only")

    test = db.query(models.TeacherTest).filter(
        models.TeacherTest.id == test_id,
        models.TeacherTest.teacher_id == current_user.id,
    ).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    # All submissions for this test
    all_results = (
        db.query(models.TeacherTestResult)
        .filter(models.TeacherTestResult.test_id == test_id)
        .order_by(models.TeacherTestResult.created_at.desc())
        .all()
    )

    # Group by student_id — keep latest result, count attempts
    seen: dict = {}
    for r in all_results:
        if r.student_id not in seen:
            seen[r.student_id] = {"result": r, "attempts": 0}
        seen[r.student_id]["attempts"] += 1

    out = []
    for student_id, data in seen.items():
        r = data["result"]
        student = db.query(models.User).filter(models.User.id == student_id).first()
        if not student:
            continue
        out.append(schemas.TeacherStudentResult(
            student_id=student_id,
            student_name=student.name,
            student_email=student.email,
            correct=r.correct,
            total=r.total,
            band=r.band,
            attempts=data["attempts"],
            latest_at=r.created_at,
        ))

    out.sort(key=lambda x: x.band, reverse=True)
    return out


# ── Teacher: overview of all tests with stats ─────────────────────────────────

@app.get("/teacher/results", response_model=List[schemas.TeacherResultsOverview])
def get_teacher_results_overview(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return per-test stats overview for all tests owned by this teacher."""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teachers only")

    tests = (
        db.query(models.TeacherTest)
        .filter(models.TeacherTest.teacher_id == current_user.id)
        .order_by(models.TeacherTest.created_at.desc())
        .all()
    )

    overview = []
    for t in tests:
        passage_count = len(t.passages)
        question_count = sum(len(p.questions) for p in t.passages)
        enrolled_count = db.query(models.StudentTestEnrollment).filter(
            models.StudentTestEnrollment.test_id == t.id
        ).count()
        all_subs = db.query(models.TeacherTestResult).filter(
            models.TeacherTestResult.test_id == t.id
        ).all()
        submission_count = len(all_subs)
        unique_completions = len({r.student_id for r in all_subs})
        bands = [r.band for r in all_subs]
        avg_band = round(sum(bands) / len(bands), 2) if bands else 0.0
        best_band = max(bands) if bands else 0.0

        overview.append(schemas.TeacherResultsOverview(
            test_id=t.id,
            test_title=t.title,
            pin_code=t.pin_code,
            is_active=bool(t.is_active),
            enrolled_count=enrolled_count,
            submission_count=submission_count,
            unique_completions=unique_completions,
            avg_band=avg_band,
            best_band=best_band,
            passage_count=passage_count,
            question_count=question_count,
        ))

    return overview


# ── Student: preview test by PIN (no enrollment created) ─────────────────────

@app.get("/join-test/{pin}")
def preview_test_by_pin(
    pin: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return test info for a PIN without creating an enrollment. Used for preview UI."""
    test = db.query(models.TeacherTest).filter(
        models.TeacherTest.pin_code == pin.strip()
    ).first()

    if not test:
        raise HTTPException(status_code=404, detail="Invalid PIN. No test found.")

    if not bool(test.is_active):
        raise HTTPException(status_code=403, detail="This test is currently inactive.")

    teacher = db.query(models.User).filter(models.User.id == test.teacher_id).first()
    already_joined = db.query(models.StudentTestEnrollment).filter(
        models.StudentTestEnrollment.student_id == current_user.id,
        models.StudentTestEnrollment.test_id == test.id,
    ).first() is not None

    return {
        "test_id": test.id,
        "title": test.title,
        "description": test.description,
        "teacher_name": teacher.name if teacher else "Unknown",
        "passage_count": len(test.passages),
        "question_count": sum(len(p.questions) for p in test.passages),
        "already_joined": already_joined,
    }


# ── Student: own attempt history across all joined teacher tests ──────────────

@app.get("/student/my-teacher-results")
def get_my_teacher_results(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Returns the student's attempt stats per teacher test.
    Shape: { "<test_id>": { attempts, best_band, latest_band, latest_at } }
    """
    results = (
        db.query(models.TeacherTestResult)
        .filter(models.TeacherTestResult.student_id == current_user.id)
        .order_by(models.TeacherTestResult.created_at.desc())
        .all()
    )

    grouped: dict = {}
    for r in results:
        key = str(r.test_id)
        if key not in grouped:
            grouped[key] = {
                "attempts": 0,
                "best_band": 0.0,
                "latest_band": None,
                "latest_at": None,
            }
        grouped[key]["attempts"] += 1
        if r.band > grouped[key]["best_band"]:
            grouped[key]["best_band"] = r.band
        if grouped[key]["latest_band"] is None:
            grouped[key]["latest_band"] = r.band
            grouped[key]["latest_at"] = r.created_at.isoformat()

    return grouped


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PHASE 5 — Teacher Analytics                                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

def _require_teacher(current_user: models.User) -> models.User:
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teachers only")
    return current_user


@app.get("/teacher/analytics", response_model=schemas.TeacherAnalyticsSummary)
def get_teacher_analytics(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Aggregate summary across ALL tests owned by this teacher:
    unique students, avg band, completion rate, total attempts.
    """
    _require_teacher(current_user)

    tests = (
        db.query(models.TeacherTest)
        .filter(models.TeacherTest.teacher_id == current_user.id)
        .all()
    )
    test_ids = [t.id for t in tests]

    if not test_ids:
        return schemas.TeacherAnalyticsSummary(
            total_tests=0,
            unique_students=0,
            total_submissions=0,
            overall_avg_band=0.0,
            overall_best_band=0.0,
            completion_rate=0.0,
            total_attempts=0,
        )

    enrollments = (
        db.query(models.StudentTestEnrollment)
        .filter(models.StudentTestEnrollment.test_id.in_(test_ids))
        .all()
    )
    unique_students = len({e.student_id for e in enrollments})

    results = (
        db.query(models.TeacherTestResult)
        .filter(models.TeacherTestResult.test_id.in_(test_ids))
        .all()
    )
    total_submissions = len(results)
    unique_submitters = len({r.student_id for r in results})
    bands = [r.band for r in results]
    overall_avg = round(sum(bands) / len(bands), 2) if bands else 0.0
    overall_best = max(bands) if bands else 0.0
    completion_rate = round(unique_submitters / unique_students * 100, 1) if unique_students > 0 else 0.0

    return schemas.TeacherAnalyticsSummary(
        total_tests=len(tests),
        unique_students=unique_students,
        total_submissions=total_submissions,
        overall_avg_band=overall_avg,
        overall_best_band=overall_best,
        completion_rate=completion_rate,
        total_attempts=total_submissions,
    )


@app.get("/teacher/student-stats", response_model=List[schemas.StudentAnalyticsStat])
def get_teacher_student_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Per-student rollup across all tests owned by this teacher.
    Returns every enrolled student with band stats, attempt counts, and a
    is_weak flag (best_band < 5.5).  Sorted by best_band descending.
    """
    _require_teacher(current_user)

    tests = (
        db.query(models.TeacherTest)
        .filter(models.TeacherTest.teacher_id == current_user.id)
        .all()
    )
    test_ids = [t.id for t in tests]

    if not test_ids:
        return []

    # All enrollments for this teacher's tests
    enrollments = (
        db.query(models.StudentTestEnrollment)
        .filter(models.StudentTestEnrollment.test_id.in_(test_ids))
        .all()
    )

    # Build map: student_id → {test_ids they're enrolled in}
    enrolled_map: dict = {}
    for e in enrollments:
        enrolled_map.setdefault(e.student_id, set()).add(e.test_id)

    # All submissions
    results = (
        db.query(models.TeacherTestResult)
        .filter(models.TeacherTestResult.test_id.in_(test_ids))
        .order_by(models.TeacherTestResult.created_at.desc())
        .all()
    )

    # Build map: student_id → list of results
    results_map: dict = {}
    for r in results:
        results_map.setdefault(r.student_id, []).append(r)

    out = []
    for student_id, enrolled_tests in enrolled_map.items():
        student = db.query(models.User).filter(models.User.id == student_id).first()
        if not student:
            continue

        student_results = results_map.get(student_id, [])
        bands = [r.band for r in student_results]
        best_band = max(bands) if bands else 0.0
        avg_band  = round(sum(bands) / len(bands), 2) if bands else 0.0
        tests_completed = len({r.test_id for r in student_results})
        last_active = student_results[0].created_at if student_results else None

        out.append(schemas.StudentAnalyticsStat(
            student_id=student_id,
            student_name=student.name,
            student_email=student.email,
            best_band=best_band,
            avg_band=avg_band,
            total_attempts=len(student_results),
            tests_enrolled=len(enrolled_tests),
            tests_completed=tests_completed,
            last_active_at=last_active,
            is_weak=best_band < 5.5 and len(student_results) > 0,
        ))

    out.sort(key=lambda x: x.best_band, reverse=True)
    return out


@app.get("/teacher/leaderboard", response_model=List[schemas.StudentAnalyticsStat])
def get_teacher_leaderboard(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Top 20 students by best band — convenience alias that reuses student-stats logic."""
    all_stats = get_teacher_student_stats(current_user=current_user, db=db)
    # Filter to students who actually submitted (band > 0) and return top 20
    submitted = [s for s in all_stats if s.total_attempts > 0]
    return submitted[:20]


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PHASE 6 — Telegram Bot + Mini App                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

@app.post("/telegram/webhook", include_in_schema=False)
async def telegram_webhook(request: Request, db: Session = Depends(get_db)):
    """
    Telegram sends every update (message, callback, etc.) here via POST.
    Endpoint is excluded from OpenAPI docs — it's not called by the frontend.
    Security: only Telegram can reach this URL (they use HTTPS).
    """
    try:
        update = await request.json()
    except Exception:
        return {"ok": True}

    message = update.get("message") or update.get("edited_message")
    if not message:
        return {"ok": True}

    chat_id   = message["chat"]["id"]
    text_body = message.get("text", "")
    from_user = message.get("from", {})
    tg_id     = from_user.get("id")
    first_name = from_user.get("first_name", "Student")

    if text_body.startswith("/start"):
        _bot_start(chat_id, first_name)
    elif text_body == "/help":
        _bot_help(chat_id)
    elif text_body == "/link":
        _bot_link(chat_id)
    elif text_body == "/status":
        _bot_status(chat_id, tg_id, db)
    elif text_body == "/progress":
        _bot_progress(chat_id, tg_id, db)
    elif text_body == "/latestscore":
        _bot_latestscore(chat_id, tg_id, db)
    elif text_body in ("/starttest", "/dashboard"):
        _bot_open_app(chat_id, text_body)

    return {"ok": True}


@app.get("/telegram/bot-info")
def telegram_bot_info():
    """
    Return the bot's public username so the frontend can dynamically load
    the Telegram Login Widget without hardcoding the bot name.
    """
    if not TELEGRAM_BOT_TOKEN:
        raise HTTPException(status_code=503, detail="Telegram is not configured on this server")
    result = _tg_get("getMe")
    if not result.get("ok"):
        raise HTTPException(status_code=503, detail="Could not reach Telegram API")
    return {
        "username": result["result"]["username"],
        "name":     result["result"]["first_name"],
    }


@app.post("/telegram/auth")
def telegram_auth(data: schemas.TelegramAuthIn, db: Session = Depends(get_db)):
    """
    Verify Telegram Login Widget data sent by the frontend.
    • If a platform account is already linked → return a JWT so the user is
      immediately logged in.
    • If no account is linked yet → return 404 so the frontend can tell the
      user to log in with email first and then link their Telegram.

    Security:
    - Hash verified with HMAC-SHA256 using SHA256(bot_token) as the key.
    - auth_date must be within 24 hours.
    """
    if not _tg_verify_hash(data.dict()):
        raise HTTPException(status_code=400, detail="Invalid Telegram auth data — hash mismatch")
    if not _tg_is_fresh(data.auth_date):
        raise HTTPException(status_code=400, detail="Telegram auth data is too old. Please try again.")

    user = db.query(models.User).filter(models.User.telegram_id == data.id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="No account linked to this Telegram. Log in with email first, then connect Telegram in Settings.",
        )

    token = create_access_token(subject=user.email)
    return {
        "status":       "linked",
        "access_token": token,
        "token_type":   "bearer",
        "role":         user.role,
        "name":         user.name,
    }


@app.post("/telegram/link")
def telegram_link(
    data: schemas.TelegramAuthIn,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Link a Telegram account to the currently logged-in platform account.
    Requires a valid JWT (the user must already be logged in via email).

    Flow:
    1. Frontend calls Telegram Login Widget → gets auth data
    2. Frontend sends auth data + JWT to this endpoint
    3. Backend verifies hash and links accounts
    """
    if not _tg_verify_hash(data.dict()):
        raise HTTPException(status_code=400, detail="Invalid Telegram auth data — hash mismatch")
    if not _tg_is_fresh(data.auth_date):
        raise HTTPException(status_code=400, detail="Telegram auth data is too old. Please try again.")

    # Check if this Telegram account is already linked to a DIFFERENT user
    conflict = db.query(models.User).filter(
        models.User.telegram_id == data.id,
        models.User.id != current_user.id,
    ).first()
    if conflict:
        raise HTTPException(
            status_code=409,
            detail="This Telegram account is already linked to another platform account.",
        )

    current_user.telegram_id       = data.id
    current_user.telegram_username = data.username
    db.commit()
    db.refresh(current_user)

    return {
        "status":             "linked",
        "telegram_id":        data.id,
        "telegram_username":  data.username or "",
        "first_name":         data.first_name,
    }


@app.delete("/telegram/unlink")
def telegram_unlink(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Remove the Telegram link from the current account."""
    current_user.telegram_id       = None
    current_user.telegram_username = None
    db.commit()
    return {"status": "unlinked"}


# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  PHASE 7 — Telegram Mini App Ecosystem                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

@app.post("/telegram/miniapp-auth")
def telegram_miniapp_auth(
    payload: schemas.TelegramMiniAppAuthIn,
    db: Session = Depends(get_db),
):
    """
    Authenticate a Telegram Mini App user via initData.

    Flow:
      1. Frontend sends window.Telegram.WebApp.initData as {init_data: "..."}
      2. Backend validates HMAC-SHA256 signature (using "WebAppData" as key prefix)
      3. Extracts Telegram user ID from the validated data
      4. Finds the platform account linked to that Telegram ID
      5. Returns JWT so the Mini App can call all normal API endpoints

    Security: Mini App secret = HMAC-SHA256("WebAppData", bot_token) — different
    from Login Widget which uses SHA256(bot_token) directly.
    """
    params = _tg_validate_init_data(payload.init_data)
    if params is None:
        raise HTTPException(status_code=400, detail="Invalid Telegram initData — signature mismatch")

    try:
        tg_user = json.loads(params.get("user", "{}"))
    except Exception:
        raise HTTPException(status_code=400, detail="Cannot parse user from initData")

    tg_id = tg_user.get("id")
    if not tg_id:
        raise HTTPException(status_code=400, detail="No user ID in initData")

    user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="no_account_linked")

    token = create_access_token(subject=user.email)
    return {
        "access_token": token,
        "token_type":   "bearer",
        "role":         user.role,
        "name":         user.name,
    }


@app.get("/student/progress-summary")
def get_progress_summary(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Single-call summary for the Telegram Mini App dashboard.
    Returns: user info, stats (best/avg band, attempts), recent results, joined tests.
    """
    teacher_results = (
        db.query(models.TeacherTestResult)
        .filter(models.TeacherTestResult.student_id == current_user.id)
        .order_by(models.TeacherTestResult.created_at.desc())
        .limit(20).all()
    )
    writing_results = (
        db.query(models.WritingResult)
        .filter(models.WritingResult.user_id == current_user.id)
        .order_by(models.WritingResult.created_at.desc())
        .limit(5).all()
    )

    all_bands = [r.band for r in teacher_results] + [r.band_score for r in writing_results]
    best_band = max(all_bands) if all_bands else 0.0
    avg_band  = round(sum(all_bands) / len(all_bands), 1) if all_bands else 0.0

    recent: list = []
    for r in teacher_results[:8]:
        test = db.query(models.TeacherTest).filter(models.TeacherTest.id == r.test_id).first()
        recent.append({
            "type":       "reading",
            "title":      test.title if test else f"Test #{r.test_id}",
            "band":       r.band,
            "correct":    r.correct,
            "total":      r.total,
            "word_count": None,
            "created_at": r.created_at.isoformat(),
        })
    for r in writing_results[:4]:
        recent.append({
            "type":       "writing",
            "title":      "Writing Task",
            "band":       r.band_score,
            "correct":    None,
            "total":      None,
            "word_count": r.word_count,
            "created_at": r.created_at.isoformat(),
        })
    recent.sort(key=lambda x: x["created_at"], reverse=True)

    enrollments = (
        db.query(models.StudentTestEnrollment)
        .filter(models.StudentTestEnrollment.student_id == current_user.id)
        .order_by(models.StudentTestEnrollment.joined_at.desc())
        .all()
    )
    joined = [
        {
            "test_id":   e.test.id,
            "title":     e.test.title,
            "test_type": e.test.test_type,
            "is_active": bool(e.test.is_active) if e.test.is_active is not None else True,
        }
        for e in enrollments
    ]

    return {
        "user": {
            "id":    current_user.id,
            "name":  current_user.name,
            "email": current_user.email,
            "role":  current_user.role,
        },
        "stats": {
            "best_band":           best_band,
            "avg_band":            avg_band,
            "total_attempts":      len(teacher_results),
            "writing_submissions": len(writing_results),
        },
        "recent_results": recent[:8],
        "joined_tests":   joined,
    }


# ── Telegram Verification Code linking (Phase 8) ─────────────────────────────
#
# Simple flow:
#   1. User clicks "Connect Telegram" on website → POST /telegram/generate-code
#   2. Backend stores a 6-digit code with 10-minute expiry in DB
#   3. User opens the Telegram bot and sends:  /link 123456
#   4. Bot reads the code from DB, links user_id ↔ telegram_id, marks code used
#   5. Website polls GET /telegram/status every 3s until linked = true
#
# Why this is secure:
#   - Code expires in 10 minutes
#   - Code is one-time use (used=True after first successful verification)
#   - Only someone in control of the Telegram account can send the code to the bot
#   - No HMAC or OAuth complexity needed
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/telegram/generate-code")
def generate_telegram_code(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Generate a 6-digit verification code for linking Telegram.
    Deletes any existing unused codes for this user first (one active code per user).
    Returns: { code, expires_at, expires_in_seconds }
    """
    # Delete old unused codes for this user so there's only one active at a time
    db.query(models.TelegramVerificationCode).filter(
        models.TelegramVerificationCode.user_id == current_user.id,
        models.TelegramVerificationCode.used == False,
    ).delete(synchronize_session=False)
    db.commit()

    # Generate a unique 6-digit code
    for _ in range(20):  # safety limit — practically never loops
        code = str(random.randint(100000, 999999))
        clash = db.query(models.TelegramVerificationCode).filter(
            models.TelegramVerificationCode.code == code,
            models.TelegramVerificationCode.used == False,
        ).first()
        if not clash:
            break

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=10)
    db.add(models.TelegramVerificationCode(
        user_id=current_user.id,
        code=code,
        expires_at=expires_at,
        used=False,
    ))
    db.commit()

    return {
        "code":               code,
        "expires_at":         expires_at.isoformat(),
        "expires_in_seconds": 600,
    }


@app.get("/telegram/status")
def get_telegram_status(
    current_user: models.User = Depends(get_current_user),
):
    """
    Lightweight endpoint polled by the frontend every few seconds
    to detect when the bot has finished linking the account.
    """
    return {
        "linked":             current_user.telegram_id is not None,
        "telegram_id":        current_user.telegram_id,
        "telegram_username":  current_user.telegram_username,
    }


# ── Telegram Login / Recovery Flow ────────────────────────────────────────────
# No JWT required — for users who forgot their email/password.
# Flow:
#   1. Site calls POST /telegram/login-code  → returns {code, expires_in_seconds}
#   2. User sends /login CODE to the bot
#   3. Bot finds account by telegram_id → sets user_id + verified = True
#   4. Site polls GET /telegram/login-status?code=... → when verified, calls step 5
#   5. Site calls POST /telegram/login-exchange  → receives JWT, logs in
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/telegram/login-code")
def telegram_login_code(db: Session = Depends(get_db)):
    """
    Generate a 6-digit login code (no auth required).
    The bot will fill in user_id when the user sends /login CODE.
    """
    # Generate a unique 6-digit code
    for _ in range(20):
        code = str(random.randint(100000, 999999))
        clash = db.query(models.TelegramLoginCode).filter(
            models.TelegramLoginCode.code == code,
            models.TelegramLoginCode.used == False,
            models.TelegramLoginCode.verified == False,
        ).first()
        if not clash:
            break

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    db.add(models.TelegramLoginCode(
        code=code,
        user_id=None,
        expires_at=expires_at,
        verified=False,
        used=False,
    ))
    db.commit()

    return {
        "code":               code,
        "expires_in_seconds": 300,
    }


@app.get("/telegram/login-status")
def telegram_login_status(code: str, db: Session = Depends(get_db)):
    """
    Poll whether the bot has verified the login code.
    Returns {verified, expired}.
    """
    record = db.query(models.TelegramLoginCode).filter(
        models.TelegramLoginCode.code == code,
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Code not found")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    expires = record.expires_at
    if expires.tzinfo is not None:
        expires = expires.replace(tzinfo=None)

    return {
        "verified": record.verified,
        "expired":  now > expires,
    }


@app.post("/telegram/login-exchange")
def telegram_login_exchange(code: str = Body(..., embed=True), db: Session = Depends(get_db)):
    """
    Exchange a verified login code for a JWT.
    Marks the code as used so it can't be replayed.
    """
    record = db.query(models.TelegramLoginCode).filter(
        models.TelegramLoginCode.code == code,
    ).first()

    if not record:
        raise HTTPException(status_code=404, detail="Code not found")

    if record.used:
        raise HTTPException(status_code=400, detail="Code already used")

    if not record.verified:
        raise HTTPException(status_code=400, detail="Code not yet verified")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    expires = record.expires_at
    if expires.tzinfo is not None:
        expires = expires.replace(tzinfo=None)
    if now > expires:
        raise HTTPException(status_code=400, detail="Code expired")

    user = db.query(models.User).filter(models.User.id == record.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    record.used = True
    db.commit()

    token = create_access_token(subject=user.email)
    return {"token": token, "name": user.name, "role": user.role}


# ═══════════════════════════════════════════════════════════════════════════════
# IELTS QUESTION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

# ── Band score lookup tables (official IELTS conversion) ──────────────────────
_READING_BANDS = [
    (39, 9.0), (37, 8.5), (35, 8.0), (33, 7.5), (30, 7.0),
    (27, 6.5), (23, 6.0), (19, 5.5), (15, 5.0), (13, 4.5),
    (10, 4.0), (8, 3.5), (6, 3.0), (4, 2.5), (0, 2.0),
]

_LISTENING_BANDS = [
    (39, 9.0), (37, 8.5), (35, 8.0), (32, 7.5), (30, 7.0),
    (26, 6.5), (23, 6.0), (18, 5.5), (16, 5.0), (13, 4.5),
    (10, 4.0), (8, 3.5), (6, 3.0), (4, 2.5), (0, 2.0),
]


def _raw_to_band(raw: int, component: str = "reading") -> float:
    table = _LISTENING_BANDS if component == "listening" else _READING_BANDS
    for min_score, band in table:
        if raw >= min_score:
            return band
    return 0.0


def _check_answer(student: Optional[str], correct: str, variants: Optional[list]) -> bool:
    """Case-insensitive answer check with optional acceptable variants."""
    if not student:
        return False
    s = student.strip().lower()
    c = correct.strip().lower()
    if s == c:
        return True
    if variants:
        return s in [v.strip().lower() for v in variants]
    return False


# ── List available IELTS tests ────────────────────────────────────────────────

@app.get("/ielts/tests", response_model=List[schemas.IELTSTestListItem])
def list_ielts_tests(
    current_user: models.User = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    tests = (db.query(models.IELTSTest)
             .filter(models.IELTSTest.is_active == True)
             .order_by(models.IELTSTest.created_at.desc())
             .all())

    if not current_user:
        return tests

    # Enrich with per-user attempt stats
    attempts = (
        db.query(models.IELTSAttempt)
        .filter(
            models.IELTSAttempt.user_id == current_user.id,
            models.IELTSAttempt.status == "submitted",
        )
        .all()
    )
    best: dict = {}
    count: dict = {}
    for a in attempts:
        count[a.test_id] = count.get(a.test_id, 0) + 1
        if a.band_score is not None:
            prev = best.get(a.test_id)
            if prev is None or a.band_score > prev:
                best[a.test_id] = a.band_score

    result = []
    for t in tests:
        item = schemas.IELTSTestListItem(
            id=t.id, title=t.title, test_type=t.test_type,
            component=t.component, time_limit=t.time_limit,
            best_band=best.get(t.id),
            attempt_count=count.get(t.id, 0) or None,
        )
        result.append(item)
    return result


# ── Get full test structure (no correct answers) ──────────────────────────────

@app.get("/ielts/test/{test_id}", response_model=schemas.IELTSTestOut)
def get_ielts_test(test_id: int, db: Session = Depends(get_db)):
    test = db.query(models.IELTSTest).filter(models.IELTSTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test


# ── Start or resume an attempt ────────────────────────────────────────────────

@app.post("/ielts/start/{test_id}", response_model=schemas.StartAttemptOut)
def start_ielts_attempt(
    test_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    test = db.query(models.IELTSTest).filter(models.IELTSTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    # Resume existing in-progress attempt if one exists
    existing = (db.query(models.IELTSAttempt)
                .filter(models.IELTSAttempt.user_id == current_user.id,
                        models.IELTSAttempt.test_id == test_id,
                        models.IELTSAttempt.status == "in_progress")
                .first())
    if existing:
        return {"attempt_id": existing.id, "test": test}

    attempt = models.IELTSAttempt(user_id=current_user.id, test_id=test_id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return {"attempt_id": attempt.id, "test": test}


# ── Save one answer (auto-save, called on every change) ───────────────────────

@app.put("/ielts/attempt/{attempt_id}/answer")
def save_ielts_answer(
    attempt_id: int,
    payload: schemas.SaveAnswerIn,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = (db.query(models.IELTSAttempt)
               .filter(models.IELTSAttempt.id == attempt_id,
                       models.IELTSAttempt.user_id == current_user.id)
               .first())
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.status != "in_progress":
        raise HTTPException(status_code=400, detail="Attempt already submitted")

    sa = (db.query(models.IELTSStudentAnswer)
          .filter(models.IELTSStudentAnswer.attempt_id == attempt_id,
                  models.IELTSStudentAnswer.question_id == payload.question_id)
          .first())

    if sa:
        if payload.answer_value is not None:
            sa.answer_value = payload.answer_value
            sa.answered_at = datetime.now(timezone.utc)
        if payload.is_flagged is not None:
            sa.is_flagged = payload.is_flagged
    else:
        db.add(models.IELTSStudentAnswer(
            attempt_id=attempt_id,
            question_id=payload.question_id,
            answer_value=payload.answer_value,
            is_flagged=payload.is_flagged or False,
            answered_at=datetime.now(timezone.utc) if payload.answer_value else None,
        ))

    db.commit()
    return {"ok": True}


# ── Get saved answers (for resuming a test) ───────────────────────────────────

@app.get("/ielts/attempt/{attempt_id}/answers")
def get_ielts_answers(
    attempt_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = (db.query(models.IELTSAttempt)
               .filter(models.IELTSAttempt.id == attempt_id,
                       models.IELTSAttempt.user_id == current_user.id)
               .first())
    if not attempt:
        raise HTTPException(status_code=404, detail="Not found")

    return [
        {"question_id": sa.question_id, "answer_value": sa.answer_value,
         "is_flagged": sa.is_flagged}
        for sa in attempt.answers
    ]


# ── Submit the attempt and calculate score ────────────────────────────────────

@app.post("/ielts/attempt/{attempt_id}/submit", response_model=schemas.SubmitAttemptOut)
def submit_ielts_attempt(
    attempt_id: int,
    time_spent: int = Body(0, embed=True),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = (db.query(models.IELTSAttempt)
               .filter(models.IELTSAttempt.id == attempt_id,
                       models.IELTSAttempt.user_id == current_user.id)
               .first())
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    if attempt.status != "in_progress":
        raise HTTPException(status_code=400, detail="Already submitted")

    # Flatten all questions in global_number order
    all_questions = []
    for passage in attempt.test.passages:
        for group in passage.question_groups:
            for q in group.questions:
                all_questions.append(q)
    all_questions.sort(key=lambda q: q.global_number)

    # Index student answers by question_id
    saved = {sa.question_id: sa.answer_value for sa in attempt.answers}

    raw = 0
    per_question = []
    for q in all_questions:
        student_ans = saved.get(q.id)
        variants = q.answer_variants if q.answer_variants else []
        is_correct = _check_answer(student_ans, q.correct_answer, variants)
        if is_correct:
            raw += 1
        per_question.append(schemas.PerQuestionResult(
            question_id=q.id,
            global_number=q.global_number,
            correct=is_correct,
            student_answer=student_ans,
            correct_answer=q.correct_answer,
        ))

    band = _raw_to_band(raw, attempt.test.component)

    attempt.status = "submitted"
    attempt.submitted_at = datetime.now(timezone.utc)
    attempt.time_spent = time_spent
    attempt.raw_score = raw
    attempt.band_score = band
    db.commit()

    return schemas.SubmitAttemptOut(
        attempt_id=attempt_id,
        raw_score=raw,
        total_questions=len(all_questions),
        band_score=band,
        time_spent=time_spent,
        per_question=per_question,
    )


# ── Get result of a submitted attempt ─────────────────────────────────────────

@app.get("/ielts/attempt/{attempt_id}/result")
def get_ielts_result(
    attempt_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempt = (db.query(models.IELTSAttempt)
               .filter(models.IELTSAttempt.id == attempt_id,
                       models.IELTSAttempt.user_id == current_user.id)
               .first())
    if not attempt or attempt.status != "submitted":
        raise HTTPException(status_code=404, detail="No submitted result found")

    return {
        "attempt_id":  attempt_id,
        "test_title":  attempt.test.title,
        "raw_score":   attempt.raw_score,
        "total":       sum(len(g.questions) for p in attempt.test.passages for g in p.question_groups),
        "band_score":  attempt.band_score,
        "time_spent":  attempt.time_spent,
        "submitted_at": attempt.submitted_at.isoformat(),
    }


# ── Admin: create an IELTS test (teacher-only, populates DB) ──────────────────

@app.post("/ielts/admin/create-test", status_code=201)
def create_ielts_test(
    payload: schemas.IELTSTestIn,
    current_user: models.User = Depends(get_teacher_user),
    db: Session = Depends(get_db),
):
    test = models.IELTSTest(
        title=payload.title,
        test_type=payload.test_type,
        component=payload.component,
        time_limit=payload.time_limit,
        created_by=current_user.id,
    )
    db.add(test)
    db.flush()

    global_num = 1
    for p_data in payload.passages:
        passage = models.IELTSPassage(
            test_id=test.id, order=p_data.order,
            title=p_data.title, body_text=p_data.body_text,
            image_url=p_data.image_url,
        )
        db.add(passage)
        db.flush()

        for g_data in p_data.question_groups:
            group = models.IELTSQuestionGroup(
                passage_id=passage.id, order=g_data.order,
                question_type=g_data.question_type,
                instruction=g_data.instruction,
                word_limit=g_data.word_limit,
                options_pool=g_data.options_pool,
            )
            db.add(group)
            db.flush()

            for q_data in g_data.questions:
                db.add(models.IELTSQuestion(
                    group_id=group.id,
                    global_number=global_num,
                    local_order=q_data.local_order,
                    stem=q_data.stem,
                    options=q_data.options,
                    correct_answer=q_data.correct_answer,
                    answer_variants=q_data.answer_variants,
                ))
                global_num += 1

    db.commit()
    return {"id": test.id, "title": test.title, "total_questions": global_num - 1}


# ── IELTS: next unseen test ────────────────────────────────────────────────────

@app.get("/ielts/next-test")
def ielts_next_test(
    component: str = "reading",
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return the test the student hasn't attempted, or attempted least recently."""
    tests = (
        db.query(models.IELTSTest)
        .filter(models.IELTSTest.component == component, models.IELTSTest.is_active == True)
        .all()
    )
    if not tests:
        raise HTTPException(status_code=404, detail="No active tests found")

    # Build map: test_id → latest submitted_at (None if never attempted)
    submitted_attempts = (
        db.query(models.IELTSAttempt)
        .filter(
            models.IELTSAttempt.user_id == current_user.id,
            models.IELTSAttempt.status == "submitted",
        )
        .all()
    )
    last_done: dict = {}
    for a in submitted_attempts:
        prev = last_done.get(a.test_id)
        if prev is None or a.submitted_at > prev:
            last_done[a.test_id] = a.submitted_at

    # Prefer tests never attempted; among attempted pick oldest submission
    never = [t for t in tests if t.id not in last_done]
    if never:
        chosen = random.choice(never)
    else:
        chosen = min(tests, key=lambda t: last_done[t.id])

    total_q = (
        db.query(models.IELTSQuestion)
        .join(models.IELTSQuestionGroup)
        .join(models.IELTSPassage)
        .filter(models.IELTSPassage.test_id == chosen.id)
        .count()
    )
    return {
        "id": chosen.id,
        "title": chosen.title,
        "test_type": chosen.test_type,
        "component": chosen.component,
        "time_limit": chosen.time_limit,
        "total_questions": total_q,
        "previously_attempted": chosen.id in last_done,
    }


# ── Writing: random prompt ─────────────────────────────────────────────────────

@app.get("/writing/random-prompt")
def writing_random_prompt(
    task: int = 2,
    test_type: str = "academic",
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return a random active writing prompt for the given task (1 or 2) and test_type."""
    if task not in (1, 2):
        raise HTTPException(status_code=422, detail="task must be 1 or 2")
    prompts = (
        db.query(models.WritingPrompt)
        .filter(
            models.WritingPrompt.task == task,
            models.WritingPrompt.test_type == test_type,
            models.WritingPrompt.is_active == True,
        )
        .all()
    )
    if not prompts:
        raise HTTPException(status_code=404, detail="No prompts found for this task/type")

    p = random.choice(prompts)
    return {
        "id": p.id,
        "task": p.task,
        "test_type": p.test_type,
        "topic": p.topic,
        "prompt_text": p.prompt_text,
        "image_description": p.image_description,
        "min_words": p.min_words,
    }


# ── Admin: manual re-seed ──────────────────────────────────────────────────────

@app.post("/admin/seed")
def admin_seed(
    force: bool = False,
    current_user: models.User = Depends(get_teacher_user),
    db: Session = Depends(get_db),
):
    """Manually trigger IELTS content seeder. Use force=true to wipe and re-seed."""
    if force:
        db.query(models.IELTSStudentAnswer).delete()
        db.query(models.IELTSAttempt).delete()
        db.query(models.IELTSQuestion).delete()
        db.query(models.IELTSQuestionGroup).delete()
        db.query(models.IELTSPassage).delete()
        db.query(models.IELTSTest).delete()
        db.query(models.WritingPrompt).delete()
        db.commit()
    result = seed_ielts_content(db)
    return {"ok": True, **result}

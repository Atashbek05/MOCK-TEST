"""
Telegram bot — simple long-polling.

This file is the ONLY place the bot lives.
It runs in a background daemon thread started from main.py startup_event.

Why polling instead of webhook?
  Telegram sends updates to ONE destination — either a webhook URL or getUpdates.
  On Render free tier the server sleeps between requests, making webhook delivery
  unreliable. Polling works regardless: the thread asks Telegram for new messages
  every 30 seconds and processes them immediately.

Features:
  - Account linking/auth (/link, /login, /status)
  - Progress & scores (/progress, /latestscore)
  - AI-powered test review (/review) — shows wrong answers + AI coach advice
  - Test completion notifications sent from main.py after each submission
"""

import json as _json
import os
import threading
import time
from datetime import datetime
from typing import Optional

import requests

from . import models
from .database import SessionLocal

# ── Config ────────────────────────────────────────────────────────────────────
TOKEN:   str = os.getenv("TELEGRAM_BOT_TOKEN", "")
APP_URL: str = os.getenv("FRONTEND_URL", "https://atashasd.vercel.app")
API:     str = f"https://api.telegram.org/bot{TOKEN}"


# ── Send a message ─────────────────────────────────────────────────────────────
def _send(chat_id: int, text: str, keyboard: Optional[dict] = None,
          parse_mode: str = "Markdown") -> None:
    payload: dict = {
        "chat_id":    chat_id,
        "text":       text,
        "parse_mode": parse_mode,
    }
    if keyboard:
        payload["reply_markup"] = keyboard
    try:
        requests.post(f"{API}/sendMessage", json=payload, timeout=10)
    except Exception:
        pass


def _tg_answer_callback(callback_query_id: str) -> None:
    try:
        requests.post(
            f"{API}/answerCallbackQuery",
            json={"callback_query_id": callback_query_id},
            timeout=5,
        )
    except Exception:
        pass


# ── Bot command handlers ───────────────────────────────────────────────────────

def _cmd_start(chat_id: int, first_name: str) -> None:
    welcome = (
        f"👋 Hello, <b>{first_name}</b>!\n\n"
        "🎯 <b>IELTS Mock Test Platform</b>\n\n"
        "Practice Reading, Listening and Writing\n"
        "with AI-powered feedback.\n\n"
        "📌 <b>Commands:</b>\n"
        "/review — AI review of your last test\n"
        "/progress — Your stats\n"
        "/latestscore — Last test result\n"
        "/link — Link your account\n\n"
        "Tap the button below to open the platform 👇"
    )
    keyboard = {
        "inline_keyboard": [
            [{"text": "🚀 Open Dashboard", "url": f"{APP_URL}/dashboard.html"}],
            [{"text": "🔗 Link Account", "url": f"{APP_URL}/telegram-connect.html"}],
        ]
    }
    try:
        requests.post(f"{API}/sendMessage", json={
            "chat_id": chat_id, "text": welcome,
            "parse_mode": "HTML", "reply_markup": keyboard,
        }, timeout=10)
    except Exception:
        pass


def _cmd_help(chat_id: int) -> None:
    _send(chat_id, (
        "📚 *Commands:*\n\n"
        "/review — AI review of your last test with mistakes & tips\n"
        "/progress — Your band stats\n"
        "/latestscore — Latest test result\n"
        "/link — Link Telegram to your account\n"
        "/login — Log in via Telegram (recovery)\n"
        "/status — Check account link status\n"
        "/start — Main menu\n"
        "/help — This list"
    ))


def _cmd_link(chat_id: int) -> None:
    """No code provided — show instructions on how to get a code from the website."""
    keyboard = {"inline_keyboard": [[
        {"text": "🔗 Get Verification Code", "url": f"{APP_URL}/telegram-connect.html"}
    ]]}
    _send(chat_id, (
        "To link your Telegram with your IELTS account:\n\n"
        "1️⃣ Open the platform and go to *Telegram Connect*\n"
        "2️⃣ Get your 6-digit verification code\n"
        "3️⃣ Send it here: `/link 123456`\n\n"
        "Tap the button to get your code 👇"
    ), keyboard)


def _cmd_link_code(chat_id: int, tg_id: int, code: str,
                   tg_username: Optional[str]) -> None:
    """
    User sent /link 123456 — verify the code in DB and link their account.
    Security checks:
      • code must exist and be unused
      • code must not be expired (10-minute window)
      • this Telegram ID must not already be linked to a different account
    """
    db = SessionLocal()
    try:
        vc = (db.query(models.TelegramVerificationCode)
              .filter(models.TelegramVerificationCode.code == code)
              .first())

        if not vc:
            _send(chat_id, "❌ Invalid code. Generate a new one on the platform.")
            return

        if vc.used:
            _send(chat_id, "❌ This code was already used. Generate a new one.")
            return

        # Compare expiry — DB stores naive UTC; handle both cases
        expires = vc.expires_at
        if expires.tzinfo is not None:
            expires = expires.replace(tzinfo=None)
        if datetime.utcnow() > expires:
            _send(chat_id, "❌ Code expired (10-minute limit). Generate a new one.")
            return

        # Conflict: this Telegram account linked to a *different* platform account
        conflict = (db.query(models.User)
                    .filter(models.User.telegram_id == tg_id,
                            models.User.id != vc.user_id)
                    .first())
        if conflict:
            _send(chat_id,
                  "❌ This Telegram is already linked to a different account.\n"
                  "Unlink it first from that account.")
            return

        user = db.query(models.User).filter(models.User.id == vc.user_id).first()
        if not user:
            _send(chat_id, "❌ Account not found. Please try again.")
            return

        # All good — link!
        user.telegram_id       = tg_id
        user.telegram_username = tg_username
        vc.used                = True
        db.commit()

        keyboard = {"inline_keyboard": [[
            {"text": "🚀 Open Dashboard", "url": f"{APP_URL}/dashboard.html"}
        ]]}
        _send(chat_id, (
            f"✅ *Successfully linked!*\n\n"
            f"Account: *{user.name}* ({user.email})\n\n"
            f"You'll now receive:\n"
            f"• 📊 Test results after each submission\n"
            f"• 🧠 AI review of your mistakes (/review)\n"
        ), keyboard)
    finally:
        db.close()


def _cmd_login_code(chat_id: int, tg_id: int, code: str,
                    tg_username: Optional[str]) -> None:
    """
    User sent /login 123456 — find their account by telegram_id,
    mark the login code as verified, set user_id.
    Security checks:
      • code must exist, be unused and unverified
      • code must not be expired (5-minute window)
      • this Telegram ID must already be linked to a platform account
    """
    db = SessionLocal()
    try:
        lc = (db.query(models.TelegramLoginCode)
              .filter(models.TelegramLoginCode.code == code)
              .first())

        if not lc:
            _send(chat_id, "❌ Invalid code. Generate a new one on the login page.")
            return

        if lc.used:
            _send(chat_id, "❌ This code was already used. Generate a new one.")
            return

        if lc.verified:
            _send(chat_id, "❌ This code was already verified. Generate a new one.")
            return

        expires = lc.expires_at
        if expires.tzinfo is not None:
            expires = expires.replace(tzinfo=None)
        if datetime.utcnow() > expires:
            _send(chat_id, "❌ Code expired (5-minute limit). Generate a new one.")
            return

        user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
        if not user:
            _send(chat_id, (
                "❌ No account linked to this Telegram.\n\n"
                "First link your account: /link\n"
                "Or log in with email/password and connect Telegram from the dashboard."
            ))
            return

        lc.user_id  = user.id
        lc.verified = True
        db.commit()

        keyboard = {"inline_keyboard": [[
            {"text": "🚀 Open Dashboard", "url": f"{APP_URL}/dashboard.html"}
        ]]}
        _send(chat_id, (
            f"✅ *Login verified!*\n\n"
            f"Welcome back, *{user.name}*!\n\n"
            f"Switch back to the browser — you'll be logged in automatically."
        ), keyboard)
    finally:
        db.close()


def _cmd_status(chat_id: int, tg_id: int) -> None:
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
        if user:
            _send(chat_id, f"✅ Linked to account *{user.name}* ({user.email})")
        else:
            _send(chat_id, "❌ Not linked yet. Use /link to connect your account.")
    finally:
        db.close()


def _cmd_progress(chat_id: int, tg_id: int) -> None:
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
        if not user:
            _send(chat_id, "❌ Account not linked. Use /link first.")
            return

        results = (db.query(models.TeacherTestResult)
                   .filter(models.TeacherTestResult.student_id == user.id)
                   .order_by(models.TeacherTestResult.created_at.desc())
                   .limit(10).all())
        writing = (db.query(models.WritingResult)
                   .filter(models.WritingResult.user_id == user.id)
                   .order_by(models.WritingResult.created_at.desc())
                   .first())

        if not results and not writing:
            _send(chat_id, "📊 No results yet.\n\nAsk your teacher for a test PIN to get started.")
            return

        text = f"📊 *Progress — {user.name}*\n\n"
        if results:
            bands = [r.band for r in results]
            text += f"🎯 Best band: *{max(bands)}*\n"
            text += f"📈 Average: *{round(sum(bands)/len(bands), 1)}*\n"
            text += f"📝 Attempts: *{len(results)}*\n"
        if writing:
            text += f"\n✏️ Last Writing: *{writing.band_score}* band\n"
        text += f"\n[Open Dashboard]({APP_URL}/dashboard.html)"
        _send(chat_id, text)
    finally:
        db.close()


def _cmd_latestscore(chat_id: int, tg_id: int) -> None:
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
        if not user:
            _send(chat_id, "❌ Account not linked. Use /link first.")
            return

        r = (db.query(models.TeacherTestResult)
             .filter(models.TeacherTestResult.student_id == user.id)
             .order_by(models.TeacherTestResult.created_at.desc())
             .first())
        if not r:
            _send(chat_id, "❌ No results yet. Ask your teacher for a test PIN.")
            return

        test = db.query(models.TeacherTest).filter(models.TeacherTest.id == r.test_id).first()
        test_name = test.title if test else f"Test #{r.test_id}"
        _send(chat_id, (
            f"🏆 *Latest Result*\n\n"
            f"📝 {test_name}\n"
            f"🎯 Band: *{r.band}*\n"
            f"✔️ {r.correct}/{r.total} correct\n"
            f"📅 {r.created_at.strftime('%d.%m.%Y')}\n\n"
            f"Type /review for a detailed AI breakdown of your mistakes."
        ))
    finally:
        db.close()


# ── AI Coach helpers ───────────────────────────────────────────────────────────

def _coach_fallback(band: float, correct: int, total: int) -> dict:
    wrong = total - correct
    if band >= 7.0:
        tips = [
            "Review your missed questions carefully for patterns.",
            "Practice skimming/scanning techniques.",
            "Expand academic vocabulary with daily word lists.",
        ]
        encouragement = "You're almost there — keep pushing!"
    elif band >= 5.5:
        tips = [
            "Re-read passages for wrong answers and find where you misunderstood.",
            "Practice paraphrasing — IELTS answers are often paraphrased.",
            "Study 10 new academic words every day.",
        ]
        encouragement = "Solid progress — consistent practice will raise your band!"
    else:
        tips = [
            "Start with shorter passages to build confidence.",
            "Master question types (TFNG, MCQ) and their strategies.",
            "Review grammar basics to understand complex sentences.",
        ]
        encouragement = "Every mistake is a lesson — you're building your foundation!"
    return {
        "summary": f"Band {band}: {correct}/{total} correct, {wrong} mistake(s).",
        "weak_areas": ["Reading comprehension", "Vocabulary"],
        "tips": tips,
        "encouragement": encouragement,
    }


def _get_coach_advice(band: float, correct: int, total: int,
                      wrong_questions: list, test_title: str) -> dict:
    """Return AI coaching dict. Falls back to rule-based if no API key or no wrong questions."""
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key or not wrong_questions:
        return _coach_fallback(band, correct, total)

    wrong_text = "\n".join(
        f"  Q{i+1}: {q['question_text'][:120]} (Correct: {q['correct_answer']})"
        for i, q in enumerate(wrong_questions[:8])
    )
    prompt = (
        f"You are an expert IELTS tutor. Student scored Band {band} ({correct}/{total}) "
        f"on '{test_title}'.\n\n"
        f"Wrong questions:\n{wrong_text}\n\n"
        "Return ONLY valid JSON:\n"
        '{"summary":"...","weak_areas":["..."],"tips":["...","...","..."],"encouragement":"..."}'
    )
    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "IELTS tutor. Reply only with valid JSON."},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 600,
                "temperature": 0.4,
                "response_format": {"type": "json_object"},
            },
            timeout=20,
        )
        return _json.loads(resp.json()["choices"][0]["message"]["content"])
    except Exception:
        return _coach_fallback(band, correct, total)


# ── /review command ────────────────────────────────────────────────────────────

def _cmd_review(chat_id: int, tg_id: int) -> None:
    """Send 2 messages: (1) score + wrong answers, (2) AI coach advice."""
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
        if not user:
            _send(chat_id, "❌ Account not linked. Use /link first.")
            return

        r = (db.query(models.TeacherTestResult)
             .filter(models.TeacherTestResult.student_id == user.id)
             .order_by(models.TeacherTestResult.created_at.desc())
             .first())
        if not r:
            _send(chat_id, "❌ No test results yet.\n\nAsk your teacher for a test PIN and complete it first.")
            return

        test = db.query(models.TeacherTest).filter(models.TeacherTest.id == r.test_id).first()
        test_title = test.title if test else f"Test #{r.test_id}"
        date_str = r.created_at.strftime("%d.%m.%Y")

        # Build wrong questions list
        wrong_questions = []
        if r.wrong_question_ids and test:
            all_q = {q.id: q for p in test.passages for q in p.questions}
            for qid in r.wrong_question_ids:
                q = all_q.get(qid)
                if q:
                    opt_text = getattr(q, f"option_{q.correct_answer.lower()}", "")
                    wrong_questions.append({
                        "question_text": q.question_text,
                        "correct_answer": q.correct_answer,
                        "correct_option_text": opt_text,
                    })

        # ── Message 1: Score + wrong answers ──────────────────────────────────
        msg1 = (
            f"📋 *Test Review*\n"
            f"📝 {test_title}\n"
            f"📅 {date_str}\n"
            f"🎯 Band: *{r.band}*  |  ✅ {r.correct}/{r.total}  |  ❌ {r.total - r.correct} mistakes\n"
        )
        if wrong_questions:
            shown = wrong_questions[:10]
            msg1 += "\n❌ *Your mistakes:*\n\n"
            for i, q in enumerate(shown):
                qt = q["question_text"]
                qt = qt[:120] + "…" if len(qt) > 120 else qt
                ot = q["correct_option_text"]
                ot = ot[:80] + "…" if len(ot) > 80 else ot
                msg1 += f"*{i+1}.* {qt}\n   ✅ {q['correct_answer']}: {ot}\n\n"
            if len(wrong_questions) > 10:
                msg1 += f"_…and {len(wrong_questions) - 10} more mistakes_\n"
        elif r.wrong_question_ids is None:
            msg1 += "\n_Detailed question breakdown available for tests taken after this update._\n"
        else:
            msg1 += "\n✨ *No mistakes — perfect score!*\n"

        _send(chat_id, msg1)

        # ── Message 2: AI Coach ────────────────────────────────────────────────
        advice = _get_coach_advice(r.band, r.correct, r.total, wrong_questions, test_title)
        msg2 = f"🧠 *AI Coach*\n\n📌 {advice['summary']}\n\n"
        if advice.get("weak_areas"):
            msg2 += f"⚠️ *Weak areas:* {', '.join(advice['weak_areas'])}\n\n"
        msg2 += "💡 *Tips:*\n"
        for tip in advice.get("tips", [])[:3]:
            msg2 += f"→ {tip}\n"
        msg2 += f"\n💪 {advice.get('encouragement', '')}"
        _send(chat_id, msg2)
    finally:
        db.close()


def _cmd_test_list(chat_id: int, tg_id: int) -> None:
    """Send the user an inline keyboard listing their last 5 test results."""
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
        if not user:
            _send(chat_id, "❌ Account not linked\\. Use /link first\\.")
            return

        results = (
            db.query(models.TeacherTestResult)
            .filter(models.TeacherTestResult.student_id == user.id)
            .order_by(models.TeacherTestResult.created_at.desc())
            .limit(5)
            .all()
        )

        if not results:
            _send(chat_id, (
                "📭 *No tests found yet\\.* \n\n"
                "Ask your teacher for a test PIN, complete the test, then come back here\\."
            ))
            return

        rows = []
        for r in results:
            test = db.query(models.TeacherTest).filter(models.TeacherTest.id == r.test_id).first()
            title = test.title if test else f"Test #{r.test_id}"
            short = (title[:25] + "…") if len(title) > 25 else title
            date_str = r.created_at.strftime("%d.%m.%y")
            btn_text = f"{short} | Band {r.band} | {date_str}"
            rows.append([{"text": btn_text, "callback_data": f"rev_{r.id}"}])

        _send(chat_id, "📋 *Выберите тест для разбора:*", {"inline_keyboard": rows})
    finally:
        db.close()


def _cmd_review_by_id(chat_id: int, tg_id: int, result_id: int) -> None:
    """Send a full review for a specific test result (ownership-checked)."""
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.telegram_id == tg_id).first()
        if not user:
            _send(chat_id, "❌ Account not linked\\. Use /link first\\.")
            return

        r = db.query(models.TeacherTestResult).filter(
            models.TeacherTestResult.id == result_id
        ).first()

        if not r or r.student_id != user.id:
            _send(chat_id, "❌ Test not found or access denied\\.")
            return

        test = db.query(models.TeacherTest).filter(models.TeacherTest.id == r.test_id).first()
        test_title = test.title if test else f"Test #{r.test_id}"
        date_str = r.created_at.strftime("%d.%m.%Y")

        wrong_questions: list[dict] = []
        if r.wrong_question_ids and test:
            all_q = {q.id: q for p in test.passages for q in p.questions}
            for qid in r.wrong_question_ids:
                q = all_q.get(qid)
                if q:
                    opt_text = getattr(q, f"option_{q.correct_answer.lower()}", "") or ""
                    wrong_questions.append({
                        "question_text": q.question_text,
                        "correct_answer": q.correct_answer,
                        "correct_option_text": opt_text,
                    })

        mistakes = r.total - r.correct
        msg1 = (
            f"📋 *Test Review*\n"
            f"📝 {test_title}\n"
            f"📅 {date_str}\n"
            f"🎯 Band: *{r.band}*  |  ✅ {r.correct}/{r.total}  |  ❌ {mistakes} mistakes\n"
        )
        if wrong_questions:
            shown = wrong_questions[:10]
            msg1 += "\n❌ *Your mistakes:*\n\n"
            for i, q in enumerate(shown, 1):
                qt = q["question_text"]
                qt = (qt[:120] + "…") if len(qt) > 120 else qt
                ot = q["correct_option_text"]
                ot = (ot[:80] + "…") if len(ot) > 80 else ot
                msg1 += f"*{i}.* {qt}\n   ✅ {q['correct_answer']}: {ot}\n\n"
            if len(wrong_questions) > 10:
                msg1 += f"_…and {len(wrong_questions) - 10} more mistakes_\n"
        elif not r.wrong_question_ids:
            msg1 += "\n✨ *No mistakes — perfect score!*\n"

        _send(chat_id, msg1)

        advice = _get_coach_advice(r.band, r.correct, r.total, wrong_questions, test_title)
        msg2 = f"🧠 *AI Coach*\n\n📌 {advice['summary']}\n\n"
        if advice.get("weak_areas"):
            msg2 += f"⚠️ *Weak areas:* {', '.join(advice['weak_areas'])}\n\n"
        msg2 += "💡 *Tips:*\n"
        for tip in advice.get("tips", [])[:3]:
            msg2 += f"→ {tip}\n"
        msg2 += f"\n💪 {advice.get('encouragement', '')}"
        _send(chat_id, msg2)
    finally:
        db.close()


# ── Handle one Telegram update ────────────────────────────────────────────────
def _handle(update: dict) -> None:
    # ── Inline button callbacks ────────────────────────────────────────────────
    cq = update.get("callback_query")
    if cq:
        _tg_answer_callback(cq.get("id"))
        cq_data  = cq.get("data", "")
        cq_chat  = cq.get("message", {}).get("chat", {}).get("id")
        cq_tg_id = cq.get("from", {}).get("id")
        if cq_data.startswith("rev_") and cq_chat and cq_tg_id:
            try:
                result_id = int(cq_data[4:])
            except ValueError:
                return
            _cmd_review_by_id(cq_chat, cq_tg_id, result_id)
        return

    # ── Regular text message ───────────────────────────────────────────────────
    message  = update.get("message", {})
    text     = message.get("text", "")
    chat_id  = message.get("chat", {}).get("id")
    from_obj = message.get("from", {})

    if not chat_id:
        return

    first_name = from_obj.get("first_name", "Student")
    tg_id      = from_obj.get("id")

    if text.startswith("/start"):
        parts = text.split(None, 1)
        param = parts[1] if len(parts) > 1 else ""
        if param == "myreviews" and tg_id:
            _cmd_test_list(chat_id, tg_id)
        else:
            _cmd_start(chat_id, first_name)
    elif text == "/help":
        _cmd_help(chat_id)
    elif text.startswith("/link"):
        # /link       → show instructions
        # /link 123456 → verify code and link account
        parts = text.split()
        if (len(parts) == 2 and parts[1].isdigit()
                and len(parts[1]) == 6 and tg_id):
            _cmd_link_code(chat_id, tg_id, parts[1], from_obj.get("username"))
        else:
            _cmd_link(chat_id)
    elif text.startswith("/login"):
        # /login       → show instructions
        # /login 123456 → verify login code
        parts = text.split()
        if (len(parts) == 2 and parts[1].isdigit()
                and len(parts[1]) == 6 and tg_id):
            _cmd_login_code(chat_id, tg_id, parts[1], from_obj.get("username"))
        else:
            keyboard = {"inline_keyboard": [[
                {"text": "🔐 Get Login Code", "url": f"{APP_URL}/login.html"}
            ]]}
            _send(chat_id, (
                "To log in via Telegram:\n\n"
                "1️⃣ Go to the login page\n"
                "2️⃣ Click *Sign in with Telegram*\n"
                "3️⃣ Send the 6-digit code here: `/login 123456`\n\n"
                "Your Telegram must already be linked to an account.\n"
                "Tap the button to open the login page 👇"
            ), keyboard)
    elif text == "/status" and tg_id:
        _cmd_status(chat_id, tg_id)
    elif text == "/progress" and tg_id:
        _cmd_progress(chat_id, tg_id)
    elif text == "/latestscore" and tg_id:
        _cmd_latestscore(chat_id, tg_id)
    elif text == "/review" and tg_id:
        _cmd_review(chat_id, tg_id)


# ── Polling loop (runs forever in a daemon thread) ────────────────────────────
def _poll() -> None:
    offset = 0

    while True:
        try:
            res = requests.get(
                f"{API}/getUpdates",
                params={
                    "timeout": 30,
                    "offset": offset,
                    "allowed_updates": '["message","callback_query"]',
                },
                timeout=35,
            )
            data = res.json()
            if data.get("ok"):
                for update in data.get("result", []):
                    offset = update["update_id"] + 1
                    _handle(update)
        except Exception:
            time.sleep(5)


# ── Public entry point — called once from main.py startup_event ───────────────
def start_polling() -> None:
    """
    1. Delete any registered webhook (required — polling and webhook are mutually exclusive).
    2. Start the polling loop in a daemon thread so it doesn't block the server.
    """
    if not TOKEN:
        return   # TELEGRAM_BOT_TOKEN not set — skip silently

    try:
        requests.post(
            f"{API}/deleteWebhook",
            json={"drop_pending_updates": True},
            timeout=10,
        )
    except Exception:
        pass

    thread = threading.Thread(target=_poll, daemon=True, name="telegram-bot")
    thread.start()

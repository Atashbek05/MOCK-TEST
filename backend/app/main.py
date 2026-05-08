from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, SessionLocal, engine, get_db
from .security import create_access_token, decode_access_token, hash_password, verify_password

app = FastAPI(title="IELTS Mock Test API", version="0.1.0")
security = HTTPBearer()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://atashasd.vercel.app",
    "https://mock-test-puce-iota.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


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


@app.on_event("startup")
async def startup_event():
    db = SessionLocal()
    try:
        _seed_questions(db)
    finally:
        db.close()


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

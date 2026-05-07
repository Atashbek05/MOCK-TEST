from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db
from .security import create_access_token, decode_access_token, hash_password, verify_password

app = FastAPI(title="IELTS Mock Test API", version="0.1.0")
security = HTTPBearer()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "https://mock-test-1-vz7c.onrender.com",
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

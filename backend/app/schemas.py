from datetime import datetime
from typing import List

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class ResultCreate(BaseModel):
    reading_score: float = Field(..., ge=0, le=9)
    listening_score: float = Field(..., ge=0, le=9)
    writing_score: float = Field(..., ge=0, le=9)
    overall: float = Field(..., ge=0, le=9)


class ResultOut(BaseModel):
    id: int
    reading_score: float
    listening_score: float
    writing_score: float
    overall: float
    created_at: datetime

    class Config:
        orm_mode = True


class DashboardOut(BaseModel):
    user: UserOut
    level: str
    latest_results: List[ResultOut]


# ── Reading test schemas ──────────────────────────────────────────────────────

class QuestionOut(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        orm_mode = True


class TestOut(BaseModel):
    id: int
    type: str
    passage: str
    questions: List[QuestionOut]

    class Config:
        orm_mode = True


class SubmitTestIn(BaseModel):
    test_id: int
    answers: dict  # {"<question_id>": "A"/"B"/"C"/"D", ...}


class SubmitResultOut(BaseModel):
    correct: int
    total: int
    band: float

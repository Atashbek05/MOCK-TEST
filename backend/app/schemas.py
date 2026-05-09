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


# ── Writing module schemas ────────────────────────────────────────────────────

class SubmitWritingIn(BaseModel):
    essay: str = Field(..., min_length=50, max_length=6000)


class WritingSubmitOut(BaseModel):
    id: int
    band_score: float
    word_count: int
    feedback: str       # JSON string — frontend will JSON.parse() this
    created_at: datetime

    class Config:
        orm_mode = True


class WritingHistoryItemOut(BaseModel):
    id: int
    band_score: float
    word_count: int
    created_at: datetime

    class Config:
        orm_mode = True


# ── Multiple Reading Tests schemas ───────────────────────────────────────────

class ReadingQuestionOut(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        orm_mode = True


class ReadingPassageOut(BaseModel):
    id: int
    order: int
    title: str
    text: str
    questions: List[ReadingQuestionOut]

    class Config:
        orm_mode = True


class ReadingTestOut(BaseModel):
    id: int
    title: str
    passages: List[ReadingPassageOut]

    class Config:
        orm_mode = True


class ReadingTestListItem(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class SubmitReadingIn(BaseModel):
    test_id: int
    answers: dict   # {"<question_id>": "A"/"B"/"C"/"D"}


class ReadingResultOut(BaseModel):
    correct: int
    total: int
    band: float


# ── Exam Session schemas ──────────────────────────────────────────────────────

class ExamSessionCreate(BaseModel):
    reading_band: float = Field(..., ge=0, le=9)
    listening_band: float = Field(..., ge=0, le=9)
    writing_band: float = Field(..., ge=0, le=9)
    overall_band: float = Field(..., ge=0, le=9)
    duration_minutes: int = Field(0, ge=0)


class ExamSessionOut(BaseModel):
    id: int
    reading_band: float
    listening_band: float
    writing_band: float
    overall_band: float
    duration_minutes: int
    created_at: datetime

    class Config:
        orm_mode = True

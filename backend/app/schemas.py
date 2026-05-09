from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    role: str = Field("student", regex="^(student|teacher)$")


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
    role: str

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


# ── Teacher Test schemas (input) ─────────────────────────────────────────────

class TeacherQuestionIn(BaseModel):
    question_text: str = Field(..., min_length=5)
    option_a: str = Field(..., min_length=1)
    option_b: str = Field(..., min_length=1)
    option_c: str = Field(..., min_length=1)
    option_d: str = Field(..., min_length=1)
    correct_answer: str = Field(..., regex="^[ABCD]$")


class TeacherPassageIn(BaseModel):
    order: int = Field(..., ge=1)
    title: str = Field(..., min_length=2)
    text: str = Field(..., min_length=20)
    questions: List[TeacherQuestionIn]


class TeacherTestIn(BaseModel):
    title: str = Field(..., min_length=3, max_length=300)
    description: str = ""
    test_type: str = "reading"
    passages: List[TeacherPassageIn]


# ── Teacher Test schemas (output) ─────────────────────────────────────────────

class TeacherQuestionOut(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str

    class Config:
        orm_mode = True


class TeacherPassageOut(BaseModel):
    id: int
    order: int
    title: str
    text: str
    questions: List[TeacherQuestionOut]

    class Config:
        orm_mode = True


class TeacherTestOut(BaseModel):
    id: int
    title: str
    description: str
    test_type: str
    pin_code: Optional[str]
    is_active: bool
    created_at: datetime
    passages: List[TeacherPassageOut]

    class Config:
        orm_mode = True


class TeacherTestSummary(BaseModel):
    id: int
    title: str
    description: str
    test_type: str
    pin_code: Optional[str]
    is_active: bool
    created_at: datetime
    passage_count: int
    question_count: int
    enrolled_count: int

    class Config:
        orm_mode = True


class JoinTestIn(BaseModel):
    pin: str = Field(..., min_length=4, max_length=10)


# ── Teacher student results ───────────────────────────────────────────────────

class TeacherStudentResult(BaseModel):
    """One student's latest result on a teacher test (with attempt count)."""
    student_id: int
    student_name: str
    student_email: str
    correct: int
    total: int
    band: float
    attempts: int
    latest_at: datetime


class TeacherResultsOverview(BaseModel):
    """Per-test summary used to populate the Students page tabs."""
    test_id: int
    test_title: str
    pin_code: Optional[str]
    is_active: bool
    enrolled_count: int
    submission_count: int
    unique_completions: int
    avg_band: float
    best_band: float
    passage_count: int
    question_count: int


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

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    role: str = Field("student", pattern="^(student|teacher)$")


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
    telegram_id: Optional[int] = None
    telegram_username: Optional[str] = None

    class Config:
        from_attributes = True


# ── Telegram Integration (Phase 6) ───────────────────────────────────────────

class TelegramAuthIn(BaseModel):
    """Data sent by Telegram Login Widget / verified by the backend."""
    id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    photo_url: Optional[str] = None
    auth_date: int
    hash: str


class TelegramMiniAppAuthIn(BaseModel):
    """Raw initData string from window.Telegram.WebApp.initData (Mini App auth)."""
    init_data: str


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
        from_attributes = True


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
        from_attributes = True


class TestOut(BaseModel):
    id: int
    type: str
    passage: str
    questions: List[QuestionOut]

    class Config:
        from_attributes = True


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
    mock_attempt_id: Optional[int] = None


class WritingSubmitOut(BaseModel):
    id: int
    band_score: float
    word_count: int
    feedback: str       # JSON string — frontend will JSON.parse() this
    created_at: datetime

    class Config:
        from_attributes = True


class WritingHistoryItemOut(BaseModel):
    id: int
    band_score: float
    word_count: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Multiple Reading Tests schemas ───────────────────────────────────────────

class ReadingQuestionOut(BaseModel):
    id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str

    class Config:
        from_attributes = True


class ReadingPassageOut(BaseModel):
    id: int
    order: int
    title: str
    text: str
    questions: List[ReadingQuestionOut]

    class Config:
        from_attributes = True


class ReadingTestOut(BaseModel):
    id: int
    title: str
    passages: List[ReadingPassageOut]

    class Config:
        from_attributes = True


class ReadingTestListItem(BaseModel):
    id: int
    title: str

    class Config:
        from_attributes = True


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
    correct_answer: str = Field(..., pattern="^[ABCD]$")


class TeacherPassageIn(BaseModel):
    order: int = Field(..., ge=1)
    title: str = Field(..., min_length=2)
    text: str = Field(..., min_length=5)
    audio_url: Optional[str] = None
    questions: List[TeacherQuestionIn] = []


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
        from_attributes = True


class TeacherPassageOut(BaseModel):
    id: int
    order: int
    title: str
    text: str
    audio_url: Optional[str] = None
    questions: List[TeacherQuestionOut]

    class Config:
        from_attributes = True


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
        from_attributes = True


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
        from_attributes = True


class TeacherWritingEssayIn(BaseModel):
    passage_id: int
    essay_text: str = Field(..., min_length=50, max_length=6000)


class TeacherWritingSubmitIn(BaseModel):
    test_id: int
    essays: List[TeacherWritingEssayIn]


class TeacherWritingTaskResult(BaseModel):
    passage_id: int
    passage_title: str
    band: float
    word_count: int
    feedback: str   # JSON string


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
        from_attributes = True


# ── Phase 5: Teacher Analytics schemas ───────────────────────────────────────

class TeacherAnalyticsSummary(BaseModel):
    total_tests: int
    unique_students: int
    total_submissions: int
    overall_avg_band: float
    overall_best_band: float
    completion_rate: float        # unique submitters / unique enrolled × 100
    total_attempts: int


class StudentAnalyticsStat(BaseModel):
    student_id: int
    student_name: str
    student_email: str
    best_band: float
    avg_band: float
    total_attempts: int
    tests_enrolled: int
    tests_completed: int          # unique tests with ≥1 submission
    last_active_at: Optional[datetime]
    is_weak: bool                 # best_band < 5.5


# ── IELTS Question Engine Schemas ─────────────────────────────────────────────

class IELTSQuestionOut(BaseModel):
    id: int
    global_number: int
    local_order: int
    stem: str
    options: Optional[list] = None
    # correct_answer intentionally omitted — never sent to student during exam

    class Config:
        from_attributes = True


class IELTSQuestionGroupOut(BaseModel):
    id: int
    order: int
    question_type: str
    instruction: str
    word_limit: Optional[int] = None
    options_pool: Optional[dict] = None
    questions: List[IELTSQuestionOut]

    class Config:
        from_attributes = True


class IELTSPassageOut(BaseModel):
    id: int
    order: int
    title: str
    body_text: str
    image_url: Optional[str] = None
    question_groups: List[IELTSQuestionGroupOut]

    class Config:
        from_attributes = True


class IELTSTestOut(BaseModel):
    id: int
    title: str
    test_type: str
    component: str
    time_limit: int
    passages: List[IELTSPassageOut]

    class Config:
        from_attributes = True


class IELTSTestListItem(BaseModel):
    id: int
    title: str
    test_type: str
    component: str
    time_limit: int
    best_band: Optional[float] = None
    attempt_count: Optional[int] = None

    class Config:
        from_attributes = True


class StartAttemptOut(BaseModel):
    attempt_id: int
    test: IELTSTestOut


class SaveAnswerIn(BaseModel):
    question_id: int
    answer_value: Optional[str] = None
    is_flagged: Optional[bool] = None


class PerQuestionResult(BaseModel):
    question_id: int
    global_number: int
    correct: bool
    student_answer: Optional[str]
    correct_answer: str


class SubmitAttemptOut(BaseModel):
    attempt_id: int
    raw_score: int
    total_questions: int
    band_score: float
    time_spent: int
    per_question: List[PerQuestionResult]


# ── IELTS Admin / Teacher Test Creation Schemas ───────────────────────────────

class IELTSQuestionIn(BaseModel):
    local_order: int
    stem: str
    options: Optional[list] = None
    correct_answer: str
    answer_variants: Optional[list] = None


class IELTSQuestionGroupIn(BaseModel):
    order: int
    question_type: str
    instruction: str
    word_limit: Optional[int] = None
    options_pool: Optional[dict] = None
    questions: List[IELTSQuestionIn]


class IELTSPassageIn(BaseModel):
    order: int
    title: str
    body_text: str
    image_url: Optional[str] = None
    question_groups: List[IELTSQuestionGroupIn]


class IELTSTestIn(BaseModel):
    title: str
    test_type: str = "academic"
    component: str = "reading"
    time_limit: int = 60
    passages: List[IELTSPassageIn]


# ── Full Mock Test schemas ────────────────────────────────────────────────────

class ListeningQuestionOut(BaseModel):
    id: int
    global_number: int
    local_order: int
    question_type: str
    stem: str
    options: Optional[Any] = None
    group_instruction: Optional[str] = None
    map_image_url: Optional[str] = None

    class Config:
        from_attributes = True


class ListeningPartOut(BaseModel):
    id: int
    part_number: int
    context_description: Optional[str] = None
    audio_url: Optional[str] = None
    questions: List[ListeningQuestionOut] = []

    class Config:
        from_attributes = True


class ListeningSectionOut(BaseModel):
    id: int
    title: str
    difficulty: int
    parts: List[ListeningPartOut] = []

    class Config:
        from_attributes = True


class MockSlotOut(BaseModel):
    slot_number: int
    attempt_id: Optional[int] = None
    status: Optional[str] = None          # None = not started
    current_section: Optional[str] = None
    listening_band: Optional[float] = None
    reading_band: Optional[float] = None
    writing_band: Optional[float] = None
    overall_band: Optional[float] = None

    class Config:
        from_attributes = True


class MockAttemptOut(BaseModel):
    id: int
    slot_number: int
    status: str
    current_section: str
    listening_section_id: int
    reading_test_id: int
    writing_task1_id: int
    writing_task2_id: int
    listening_band: Optional[float] = None
    reading_band: Optional[float] = None
    writing_band: Optional[float] = None
    overall_band: Optional[float] = None
    listening_submitted_at: Optional[datetime] = None
    reading_submitted_at: Optional[datetime] = None
    writing_submitted_at: Optional[datetime] = None
    ielts_attempt_id: Optional[int] = None

    class Config:
        from_attributes = True


class ListeningAnswerIn(BaseModel):
    question_id: int
    answer_value: Optional[str] = None


class ListeningSubmitIn(BaseModel):
    answers: List[ListeningAnswerIn]

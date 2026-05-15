from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import JSON, BigInteger, Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="student", server_default="student")
    # Telegram integration (Phase 6)
    telegram_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True, index=True)
    telegram_username: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    results = relationship("Result", back_populates="user", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="user", cascade="all, delete-orphan")
    writing_results = relationship("WritingResult", back_populates="user", cascade="all, delete-orphan")
    exam_sessions = relationship("ExamSession", back_populates="user", cascade="all, delete-orphan")


class Test(Base):
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    passage: Mapped[str] = mapped_column(Text, nullable=True)  # Reading passage text

    questions = relationship("Question", back_populates="test", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="test", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    option_a: Mapped[str] = mapped_column(String(500), nullable=False)
    option_b: Mapped[str] = mapped_column(String(500), nullable=False)
    option_c: Mapped[str] = mapped_column(String(500), nullable=False)
    option_d: Mapped[str] = mapped_column(String(500), nullable=False)
    correct_answer: Mapped[str] = mapped_column(String(1), nullable=False)  # "A", "B", "C", or "D"

    test = relationship("Test", back_populates="questions")


class Result(Base):
    __tablename__ = "results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reading_score: Mapped[float] = mapped_column(Float, default=0.0)
    listening_score: Mapped[float] = mapped_column(Float, default=0.0)
    writing_score: Mapped[float] = mapped_column(Float, default=0.0)
    overall: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="results")


class Attempt(Base):
    __tablename__ = "attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    test_id: Mapped[int] = mapped_column(ForeignKey("tests.id"), nullable=False)
    answers: Mapped[dict] = mapped_column(JSON, default=dict)

    user = relationship("User", back_populates="attempts")
    test = relationship("Test", back_populates="attempts")


class WritingResult(Base):
    __tablename__ = "writing_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    essay_text: Mapped[str] = mapped_column(Text, nullable=False)
    feedback: Mapped[str] = mapped_column(Text, nullable=False)  # JSON string from Claude
    band_score: Mapped[float] = mapped_column(Float, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="writing_results")


class ExamSession(Base):
    __tablename__ = "exam_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    reading_band: Mapped[float] = mapped_column(Float, default=0.0)
    listening_band: Mapped[float] = mapped_column(Float, default=0.0)
    writing_band: Mapped[float] = mapped_column(Float, default=0.0)
    overall_band: Mapped[float] = mapped_column(Float, default=0.0)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="exam_sessions")


# ── Multiple Reading Tests System ─────────────────────────────────────────────

class ReadingTest(Base):
    __tablename__ = "reading_tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)

    passages = relationship(
        "ReadingPassage",
        back_populates="test",
        order_by="ReadingPassage.order",
        cascade="all, delete-orphan",
    )


class ReadingPassage(Base):
    __tablename__ = "reading_passages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("reading_tests.id"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)   # 1, 2, 3
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    test = relationship("ReadingTest", back_populates="passages")
    questions = relationship(
        "ReadingQuestion",
        back_populates="passage",
        cascade="all, delete-orphan",
    )


class ReadingQuestion(Base):
    __tablename__ = "reading_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    passage_id: Mapped[int] = mapped_column(ForeignKey("reading_passages.id"), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    option_a: Mapped[str] = mapped_column(String(500), nullable=False)
    option_b: Mapped[str] = mapped_column(String(500), nullable=False)
    option_c: Mapped[str] = mapped_column(String(500), nullable=False)
    option_d: Mapped[str] = mapped_column(String(500), nullable=False)
    correct_answer: Mapped[str] = mapped_column(String(1), nullable=False)

    passage = relationship("ReadingPassage", back_populates="questions")


# ── Teacher-Created Tests ──────────────────────────────────────────────────────

class TeacherTest(Base):
    __tablename__ = "teacher_tests"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    test_type: Mapped[str] = mapped_column(String(50), default="reading")
    pin_code: Mapped[str] = mapped_column(String(10), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    passages = relationship(
        "TeacherPassage",
        back_populates="test",
        order_by="TeacherPassage.order",
        cascade="all, delete-orphan",
    )
    enrollments = relationship("StudentTestEnrollment", back_populates="test", cascade="all, delete-orphan")
    results = relationship("TeacherTestResult", back_populates="test", cascade="all, delete-orphan")
    writing_results = relationship("TeacherWritingResult", cascade="all, delete-orphan")


class TeacherPassage(Base):
    __tablename__ = "teacher_passages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("teacher_tests.id"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    audio_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    test = relationship("TeacherTest", back_populates="passages")
    questions = relationship(
        "TeacherQuestion",
        back_populates="passage",
        cascade="all, delete-orphan",
    )


class TeacherQuestion(Base):
    __tablename__ = "teacher_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    passage_id: Mapped[int] = mapped_column(ForeignKey("teacher_passages.id"), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    option_a: Mapped[str] = mapped_column(String(500), nullable=False)
    option_b: Mapped[str] = mapped_column(String(500), nullable=False)
    option_c: Mapped[str] = mapped_column(String(500), nullable=False)
    option_d: Mapped[str] = mapped_column(String(500), nullable=False)
    correct_answer: Mapped[str] = mapped_column(String(1), nullable=False)

    passage = relationship("TeacherPassage", back_populates="questions")


class StudentTestEnrollment(Base):
    __tablename__ = "student_test_enrollments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    test_id: Mapped[int] = mapped_column(ForeignKey("teacher_tests.id"), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    student = relationship("User", foreign_keys=[student_id])
    test = relationship("TeacherTest", back_populates="enrollments")


class TeacherWritingResult(Base):
    """Stores one student's essay submission for a teacher-created writing test task."""
    __tablename__ = "teacher_writing_results"

    id:         Mapped[int]             = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int]             = mapped_column(ForeignKey("users.id"), nullable=False)
    test_id:    Mapped[int]             = mapped_column(ForeignKey("teacher_tests.id"), nullable=False)
    passage_id: Mapped[int]             = mapped_column(ForeignKey("teacher_passages.id"), nullable=False)
    essay_text: Mapped[str]             = mapped_column(Text, nullable=False)
    feedback:   Mapped[Optional[str]]   = mapped_column(Text, nullable=True)   # JSON string from AI
    band:       Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    word_count: Mapped[int]             = mapped_column(Integer, default=0)
    created_at: Mapped[datetime]        = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    student = relationship("User", foreign_keys=[student_id])


class TelegramLoginCode(Base):
    """
    Temporary codes for logging in (or recovering account) via Telegram.
    Flow:
      1. Website generates code — NO auth required, user_id is NULL at creation
      2. User sends /login CODE to the bot
      3. Bot finds account by Telegram ID → sets user_id + verified = True
      4. Website polls /telegram/login-status → when verified, exchanges for JWT
    Expires in 5 minutes (shorter than linking codes — login is more sensitive).
    """
    __tablename__ = "telegram_login_codes"

    id:         Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    code:       Mapped[str]           = mapped_column(String(10), unique=True, index=True, nullable=False)
    user_id:    Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    expires_at: Mapped[datetime]      = mapped_column(DateTime, nullable=False)
    verified:   Mapped[bool]          = mapped_column(Boolean, default=False, server_default="false")
    used:       Mapped[bool]          = mapped_column(Boolean, default=False, server_default="false")
    created_at: Mapped[datetime]      = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class TelegramVerificationCode(Base):
    """
    Temporary one-time codes used to link a platform account with a Telegram account.
    Flow: website generates code → user sends /link CODE to bot → bot verifies here.
    """
    __tablename__ = "telegram_verification_codes"

    id:         Mapped[int]      = mapped_column(Integer, primary_key=True, index=True)
    user_id:    Mapped[int]      = mapped_column(ForeignKey("users.id"), nullable=False)
    code:       Mapped[str]      = mapped_column(String(10), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    used:       Mapped[bool]     = mapped_column(Boolean, default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User", foreign_keys=[user_id])


# ── IELTS Question Engine ─────────────────────────────────────────────────────

class IELTSTest(Base):
    """A full IELTS practice test (Reading, Listening, or Writing component)."""
    __tablename__ = "ielts_tests"

    id:          Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    title:       Mapped[str]           = mapped_column(String(300), nullable=False)
    test_type:   Mapped[str]           = mapped_column(String(20), default="academic")   # academic | general
    component:   Mapped[str]           = mapped_column(String(20), default="reading")    # reading | listening
    time_limit:  Mapped[int]           = mapped_column(Integer, default=60)              # minutes
    is_active:   Mapped[bool]          = mapped_column(Boolean, default=True, server_default="true")
    created_by:  Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at:  Mapped[datetime]      = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    passages = relationship("IELTSPassage", back_populates="test",
                            order_by="IELTSPassage.order", cascade="all, delete-orphan")
    attempts = relationship("IELTSAttempt", back_populates="test", cascade="all, delete-orphan")


class IELTSPassage(Base):
    """One passage (1-3) within an IELTS test."""
    __tablename__ = "ielts_passages"

    id:        Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    test_id:   Mapped[int]           = mapped_column(ForeignKey("ielts_tests.id"), nullable=False)
    order:     Mapped[int]           = mapped_column(Integer, nullable=False)   # 1, 2, 3
    title:     Mapped[str]           = mapped_column(String(300), nullable=False)
    body_text: Mapped[str]           = mapped_column(Text, nullable=False)
    image_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    test = relationship("IELTSTest", back_populates="passages")
    question_groups = relationship("IELTSQuestionGroup", back_populates="passage",
                                   order_by="IELTSQuestionGroup.order", cascade="all, delete-orphan")


class IELTSQuestionGroup(Base):
    """
    A block of questions sharing the same type and instruction.
    E.g. 'Questions 14–17: True / False / Not Given'
    """
    __tablename__ = "ielts_question_groups"

    id:            Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    passage_id:    Mapped[int]           = mapped_column(ForeignKey("ielts_passages.id"), nullable=False)
    order:         Mapped[int]           = mapped_column(Integer, nullable=False)
    question_type: Mapped[str]           = mapped_column(String(50), nullable=False)
    # tfng | ynng | mcq | mcq_multi | matching_headings | matching_info
    # sentence_completion | summary_completion | table_completion | short_answer
    instruction:   Mapped[str]           = mapped_column(Text, nullable=False)
    word_limit:    Mapped[Optional[int]] = mapped_column(Integer, nullable=True)   # for completion tasks
    options_pool:  Mapped[Optional[dict]]= mapped_column(JSON, nullable=True)      # headings list for matching

    passage = relationship("IELTSPassage", back_populates="question_groups")
    questions = relationship("IELTSQuestion", back_populates="group",
                             order_by="IELTSQuestion.local_order", cascade="all, delete-orphan")


class IELTSQuestion(Base):
    """One question within a group. global_number is the 1-40 exam number."""
    __tablename__ = "ielts_questions"

    id:             Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    group_id:       Mapped[int]           = mapped_column(ForeignKey("ielts_question_groups.id"), nullable=False)
    global_number:  Mapped[int]           = mapped_column(Integer, nullable=False, index=True)
    local_order:    Mapped[int]           = mapped_column(Integer, nullable=False)
    stem:           Mapped[str]           = mapped_column(Text, nullable=False)
    options:        Mapped[Optional[dict]]= mapped_column(JSON, nullable=True)   # [{"key":"A","text":"..."}]
    correct_answer: Mapped[str]           = mapped_column(Text, nullable=False)  # "TRUE","A","migration"
    answer_variants:Mapped[Optional[dict]]= mapped_column(JSON, nullable=True)  # ["colour","color"]

    group = relationship("IELTSQuestionGroup", back_populates="questions")


class IELTSAttempt(Base):
    """One student's attempt at an IELTS test."""
    __tablename__ = "ielts_attempts"

    id:           Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    user_id:      Mapped[int]           = mapped_column(ForeignKey("users.id"), nullable=False)
    test_id:      Mapped[int]           = mapped_column(ForeignKey("ielts_tests.id"), nullable=False)
    started_at:   Mapped[datetime]      = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    time_spent:   Mapped[int]           = mapped_column(Integer, default=0)       # seconds
    status:       Mapped[str]           = mapped_column(String(20), default="in_progress")
    # in_progress | submitted | expired
    raw_score:    Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    band_score:   Mapped[Optional[float]]= mapped_column(Float, nullable=True)

    user    = relationship("User", foreign_keys=[user_id])
    test    = relationship("IELTSTest", back_populates="attempts")
    answers = relationship("IELTSStudentAnswer", back_populates="attempt", cascade="all, delete-orphan")


class WritingPrompt(Base):
    """A writing task prompt (Task 1 or Task 2) drawn randomly for students."""
    __tablename__ = "writing_prompts"

    id:                 Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    task:               Mapped[int]           = mapped_column(Integer, nullable=False)         # 1 or 2
    test_type:          Mapped[str]           = mapped_column(String(20), default="academic")  # academic | general
    topic:              Mapped[str]           = mapped_column(String(100), nullable=False)      # science, health, etc.
    prompt_text:        Mapped[str]           = mapped_column(Text, nullable=False)
    image_description:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)             # chart/diagram for Task 1
    min_words:          Mapped[int]           = mapped_column(Integer, default=250)
    is_active:          Mapped[bool]          = mapped_column(Boolean, default=True, server_default="true")
    created_at:         Mapped[datetime]      = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))


class IELTSStudentAnswer(Base):
    """One saved answer for one question in one attempt."""
    __tablename__ = "ielts_student_answers"

    id:          Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    attempt_id:  Mapped[int]           = mapped_column(ForeignKey("ielts_attempts.id"), nullable=False)
    question_id: Mapped[int]           = mapped_column(ForeignKey("ielts_questions.id"), nullable=False)
    answer_value:Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_flagged:  Mapped[bool]          = mapped_column(Boolean, default=False, server_default="false")
    answered_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    attempt  = relationship("IELTSAttempt", back_populates="answers")
    question = relationship("IELTSQuestion", foreign_keys=[question_id])


class TeacherTestResult(Base):
    """Stores every submission a student makes on a teacher-created test."""
    __tablename__ = "teacher_test_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    test_id: Mapped[int] = mapped_column(ForeignKey("teacher_tests.id"), nullable=False)
    correct: Mapped[int] = mapped_column(Integer, default=0)
    total: Mapped[int] = mapped_column(Integer, default=0)
    band: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    student = relationship("User", foreign_keys=[student_id])
    test = relationship("TeacherTest", back_populates="results")


# ---------------------------------------------------------------------------
# Full Mock Test — Listening layer
# ---------------------------------------------------------------------------

class ListeningSection(Base):
    """One complete IELTS Listening section (4 parts, 40 questions)."""
    __tablename__ = "listening_sections"

    id:         Mapped[int]  = mapped_column(Integer, primary_key=True, index=True)
    title:      Mapped[str]  = mapped_column(String(200), nullable=False)
    difficulty: Mapped[int]  = mapped_column(Integer, default=3)          # 1-5
    is_active:  Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    parts = relationship("ListeningPart", back_populates="section", order_by="ListeningPart.part_number")


class ListeningPart(Base):
    """One of four parts within a ListeningSection."""
    __tablename__ = "listening_parts"

    id:                  Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    section_id:          Mapped[int]           = mapped_column(ForeignKey("listening_sections.id"), nullable=False)
    part_number:         Mapped[int]           = mapped_column(Integer, nullable=False)   # 1-4
    context_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    audio_url:           Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    transcript:          Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    section   = relationship("ListeningSection", back_populates="parts")
    questions = relationship("ListeningQuestion", back_populates="part", order_by="ListeningQuestion.local_order")


class ListeningQuestion(Base):
    """Single question within a ListeningPart."""
    __tablename__ = "listening_questions"

    id:              Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    part_id:         Mapped[int]           = mapped_column(ForeignKey("listening_parts.id"), nullable=False)
    global_number:   Mapped[int]           = mapped_column(Integer, nullable=False, index=True)  # 1-40
    local_order:     Mapped[int]           = mapped_column(Integer, nullable=False)
    question_type:   Mapped[str]           = mapped_column(String(50), nullable=False)
    # form_completion | note_completion | mcq | map_labeling | matching | sentence_completion
    stem:            Mapped[str]           = mapped_column(Text, nullable=False)
    options:         Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)   # list for MCQ / matching
    correct_answer:  Mapped[str]           = mapped_column(Text, nullable=False)
    answer_variants: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)   # acceptable alternatives
    group_instruction: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    map_image_url:   Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    part = relationship("ListeningPart", back_populates="questions")


class ListeningStudentAnswer(Base):
    """Student answer for one ListeningQuestion inside a FullMockAttempt."""
    __tablename__ = "listening_student_answers"

    id:              Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    full_attempt_id: Mapped[int]           = mapped_column(ForeignKey("full_mock_attempts.id"), nullable=False)
    question_id:     Mapped[int]           = mapped_column(ForeignKey("listening_questions.id"), nullable=False)
    answer_value:    Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    answered_at:     Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    full_attempt = relationship("FullMockAttempt", back_populates="listening_answers")
    question     = relationship("ListeningQuestion")


# ---------------------------------------------------------------------------
# Full Mock Test — attempt tracker
# ---------------------------------------------------------------------------

class FullMockAttempt(Base):
    """Tracks one student's attempt at one of the 20 full mock test slots."""
    __tablename__ = "full_mock_attempts"

    id:                    Mapped[int]           = mapped_column(Integer, primary_key=True, index=True)
    user_id:               Mapped[int]           = mapped_column(ForeignKey("users.id"), nullable=False)
    slot_number:           Mapped[int]           = mapped_column(Integer, nullable=False)   # 1-20
    # randomly-assigned content
    listening_section_id:  Mapped[int]           = mapped_column(ForeignKey("listening_sections.id"), nullable=False)
    reading_test_id:       Mapped[int]           = mapped_column(ForeignKey("ielts_tests.id"), nullable=False)
    writing_task1_id:      Mapped[int]           = mapped_column(ForeignKey("writing_prompts.id"), nullable=False)
    writing_task2_id:      Mapped[int]           = mapped_column(ForeignKey("writing_prompts.id"), nullable=False)
    # progress
    started_at:            Mapped[datetime]      = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    status:                Mapped[str]           = mapped_column(String(20), default="in_progress", server_default="in_progress")
    # in_progress | completed
    current_section:       Mapped[str]           = mapped_column(String(20), default="listening", server_default="listening")
    # listening | reading | writing | done
    listening_submitted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    reading_submitted_at:   Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    writing_submitted_at:   Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    # scores
    listening_raw_score:   Mapped[Optional[int]]   = mapped_column(Integer, nullable=True)
    listening_band:        Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    reading_raw_score:     Mapped[Optional[int]]   = mapped_column(Integer, nullable=True)
    reading_band:          Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    writing_band:          Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    overall_band:          Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    # link to existing reading-section attempt (created when student enters reading)
    ielts_attempt_id:      Mapped[Optional[int]]   = mapped_column(ForeignKey("ielts_attempts.id"), nullable=True)

    user             = relationship("User")
    listening_section = relationship("ListeningSection")
    reading_test      = relationship("IELTSTest")
    writing_task1     = relationship("WritingPrompt", foreign_keys=[writing_task1_id])
    writing_task2     = relationship("WritingPrompt", foreign_keys=[writing_task2_id])
    ielts_attempt     = relationship("IELTSAttempt", foreign_keys=[ielts_attempt_id])
    listening_answers = relationship("ListeningStudentAnswer", back_populates="full_attempt")

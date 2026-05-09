from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="student", server_default="student")

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
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

    passages = relationship(
        "TeacherPassage",
        back_populates="test",
        order_by="TeacherPassage.order",
        cascade="all, delete-orphan",
    )


class TeacherPassage(Base):
    __tablename__ = "teacher_passages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    test_id: Mapped[int] = mapped_column(ForeignKey("teacher_tests.id"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)

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

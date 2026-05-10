import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Use DATABASE_URL env var in production (PostgreSQL on Render).
# Fall back to local SQLite for development.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ielts_mock.db")

# Render sets DATABASE_URL starting with "postgres://".
# SQLAlchemy 2.x + psycopg3 needs the "postgresql+psycopg://" dialect prefix.
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg://", 1)
elif DATABASE_URL.startswith("postgresql://") and "+psycopg" not in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://", 1)

# SQLite needs check_same_thread=False; PostgreSQL does not accept that argument
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

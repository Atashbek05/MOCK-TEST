from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


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
    latest_results: list[ResultOut]

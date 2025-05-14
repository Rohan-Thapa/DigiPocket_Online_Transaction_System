from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    tier: Literal['basic','premium'] = 'basic'

class UserInDB(BaseModel):
    id: str | None = Field(alias="_id")
    email: EmailStr
    hashed_password: str
    tier: Literal['basic','premium']
    balance: float = 0.0
    daily_spent: float = 0.0
    kyc: bool

    class Config:
        allow_population_by_field_name = True
        orm_mode = True

class UserOut(BaseModel):
    id: str
    email: EmailStr
    tier: Literal['basic','premium']
    balance: float
    kyc: bool

class LoginRequest(BaseModel):
    username: str
    password: str

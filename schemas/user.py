from pydantic import BaseModel, EmailStr, constr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: constr(min_length=3, max_length=30)
    email: EmailStr
    password: constr(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    eco_wallet_balance: float
    total_donated: float
    total_co2_saved: float
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    eco_wallet_balance: Optional[float] = None 
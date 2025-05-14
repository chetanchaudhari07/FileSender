from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    hashed_password: str
    role: str
    is_verified: bool = False
    verification_token: Optional[str] = None
    created_at: datetime = datetime.utcnow()

class User(UserBase):
    id: str
    role: str
    is_verified: bool
    created_at: datetime
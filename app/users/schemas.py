from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.users.models import ERole


class SUser(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str | None
    company: str
    phone: str
    site: str | None
    registration_date: datetime
    role: str


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str | None = None
    company: str
    phone: str
    site: str | None = None
    # registration_date: datetime
    role: ERole = ERole.user

    class Config:
        from_attributes = True

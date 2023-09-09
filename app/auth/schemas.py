from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.users.models import ERole

class SLogin(BaseModel):
    username: EmailStr
    password: str

    class Config:
        from_attribute = True


class SToken(BaseModel):
    access_token: str
    # token_type: str

class STokenData(BaseModel):
    email: str | None = None

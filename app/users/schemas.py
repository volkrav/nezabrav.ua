from pydantic import BaseModel, EmailStr

from app.users.models import ERole


class SUserAuth(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str | None = None
    company: str
    phone: str
    site: str | None = None
    # registration_date: datetime.datetime
    role: ERole = ERole.user

    class Config:
        from_attributes=True

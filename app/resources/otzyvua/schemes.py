from datetime import date
from typing import List
from pydantic import BaseModel

class SOtzyvuaComment(BaseModel):
    id: str
    title: str | None
    date: date
    text: str | None
    phone: str | None
    advantages: str | None
    disadvantages: str | None
    images: List[str] | None

    class Config:
        from_attributes = True

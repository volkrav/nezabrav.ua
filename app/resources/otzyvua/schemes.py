from datetime import date
from typing import List
from pydantic import BaseModel

class SOtzyvuaComment(BaseModel):
    id: str
    title: str
    date: date
    text: str
    phone: str
    advantages: str
    disadvantages: str
    images: List[str]

    class Config:
        from_attributes = True

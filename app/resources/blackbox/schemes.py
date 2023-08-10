from typing import List
from pydantic import BaseModel, Json

from app.resources.blackbox.models import BlackboxComment

class SBlackboxComment(BaseModel):
    id: str
    fios: List[str] | None
    phone: str | None
    phone_formatted: str | None
    tracks: Json

    class Config:
        from_attributes = True


class SResponseMessageFromBlackbox(BaseModel):
    status: str
    data: SBlackboxComment | None

    class Config:
        from_attributes = True

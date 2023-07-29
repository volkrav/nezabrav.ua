from typing import List
from pydantic import BaseModel, Json

class SBlackboxComment(BaseModel):
    id: str
    fios: List[str]
    phone: str
    phone_formatted: str
    tracks: Json

    class Config:
        from_attributes = True

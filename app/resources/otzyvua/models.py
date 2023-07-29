from sqlalchemy import ARRAY, JSON, Column, Date, String
from app.database import Base


class OtzyvuaComment(Base):
    __tablename__ = 'otzyvua'

    id = Column(String, primary_key=True, nullable=False)
    title = Column(String, nullable=True)
    date = Column(Date)
    text = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    advantages = Column(ARRAY(String), nullable=True)
    disadvantages = Column(ARRAY(String), nullable=True)
    images = Column(ARRAY(String), nullable=True)

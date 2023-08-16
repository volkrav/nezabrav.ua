from asyncpg import NameTooLongError
from sqlalchemy import Column, Integer, String, null
from app.database import Base

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

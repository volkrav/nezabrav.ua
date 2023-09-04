import enum
from typing import List

from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import relationship, Mapped

from app.database import Base


class ERole(enum.Enum):
    admin = 'admin'
    user = 'user'


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    company = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    site = Column(String, nullable=True)
    registration_date = Column(String, nullable=True)
    role = Column(Enum(ERole), nullable=False, default=ERole.user)

    # report: Mapped[List['Reports']] = relationship(back_populates='user')

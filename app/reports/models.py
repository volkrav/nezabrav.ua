import enum

from sqlalchemy import (ARRAY, Column, DateTime, Enum, ForeignKey, Integer,
                        String, func)
from sqlalchemy.orm import relationship, Mapped

from app.database import Base


class ESource(enum.Enum):
    nezabrav = 'nezabrav'
    blackbox = 'blackbox'
    otzyvua = 'otzyvua'


class EStatusBlackbox(enum.Enum):
    online = 'online'
    offline = 'offline'


class Reports(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ext_id = Column(String, nullable=False)
    source = Column(Enum(ESource), nullable=False)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    phone = Column(String, nullable=False)
    name = Column(String, nullable=True)
    extra_names = Column(ARRAY(String), nullable=True)
    report = Column(String, nullable=False)
    TTN = Column(String, nullable=True)
    carrier = Column(String, nullable=True)
    city = Column(String, nullable=True)
    warehouse = Column(String, nullable=True)
    losses = Column(Integer, nullable=True)
    shipment_date = Column(DateTime, nullable=True)
    images = Column(ARRAY(String), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # user: Mapped['Users'] = relationship(back_populates='report')

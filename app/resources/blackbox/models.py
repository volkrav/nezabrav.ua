from sqlalchemy import ARRAY, JSON, Column, Date, Integer, String
from app.database import Base


class BlackboxComment(Base):
    __tablename__ = 'blackbox'

    id = Column(String, primary_key=True, nullable=False)
    fios = Column(ARRAY(String), nullable=True)
    phone = Column(String, nullable=True)
    phone_formatted = Column(String, nullable=True)
    tracks = Column(JSON, nullable=False) # TODO it is better to make a separate table


    # city = Column(String, nullable=True)
    # comment = Column(String, nullable=True)
    # cost = Column(String, nullable=True)
    # !did not find the format of the returned string wit the date
    # date = Column(String, nullable=True) #
    # type = Column(Date, nullable=True)
    # warehouse = Column(Date, nullable=True)

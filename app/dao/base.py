from typing import Any
from sqlalchemy import Insert, Result, Select, insert, select
from sqlalchemy.orm import Session

from app.database import Base, async_session_maker


class BaseDAO:
    model: Base = None

    @classmethod
    async def add(cls, **data):
        session: Session
        async with async_session_maker() as session:
            query: Insert = insert(cls.model).values(**data).returning(cls.model.id)
            result: Result = await session.execute(query)
            await session.commit()
            return result.scalar()

    @classmethod
    async def find_by_id(cls, model_id: int | str):
        session: Session
        async with async_session_maker() as session:
            query: Select = select(cls.model).filter_by(id=model_id)
            result: Result = await session.execute(query)
            return result.scalar_one_or_none()
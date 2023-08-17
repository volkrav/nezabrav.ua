from typing import Any

from sqlalchemy import Insert, MappingResult, Result, Select, insert, select
from sqlalchemy.orm import Session

from app.database import Base, async_session_maker
from app.exceptions import NoDatabaseConnection


class BaseDAO:
    model: Base = None

    @classmethod
    async def add(cls, **data) -> Any | None:
        session: Session
        async with async_session_maker() as session:
            query: Insert = insert(cls.model).values(
                **data).returning(cls.model.id)
            try:
                result: Result = await session.execute(query)
                await session.commit()
            except ConnectionRefusedError as e:
                raise NoDatabaseConnection
        return result.scalar()

    @classmethod
    async def find_by_id(cls, model_id: int | str) -> Any | None:
        session: Session
        async with async_session_maker() as session:
            query: Select = select(cls.model).filter_by(id=model_id)
            try:
                result: Result = await session.execute(query)
            except ConnectionRefusedError as e:
                raise NoDatabaseConnection
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filters):
        session: Session
        async with async_session_maker() as session:
            query: Select = select(cls.model).filter_by(**filters)
            try:
                result: Result = await session.execute(query)
            except ConnectionRefusedError as e:
                raise NoDatabaseConnection
            return result.scalar_one_or_none()


    @classmethod
    async def find_all_filter_by(cls, **filters) -> MappingResult:
        session: Session
        async with async_session_maker() as session:
            query: Select = select(
                cls.model.__table__.columns).filter_by(**filters)
            try:
                result: Result = await session.execute(query)
            except ConnectionRefusedError as e:
                raise NoDatabaseConnection
            return result.mappings().all()

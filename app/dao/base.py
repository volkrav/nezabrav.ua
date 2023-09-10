from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import (Delete, Insert, MappingResult, Result, Select, Update,
                        delete, insert, select, update)
from sqlalchemy.orm import Session

from app.database import Base, async_session_maker
from app.exceptions import NoDatabaseConnection


class BaseDAO:
    model: Base = None

    @classmethod
    async def add(cls, **data) -> Any | None:
        print(data)
        session: Session
        async with async_session_maker() as session:
            query: Insert = insert(cls.model).values(
                **data).returning(cls.model.phone)
            try:
                result: Result = await session.execute(query)
                await session.commit()
            except ConnectionRefusedError as e:
                raise NoDatabaseConnection()
        return result.scalar()

    @classmethod
    async def find_by_id(cls, model_id: int | str) -> Any | None:
        session: Session
        async with async_session_maker() as session:
            query: Select = select(cls.model).filter_by(id=model_id)
            try:
                result: Result = await session.execute(query)
            except ConnectionRefusedError as e:
                raise NoDatabaseConnection()
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filters):
        session: Session
        async with async_session_maker() as session:
            query: Select = select(cls.model).filter_by(**filters)
            try:
                result: Result = await session.execute(query)
            except ConnectionRefusedError as e:
                raise NoDatabaseConnection()
            except OSError as e:
                print(e)
                exit(1)
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
                raise NoDatabaseConnection()
        return result.mappings().all()

    @classmethod
    async def delete(cls, **filters):
        session: Session
        async with async_session_maker() as session:
            stmt: Delete = delete(cls.model).filter_by(**filters)
            try:
                await session.execute(stmt)
            except ConnectionRefusedError as e:
                raise NoDatabaseConnection()
            await session.commit()

    @classmethod
    async def update(cls, filters, values):
        session: Session
        print(filters)
        print(values)
        stmt: Update = update(cls.model).filter_by(**filters).values(**values)
        async with async_session_maker() as session:
            try:
                await session.execute(stmt)
            except ConnectionRefusedError as e:
                raise NoDatabaseConnection()
            await session.commit()

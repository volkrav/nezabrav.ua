from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.jwt import get_password_hash, get_current_user
from app.exceptions import UserAlreadyExsitsException
from app.users.dao import UsersDAO
from app.users.schemas import SUser, SUserRegister

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.post('/registration')
async def registration_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExsitsException()
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        company=user_data.company,
        phone=user_data.phone,
        site=user_data.site,
        registration_date=datetime.utcnow(),
        role=user_data.role,
    )


@router.get("/me")
async def read_users_me(
    current_user: Annotated[SUser, Depends(get_current_user)]
):
    return current_user

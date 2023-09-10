from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, Request

from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
import traceback

from app.config import settings
from app.exceptions import InvalidEmailOrPasswordException, InvalidTokenFormatException, TokenAbsentException, TokenExpiredException, UserIsNotPresentedException
from app.users.dao import UsersDAO
from app.users.models import Users
from app.users.schemas import SUser
from .schemas import SToken, STokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password) -> bool:
    if settings.MODE == 'TEST':
        return plain_password == hashed_password
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def get_user(email: EmailStr) -> Users | None:
    return await UsersDAO.find_one_or_none(email=email)

async def authenticate_user(username: EmailStr, password: str) -> Users | bool:
    user = await get_user(username)
    if not user:
        # return "User with this email does not exist"
        return False
    if not verify_password(password, user.hashed_password):
        # return "Incorrect password"
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> SToken:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_token(request: Request) -> SToken:
    token = request.cookies.get('access_token')
    if not token:
        raise TokenAbsentException()
    return token


# depends = oauth2_scheme
depends = get_token

async def get_current_user(token: Annotated[str, Depends(depends)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if id is None:
            raise InvalidTokenFormatException(detail='email is None')
        token_data = STokenData(email=email) # username -> id
    except ExpiredSignatureError as err:
        raise TokenExpiredException()
    except JWTError as err:
        #! log(traceback.format_exception_only(err)[0])
        raise InvalidTokenFormatException(traceback.format_exception_only(err)[0])
    expire = payload.get('exp')
    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise TokenExpiredException()
    user = await get_user(email=token_data.email)
    if user is None:
        raise UserIsNotPresentedException()
    return user

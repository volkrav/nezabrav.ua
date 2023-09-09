from datetime import datetime, timedelta
from typing import Annotated
from fastapi import APIRouter, Header, Request, Response, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt import authenticate_user, create_access_token, get_current_user

from app.auth.schemas import SLogin, SToken
from app.config import settings
from app.exceptions import InvalidEmailOrPasswordException
from app.users.schemas import SUser


router = APIRouter(
    tags=['Auth']
)


@router.post("/login", response_model=SToken)
async def login_for_access_token(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    # form_data: SLogin,
):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise InvalidEmailOrPasswordException()
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.email)}, expires_delta=access_token_expires
    )
    response.set_cookie(key='access_token',
                        value=access_token,
                        # max_age=access_token_expires.seconds,
                        httponly=True)
    return {"access_token": access_token}


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie(key='access_token', path='/', domain=None)

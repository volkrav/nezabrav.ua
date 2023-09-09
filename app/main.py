from fastapi import FastAPI

from app.router import router as search_router
from app.users.router import router as users_router
from app.auth.router import router as auth_router
from starlette.middleware.sessions import SessionMiddleware



app = FastAPI(title='nezabrav.com')
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

app.include_router(search_router)
app.include_router(users_router)
app.include_router(auth_router)

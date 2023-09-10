import logging

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.auth.router import router as auth_router
from app.router import router as search_router
from app.users.router import router as users_router


# Configure logging
# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    datefmt='%d-%m-%y %H:%M:%S',
    format=u'%(asctime)s - [%(levelname)s] - (%(name)s).%(funcName)s:%(lineno)d - %(message)s',
    # filename='nezabrav.log'
)

app = FastAPI(title='nezabrav.com')
app.add_middleware(SessionMiddleware, secret_key="some-random-string")

app.include_router(search_router)
app.include_router(users_router)
app.include_router(auth_router)

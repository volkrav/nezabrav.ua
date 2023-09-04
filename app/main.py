from fastapi import FastAPI

from app.router import router


app = FastAPI(title='nezabrav.com')

app.include_router(router)

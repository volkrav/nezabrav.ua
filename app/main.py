from fastapi import FastAPI
from app.search.router import router as search_router

app = FastAPI(title='nezabrav.com')


app.include_router(search_router)

from fastapi import FastAPI
from app.search.router import router as search_router
from app.resources.blackbox.router import router as blackbox_router

app = FastAPI(title='nezabrav.com')

app.include_router(search_router)
app.include_router(blackbox_router)

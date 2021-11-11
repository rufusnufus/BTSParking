from app.db import db
from fastapi import FastAPI
from .routers import api

app = FastAPI(title="Async FastAPI")

app.include_router(api.router)


@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

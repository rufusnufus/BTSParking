from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.api_v1 import api
from app.db import db
from app.logs import logger

app = FastAPI(title="Async FastAPI")

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)


instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    inprogress_name="inprogress",
    inprogress_labels=True,
)

instrumentator.instrument(app)
instrumentator.expose(app, include_in_schema=False, should_gzip=True)


@app.on_event("startup")
async def startup():
    await db.connect()
    logger.info("PostgreSQL DB is connected")


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    logger.info("PostgreSQL DB is disconnected")

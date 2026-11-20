
from contextlib import asynccontextmanager
from importlib.metadata import version

from fastapi import FastAPI
from redis.asyncio import Redis
from .controller.location_controller import router

APP_NAME = "location-service"
APP_VERSION = version(APP_NAME)


@asynccontextmanager
async def lifespan(app: FastAPI) :
    app.state.redis_client=Redis(
        host="localhost",
        port=6379,
    )
    yield

app = FastAPI(title=APP_NAME, version=APP_VERSION, lifespan=lifespan)
app.include_router(router)

"""This module contains the fastAPI serving the different endpoints to the customer."""

import asyncio
from contextlib import asynccontextmanager
from importlib import resources
from typing import Any

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from fairqapi import __version__
from fairqapi.cache.cache import cache
from fairqapi.routers import (
    grid,
    health_check,
    lor,
    simulation,
    stations,
    streets,
)

background_tasks: set[asyncio.Task[Any]] = set()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    Start a coroutine which checks every minute if
    an update to the cache is necessary.
    """
    loop = asyncio.get_event_loop()
    task = loop.create_task(cache.load_cache_files_loop())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)
    yield


def get_version():
    return __version__


description = resources.files("fairqapi").joinpath("api_description.md").read_text(encoding="utf-8")

app = FastAPI(
    title="Forecasting Air Quality: FAirQ API 🍃",
    description=description,
    version=get_version(),
    license_info={
        "name": "DL-DE BY-2.0",
        "url": "https://www.govdata.de/dl-de/by-2-0",
    },
    contact={
        "name": "inwt",
        "url": "https://www.inwt-statistics.com/",
        "email": "fairq@inwt-statistics.de",
    },
    lifespan=lifespan,
)

Instrumentator().instrument(app).expose(app, endpoint="/metrics/", include_in_schema=False)

app.include_router(health_check.router)
app.include_router(stations.router)
app.include_router(streets.router)
app.include_router(grid.router)
app.include_router(lor.router)
app.include_router(simulation.router)

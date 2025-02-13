"""This module contains the fastAPI serving the different endpoints to the customer."""
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware, metrics
import pkgutil

from fairqapi import __version__
from fairqapi.cache.cache import cache
from fairqapi.routers import (  # noqa: WPS300
    grid,
    health_check,
    lor,
    simulation,
    stations,
    streets,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Start a coroutine which checks every minute if
    an update to the cache is necessary.
    """
    loop = asyncio.get_event_loop()
    loop.create_task(cache.load_cache_files_loop())
    yield


def get_version():
    return __version__


description = pkgutil.get_data("fairqapi", "api_description.md").decode("utf-8")

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

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)

app.include_router(health_check.router)
app.include_router(stations.router)
app.include_router(streets.router)
app.include_router(grid.router)
app.include_router(lor.router)
app.include_router(simulation.router)

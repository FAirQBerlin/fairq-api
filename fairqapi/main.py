"""This module contains the fastAPI serving the different endpoints to the customer."""
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware, metrics

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


description = """
FAirQ API 🚀

## stations

get prediction of no2, pm10 & pm2.5 for all  measuringstation

## streets

get prediction of no2, pm10 & pm2.5 on street level

## grid

get prediction of no2, pm10 & pm2.5 on grid level

## lor

get prediction of no2, pm10 & pm2.5 for the "Lebensweltlich
orientierte Räume" (LOR)

## simulation

Get predictions of no2, pm10 and pm2.5 for simulated (reduced) kfz per hour in selected streets.
"""

app = FastAPI(
    title="FAirQ API",
    description=description,
    version=get_version(),
    # license_info,
    # contact,
    lifespan=lifespan
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)

app.include_router(health_check.router)
app.include_router(stations.router)
app.include_router(streets.router)
app.include_router(grid.router)
app.include_router(lor.router)
app.include_router(simulation.router)

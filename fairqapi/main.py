"""This module contains the fastAPI serving the different endpoints to the customer."""
import asyncio

from fastapi import FastAPI
from starlette_prometheus import PrometheusMiddleware, metrics

from fairqapi.cache.cache import cache
from fairqapi.routers import (  # noqa: WPS300
    grid,
    health_check,
    lor,
    simulation,
    stations,
    streets,
)

app = FastAPI()

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics/", metrics)

app.include_router(health_check.router)
app.include_router(stations.router)
app.include_router(streets.router)
app.include_router(grid.router)
app.include_router(lor.router)
app.include_router(simulation.router)


@app.on_event("startup")
async def update_cache_periodically():
    """
    Start a coroutine which checks every minute if
    an update to the cache is necessary.
    """
    loop = asyncio.get_event_loop()
    loop.create_task(cache.load_cache_files_loop())

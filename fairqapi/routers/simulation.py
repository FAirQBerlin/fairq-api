"""Endpoint /simulation functionality."""

import logging
from logging.config import dictConfig

from fastapi import APIRouter, Depends

from fairqapi.cache.cache import cache
from fairqapi.logging_config.logger_config import get_logger_config
from fairqapi.schemas.request import Request
from fairqapi.schemas.simulation_response import SimulationResponse

dictConfig(get_logger_config())

router = APIRouter()


@router.get("/simulation", response_model=SimulationResponse)
async def simulation(request: Request = Depends()):
    """Simulation endpoint."""
    simulation_out = {
        "type": "FeatureCollection",
        "features": cache.simulation["features"][request.skip:(request.skip + request.limit)]
    }
    logging.info("access simulation")
    return simulation_out

"""Endpoint /simulation functionality."""

import logging
from logging.config import dictConfig
from typing import Annotated

from fastapi import APIRouter, Depends

from fairqapi.cache.cache import cache
from fairqapi.logging_config.logger_config import get_logger_config
from fairqapi.schemas.request import Request
from fairqapi.schemas.simulation_response import SimulationResponse

dictConfig(get_logger_config())
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/simulation", response_model=SimulationResponse)
async def simulation(request: Annotated[Request, Depends()]):
    """Simulation endpoint."""
    simulation_out = {
        "type": "FeatureCollection",
        "features": cache.simulation["features"][request.skip : (request.skip + request.limit)],
    }
    logger.info("access simulation")
    return simulation_out

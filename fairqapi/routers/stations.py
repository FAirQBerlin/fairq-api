"""Endpoint /stations functionality."""

import logging
from logging.config import dictConfig

from fastapi import APIRouter

from fairqapi.cache.cache import cache
from fairqapi.logging_config.logger_config import get_logger_config
from fairqapi.schemas.stations_response import StationsResponse

dictConfig(get_logger_config())
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/stations", response_model=StationsResponse)
async def stations():
    """stations endpoint."""
    logger.info("access stations")
    return cache.stations

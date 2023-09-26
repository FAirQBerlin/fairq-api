"""Endpoint /streets functionality."""

import logging
from logging.config import dictConfig

from fastapi import APIRouter, Depends

from fairqapi.cache.cache import cache
from fairqapi.logging_config.logger_config import get_logger_config
from fairqapi.schemas.request import Request
from fairqapi.schemas.streets_response import StreetsResponse

dictConfig(get_logger_config())

router = APIRouter()


@router.get("/streets", response_model=StreetsResponse)
async def streets(request: Request = Depends()):
    """Streets endpoint."""
    streets_out = {
        "type": "FeatureCollection",
        "features": cache.streets["features"][request.skip:(request.skip + request.limit)]
    }
    logging.info("access streets")
    return streets_out

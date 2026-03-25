"""Endpoint /grid functionality."""

import logging
from logging.config import dictConfig
from typing import Annotated

from fastapi import APIRouter, Depends

from fairqapi.cache.cache import cache
from fairqapi.logging_config.logger_config import get_logger_config
from fairqapi.schemas.grid_response import GridResponse
from fairqapi.schemas.request import Request

dictConfig(get_logger_config())
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/grid", response_model=GridResponse)
async def grid(request: Annotated[Request, Depends()]):
    """Grid endpoint."""

    grid_out = {
        "type": "FeatureCollection",
        "features": cache.grid["features"][request.skip : (request.skip + request.limit)],
    }
    logger.info("access grid")
    return grid_out

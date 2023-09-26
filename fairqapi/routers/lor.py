"""Endpoint /lor functionality."""

import logging
from logging.config import dictConfig

from fastapi import APIRouter, Depends

from fairqapi.cache.cache import cache
from fairqapi.logging_config.logger_config import get_logger_config
from fairqapi.schemas.lor_response import LorResponse
from fairqapi.schemas.request import Request

dictConfig(get_logger_config())

router = APIRouter()


@router.get("/lor", response_model=LorResponse)
async def lor(request: Request = Depends()):
    """LOR (LebensOrientierte Räume) endpoint."""
    lor_out = {
        "type": "FeatureCollection",
        "features": cache.lor["features"][request.skip:(request.skip + request.limit)]
    }
    logging.info("access lor")
    return lor_out

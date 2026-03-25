"""Endpoint /health functionality."""

import logging
from logging.config import dictConfig

from fastapi import APIRouter, HTTPException

from fairqapi.cache.cache import cache
from fairqapi.logging_config.logger_config import get_logger_config

dictConfig(get_logger_config())
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def perform_api_healthcheck():
    """Perform health check."""

    if cache.cache_is_loaded():
        logger.info("access health")
        return {"status": "everything good"}

    logger.error("health ERROR: cache not loaded")
    raise HTTPException(status_code=503, detail="API not ready")

"""Endpoint /health functionality."""
import logging
from logging.config import dictConfig

from fastapi import APIRouter, HTTPException

from fairqapi.cache.cache import cache
from fairqapi.logging_config.logger_config import get_logger_config

dictConfig(get_logger_config())

router = APIRouter()


@router.get("/health")
async def perform_api_healthcheck():
    """Perform health check."""

    if cache.cache_is_loaded():
        logging.info("access health")
        return {"status": "everything good"}

    logging.error("health ERROR: cache not loaded")
    raise HTTPException(status_code=503, detail="API not ready")

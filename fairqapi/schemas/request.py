"""Request model for streets & grid endpoints."""
from fastapi import Query
from pydantic import BaseModel


class Request(BaseModel):
    """Request class for grid and streets endpoints"""

    skip: int = Query(default=0, ge=0, le=400000)
    limit: int = Query(default=1000, ge=10, le=400000)

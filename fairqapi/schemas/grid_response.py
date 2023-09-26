"""Response model for grid endpoint."""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Geometry(BaseModel):
    type: str = "Point"
    coordinates: List[int]
    crs: str = "EPSG:25833"


class Properties(BaseModel):
    id: int
    date_time_forecast_iso8601: datetime
    forecast_range_iso8601: str
    no2: List[float]
    pm10: List[float]
    pm2_5: List[float] = Field(..., alias="pm2.5")


class Feature(BaseModel):
    type: str = "Feature"
    geometry: Geometry
    properties: Properties


class GridResponse(BaseModel):
    type: str = "FeatureCollection"
    features: List[Feature]

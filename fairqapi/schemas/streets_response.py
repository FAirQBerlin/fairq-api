"""Response model for streets endpoint."""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Geometry(BaseModel):
    type: str = "LineString"
    coordinates: List[List[float]]  # weiter eingrenzbar?
    crs: str = "EPSG:25833"


class Properties(BaseModel):
    element_nr: str
    date_time_forecast_iso8601: datetime
    forecast_range_iso8601: str  # weiter eingrenzbar?
    no2: List[float]
    pm10: List[float]
    pm2_5: List[float] = Field(..., alias="pm2.5")


class Feature(BaseModel):
    type: str = "Feature"
    geometry: Geometry
    properties: Properties


class StreetsResponse(BaseModel):
    type: str = "FeatureCollection"
    features: List[Feature]

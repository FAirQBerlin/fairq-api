"""Response model for streets endpoint."""

from datetime import datetime

from pydantic import BaseModel, Field


class Geometry(BaseModel):
    type: str = "MultiPolygon"
    coordinates: list[list[list[list[float]]]]
    crs: str = "EPSG:25833"


class Properties(BaseModel):
    PLR_ID: str
    date_time_forecast_iso8601: datetime
    forecast_range_iso8601: str
    no2: list[float]
    pm10: list[float]
    pm2_5: list[float] = Field(..., alias="pm2.5")


class Feature(BaseModel):
    type: str = "Feature"
    geometry: Geometry
    properties: Properties


class LorResponse(BaseModel):
    type: str = "FeatureCollection"
    features: list[Feature]

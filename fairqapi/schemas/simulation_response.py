"""Response model for simulation endpoint."""

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class Geometry(BaseModel):
    type: str = "LineString"
    coordinates: List[List[float]]
    crs: str = "EPSG:25833"


class Properties(BaseModel):
    element_nr: str
    date_time_forecast_iso8601: datetime
    forecast_range_iso8601: str
    no2_0: List[float]
    no2_10: List[float]
    no2_20: List[float]
    no2_30: List[float]
    no2_40: List[float]
    no2_50: List[float]
    no2_60: List[float]
    no2_70: List[float]
    no2_80: List[float]
    no2_90: List[float]
    no2_100: List[float]
    pm10_0: List[float]
    pm10_10: List[float]
    pm10_20: List[float]
    pm10_30: List[float]
    pm10_40: List[float]
    pm10_50: List[float]
    pm10_60: List[float]
    pm10_70: List[float]
    pm10_80: List[float]
    pm10_90: List[float]
    pm10_100: List[float]
    pm25_0: List[float] = Field(..., alias="pm2.5_0")
    pm25_10: List[float] = Field(..., alias="pm2.5_10")
    pm25_20: List[float] = Field(..., alias="pm2.5_20")
    pm25_30: List[float] = Field(..., alias="pm2.5_30")
    pm25_40: List[float] = Field(..., alias="pm2.5_40")
    pm25_50: List[float] = Field(..., alias="pm2.5_50")
    pm25_60: List[float] = Field(..., alias="pm2.5_60")
    pm25_70: List[float] = Field(..., alias="pm2.5_70")
    pm25_80: List[float] = Field(..., alias="pm2.5_80")
    pm25_90: List[float] = Field(..., alias="pm2.5_90")
    pm25_100: List[float] = Field(..., alias="pm2.5_100")

class Feature(BaseModel):
    type: str = "Feature"
    geometry: Geometry
    properties: Properties


class SimulationResponse(BaseModel):
    type: str = "FeatureCollection"
    features: List[Feature]

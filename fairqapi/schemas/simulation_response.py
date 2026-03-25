"""Response model for simulation endpoint."""

from datetime import datetime

from pydantic import BaseModel, Field


class Geometry(BaseModel):
    type: str = "LineString"
    coordinates: list[list[float]]
    crs: str = "EPSG:25833"


class Properties(BaseModel):
    element_nr: str
    date_time_forecast_iso8601: datetime
    forecast_range_iso8601: str
    no2_0: list[float]
    no2_10: list[float]
    no2_20: list[float]
    no2_30: list[float]
    no2_40: list[float]
    no2_50: list[float]
    no2_60: list[float]
    no2_70: list[float]
    no2_80: list[float]
    no2_90: list[float]
    no2_100: list[float]
    pm10_0: list[float]
    pm10_10: list[float]
    pm10_20: list[float]
    pm10_30: list[float]
    pm10_40: list[float]
    pm10_50: list[float]
    pm10_60: list[float]
    pm10_70: list[float]
    pm10_80: list[float]
    pm10_90: list[float]
    pm10_100: list[float]
    pm25_0: list[float] = Field(..., alias="pm2.5_0")
    pm25_10: list[float] = Field(..., alias="pm2.5_10")
    pm25_20: list[float] = Field(..., alias="pm2.5_20")
    pm25_30: list[float] = Field(..., alias="pm2.5_30")
    pm25_40: list[float] = Field(..., alias="pm2.5_40")
    pm25_50: list[float] = Field(..., alias="pm2.5_50")
    pm25_60: list[float] = Field(..., alias="pm2.5_60")
    pm25_70: list[float] = Field(..., alias="pm2.5_70")
    pm25_80: list[float] = Field(..., alias="pm2.5_80")
    pm25_90: list[float] = Field(..., alias="pm2.5_90")
    pm25_100: list[float] = Field(..., alias="pm2.5_100")


class Feature(BaseModel):
    type: str = "Feature"
    geometry: Geometry
    properties: Properties


class SimulationResponse(BaseModel):
    type: str = "FeatureCollection"
    features: list[Feature]

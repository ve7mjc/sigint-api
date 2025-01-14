from common.schemas import MinioObjectCreateBase

from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class Coordinate(BaseModel):

    # wgs84
    latitude: float
    longitude: float
    ellipsoid_height: Optional[float] = None  # height above elipsoid (gps height)

    elevation_amsl: Optional[float] = None # computed from geoid, srtm de


class CoordinateCreate(Coordinate):

    @model_validator(mode="after")
    def validate_coordinates(cls, values):
        if not (-180 <= values.longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        if not (-90 <= values.latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        # Altitude validation (optional)
        # if not isinstance(values.ellipsoid_height, (int, float)):
        #     raise ValueError("elipsoid_height must be a number.")
        return values


from common.schemas import MinioObjectCreateBase
from common.schemas.geo import CoordinateCreate

from typing import Optional
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class InterceptAudioCreate(MinioObjectCreateBase):
    pass


class Intercept(BaseModel):

    # node information
    node_id: Optional[UUID] = None
    node_name: Optional[str] = None

    # position information
    position: Optional[CoordinateCreate] = None

    antenna_height: Optional[float] = None

    # signal characteristics
    frequency_center: float
    time_start: datetime
    duration: float


class InterceptCreateRequest(Intercept):

    @model_validator(mode="after")
    def validate_id_or_name(cls, values):
        if not values.node_id and not values.node_name:
            raise ValueError("Either 'node_id' or 'node_name' must be provided.")
        return values

    # audio_file: Optional[InterceptAudioCreate] = None

    # location: Location


class InterceptCreateResponse(BaseModel):

    id: UUID

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from server.schemas.common import Location, MinioObjectCreateBase


class InterceptAudioCreate(MinioObjectCreateBase):
    pass


class InterceptCreate(BaseModel):

    node_id: str

    frequency_center: float
    time_start: datetime
    duration: float

    audio_file: Optional[InterceptAudioCreate] = None

    # location: Location


class InterceptResponse(BaseModel):
    id: int

    class Config:
        from_attributes = True



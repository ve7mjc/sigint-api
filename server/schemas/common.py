from pydantic import BaseModel
from typing import Optional


class Location(BaseModel):
    latitude: float
    longitude: float
    elevation: Optional[float] = None

class MinioObjectCreateBase(BaseModel):
    bucket_name: str
    object_name: str
    etag: str
    size: Optional[int] = None


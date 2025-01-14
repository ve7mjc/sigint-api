from pydantic import BaseModel
from typing import Optional


class MinioObjectCreateBase(BaseModel):
    bucket_name: str
    object_name: str
    etag: str
    size: Optional[int] = None

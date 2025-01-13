from minio import Minio
from minio.helpers import ObjectWriteResult
from app.core.config import settings
from io import BytesIO

minio_client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=True,
)

def upload_to_minio(bucket_name: str, file_name: str, file_data: bytes) -> ObjectWriteResult:
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
    result = minio_client.put_object(bucket_name, file_name, BytesIO(file_data), length=len(file_data))
    return result



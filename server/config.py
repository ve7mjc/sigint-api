from os import getenv
from dataclasses import dataclass


@dataclass
class DatabaseConfig():
    username: str
    password: str
    name: str

    # defaults
    host: str = "localhost"
    port: int = 5432

@dataclass
class MinioConfig():
    endpoint: str
    bucket_name: str
    access_key: str
    secret_key: str


# Database Setup
db_config = DatabaseConfig(
    host = getenv('DATABASE_HOST'),
    port = getenv('DATABASE_PORT', 5432),
    username = getenv('DATABASE_USERNAME'),
    password = getenv('DATABASE_PASSWORD'),
    name = getenv('DATABASE_NAME', 'sigint')
)

def build_db_url(cfg: DatabaseConfig) -> str:
    return f"postgresql://{cfg.username}:{cfg.password}@{cfg.host}/{cfg.name}"

db_url = build_db_url(db_config)


minio_config = MinioConfig(
    endpoint=getenv('MINIO_ENDPOINT'),
    bucket_name=getenv('MINIO_BUCKET_NAME'),
    access_key=getenv('MINIO_ACCESS_KEY'),
    secret_key=getenv('MINIO_SECRET_KEY')
)


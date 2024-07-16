import os

from dotenv import load_dotenv

load_dotenv('../../.env')

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "memes")
POSTGRES_SOCKET = os.getenv("POSTGRES_SOCKET", "localhost:5432")

DB_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SOCKET}/{POSTGRES_DB}"

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")

MEDIA_SERVICE_PORT = int(os.getenv("MEDIA_SERVICE_PORT", 8001))
MEDIA_SERVICE_HOST = os.getenv("MEDIA_SERVICE_HOST", "localhost")
MEDIA_SERVICE_SOCKET = f"{MEDIA_SERVICE_HOST}:{MEDIA_SERVICE_PORT}"

PUBLIC_API_PORT = int(os.getenv("PUBLIC_API_PORT", 8000))

BUCKET_NAME = os.getenv("BUCKET_NAME", "memes")

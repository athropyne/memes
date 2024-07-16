import os

import minio
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi_cli.cli import run
from minio import S3Error
from starlette import status
from starlette.responses import StreamingResponse

load_dotenv('../.env')

MEDIA_SERVICE_PORT = os.getenv("MEDIA_SERVICE_PORT", 8001)
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
BUCKET_NAME = os.getenv("BUCKET_NAME", "memes")

s3client = minio.Minio(
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    secure=False,
    cert_check=False
)

app = FastAPI(lifespan=None)


@app.get("/{filename}")
async def media(filename: str):
    try:
        obj = s3client.get_object(BUCKET_NAME, filename)
        return StreamingResponse(
            obj
        )
    except S3Error as e:
        if e.code == "NoSuchKey":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="объект не найден"
            )
        # И здесь типа нужно отправить событие через какой нить брокер чтобы снести несуществующий объект из базы
        raise HTTPException

if __name__ == '__main__':
    run(port=int(MEDIA_SERVICE_PORT))

import logging
import socket

import minio
import sqlalchemy
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine
from starlette import status

from core import config
from core.schemas import metadata


class Database:
    engine = create_async_engine(config.DB_DSN, echo=True)

    @classmethod
    async def get(cls):
        try:
            async with cls.engine.connect() as connection:
                yield connection
        except sqlalchemy.exc.InterfaceError as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="нет соединения с базой")
        except socket.gaierror as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="нет соединения с базой")

    @classmethod
    async def init(cls):
        async with Database.engine.connect() as connection:
            # await connection.run_sync(metadata.drop_all)
            await connection.run_sync(metadata.create_all)
            await connection.commit()
        await Database.engine.dispose()


class S3:
    client: minio.Minio = minio.Minio(config.MINIO_ENDPOINT,
                                      config.MINIO_ACCESS_KEY,
                                      config.MINIO_SECRET_KEY,
                                      secure=False,
                                      cert_check=False)

    @classmethod
    def get(cls):
        return cls.client

    @classmethod
    def init(cls, bucket_name):
        if not cls.client.bucket_exists(bucket_name):
            cls.client.make_bucket(bucket_name)

import logging
import socket

import minio
import sqlalchemy
from fastapi import HTTPException, Depends
from minio import Minio
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from core import config
from core.storages import Database, S3


class BaseRepository:
    def __init__(self, connection: AsyncConnection = Depends(Database.get)):
        self.connection = connection

    # @classmethod
    # async def init(cls):
    #     try:
    #         async with Database.engine.connect() as connection:
    #             yield cls(connection)
    #     except sqlalchemy.exc.InterfaceError as e:
    #         logging.exception(e)
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                             detail="нет соединения с базой")
    #     except socket.gaierror as e:
    #         logging.exception(e)
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #                             detail="нет соединения с базой")


class BaseS3Client:
    def __init__(self, client=Depends(S3.get)):
        self.bucket = config.BUCKET_NAME
        self.client: Minio = client

import logging
import uuid
from uuid import UUID

import minio
from fastapi import Depends, UploadFile, HTTPException
from minio.helpers import ObjectWriteResult
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from core import config
from core.misc import transform
from services.memes.aliases import AMem
from services.memes.repository import Repository
from services.memes.s3 import S3


class Handler:
    def __init__(self,
                 repository: Repository = Depends(Repository),
                 client: S3 = Depends(S3)):
        self.repository = repository
        self.client = client

    async def put(self, text: str, file: UploadFile):
        file_id = uuid.uuid4()
        data: dict = {
            AMem.ID: file_id,
            AMem.TITLE: text,
            AMem.ORIGINAL_NAME: file.filename,
            AMem.CONTENT_TYPE: file.content_type,
            AMem.EXT: file.filename.split(".")[-1]
        }
        try:
            db_result = await self.repository.create(data)
            db_result = dict(db_result)
            db_result[AMem.FILE_URL] = f"{config.MEDIA_SERVICE_SOCKET}/{file_id}.{data[AMem.EXT]}"
            s3_result: ObjectWriteResult = await self.client.put(f"{data[AMem.ID]}.{data[AMem.EXT]}", file.file)
            return db_result
        except SQLAlchemyError as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="файл не загружен")
        except minio.S3Error as e:
            logging.exception(e)
            await self.repository.delete(file_id)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="файл не загружен")

    async def get_list(self, skip: int, limit: int):
        result = await self.repository.get_list(skip, limit)
        result = [transform(i) for i in result]
        return result

    async def get_by_id(self, mem_id: UUID):
        result = await self.repository.get_by_id(mem_id)
        return transform(result)

    async def delete(self, mem_id: UUID):
        result = await self.repository.delete(mem_id)
        await self.client.delete(f"{mem_id}.{result[AMem.EXT]}")

    async def update(self, mem_id: UUID, text: str | None, file: UploadFile | None):
        data: dict = {}
        if text:
            data[AMem.TITLE] = text
        if file:
            data[AMem.ORIGINAL_NAME] = file.filename
            data[AMem.CONTENT_TYPE] = file.content_type
            data[AMem.EXT] = file.filename.split(".")[-1]
        if len(data) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="нет данных для обновления")
        try:
            result = await self.repository.update(mem_id, data)
            if file:
                await self.client.put(f"{mem_id}.{data[AMem.EXT]}", file.file)
            return transform(result)
        except HTTPException as e:
            logging.exception(str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="мем не изменен")

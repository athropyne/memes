import asyncio
import logging
from typing import BinaryIO

from fastapi import HTTPException
from starlette import status

from core.interfaces import BaseS3Client
from services.memes.aliases import AMem


class S3(BaseS3Client):
    async def put(self, file_name: str, file: BinaryIO):
        try:
            return await asyncio.to_thread(self.client.put_object,
                                           bucket_name=self.bucket,
                                           object_name=file_name,
                                           data=file,
                                           length=-1,
                                           content_type="application/octet-stream",
                                           part_size=10 * 1024 ** 2,
                                           metadata=None,
                                           sse=None,
                                           progress=None,
                                           num_parallel_uploads=3,
                                           tags=None,
                                           retention=None,
                                           legal_hold=False
                                           )
        except Exception as e:
            logging.exception(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="файл не загружен")

    async def delete(self, name: str):
        try:
            await asyncio.to_thread(self.client.remove_object,
                                    bucket_name=self.bucket,
                                    object_name=name,
                                    version_id=None
                                    )
        except Exception as e:
            logging.exception(e)
            logging.warning("файл не удален из объектного хранилища")

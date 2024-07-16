import asyncio
import logging
from contextlib import asynccontextmanager

import fastapi_cli.cli
import minio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core import config
from core.storages import Database, S3

from routes import routes


@asynccontextmanager
async def lifespan(instance: FastAPI):
    for i in range(1,3):
        try:
            await Database.init()
            break
        except Exception as e:
            logging.error(e)
            logging.warning("попытка повторного подключения к базе")
            if i == 2: raise Exception("подключение к базе не удалось", e)
            await asyncio.sleep(5 * i)
    try:
        S3.init(config.BUCKET_NAME)
    except minio.S3Error as e:
        logging.error(e)
        raise Exception("ошибка создания корзины")
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


for r in routes:
    app.include_router(r)

if __name__ == '__main__':
    fastapi_cli.cli.run(
        port=config.PUBLIC_API_PORT
    )

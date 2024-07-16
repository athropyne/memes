import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import CursorResult, select
from sqlalchemy.exc import NoResultFound
from starlette import status

from core.interfaces import BaseRepository
from core.schemas import memes
from services.memes.aliases import AMem


class Repository(BaseRepository):
    async def create(self, data: dict):
        cursor: CursorResult = await self.connection.execute(
            memes.insert().values(data).returning("*")
        )
        await self.connection.commit()
        return cursor.mappings().one()

    async def delete(self, mem_id: UUID):
        cursor: CursorResult = await self.connection.execute(
            memes.delete().where(memes.c[AMem.ID] == mem_id).returning("*")
        )
        if cursor.rowcount != 1:
            await self.connection.rollback()
            logging.warning("попытка удаления несуществующего файла")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="мем не найден")
        await self.connection.commit()
        return cursor.mappings().one()

    async def get_list(self, skip: int, limit: int):
        cursor: CursorResult = await self.connection.execute(
            select(
                memes.c[AMem.ID],
                memes.c[AMem.TITLE],
                memes.c[AMem.ORIGINAL_NAME],
                memes.c[AMem.EXT]
            ).offset(skip).limit(limit)
        )
        return cursor.mappings().fetchall()

    async def get_by_id(self, mem_id: UUID):
        try:
            cursor: CursorResult = await self.connection.execute(
                memes.select().where(memes.c[AMem.ID] == mem_id)
            )
            return cursor.mappings().one()
        except NoResultFound as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="мем не найден")

    async def update(self, mem_id: UUID, data: dict):
        try:
            cursor: CursorResult = await self.connection.execute(
                memes.update().values(data).where(memes.c[AMem.ID] == mem_id).returning("*")
            )
            if cursor.rowcount != 1:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail="мем не найден")
            await self.connection.commit()
            return cursor.mappings().one()
        except Exception as e:
            logging.exception(str(e))
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="мем не изменен")

from uuid import UUID

from fastapi import APIRouter, Form, UploadFile, File, Depends, Query, Path
from starlette import status

from services.memes.dto import ResponseModel, ShortResponseModel
from services.memes.handler import Handler

router = APIRouter(prefix="/memes")


@router.post("/",
             status_code=status.HTTP_201_CREATED,
             response_model=ResponseModel,
             description="добавить новый мем")
async def add(
        text: str = Form(..., title="какой то текст, название или описание", max_length=300),
        file: UploadFile = File(..., title="медиафайл ( по факту любой, никаких проверок нет )"),
        handler: Handler = Depends(Handler)
):
    return await handler.put(text, file)


@router.get("/",
            response_model=list[ShortResponseModel],
            description="получает список мемов")
async def get_list(
        skip: int = Query(0, title="пропустить"),
        limit: int = Query(30, title="количество"),
        handler: Handler = Depends(Handler)
):
    return await handler.get_list(skip, limit)


@router.get("/{mem_id}",
            response_model=ResponseModel,
            description="получает мем по ID")
async def get_by_id(
        mem_id: UUID = Path(..., title="ID мема (UUID)"),
        handler: Handler = Depends(Handler)
):
    return await handler.get_by_id(mem_id)


@router.put("/{mem_id}",
            response_model=ResponseModel,
            description="изменяет мем по ID. все поля не обязательны. можно опменять как все так и частично")
async def update(
        mem_id: UUID = Path(..., title="ID мема (UUID)"),
        text: str | None = Form(None, title="какой то текст, название или описание", max_length=300),
        file: UploadFile | None = File(None, title="медиафайл ( по факту любой, никаких проверок нет )"),
        handler:Handler = Depends(Handler)
):
    return await handler.update(mem_id, text, file)


@router.delete("/{mem_id}",
               status_code=status.HTTP_204_NO_CONTENT,
               description="удаляет мем по ID")
async def delete(
        mem_id: UUID = Path(..., title="ID мема (UUID)"),
        handler: Handler = Depends(Handler)
):
    return await handler.delete(mem_id)




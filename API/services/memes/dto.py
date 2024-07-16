import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ResponseModel(BaseModel):
    id: UUID = Field(description="ID мема")
    title: str = Field(description="какой то текст, название или описание")
    content_type: str = Field(description="тип контента (аудио, видео, изображение и т д")
    ext: str = Field(description="расширение файла")
    original_name: str = Field(description="оригинальное название файла")
    added_date: datetime.datetime = Field(description="дата добавления")
    url: str = Field(description="ссылка на медиа файл")


class ShortResponseModel(BaseModel):
    id: UUID = Field(description="ID мема")
    title: str = Field(description="какой то текст, название или описание")
    original_name: str = Field(description="оригинальное название файла")
    ext: str = Field(description="расширение файла")
    url: str = Field(description="ссылка на медиа файл")



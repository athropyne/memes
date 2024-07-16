from sqlalchemy import RowMapping

from core import config
from services.memes.aliases import AMem


def transform(arg: RowMapping):
    """преобразует строку из базы в словарь и пихает еще одно поле с урлом"""
    arg = dict(arg)
    arg[AMem.FILE_URL] = f"{config.MEDIA_SERVICE_SOCKET}/{arg[AMem.ID]}.{arg[AMem.EXT]}"
    return arg

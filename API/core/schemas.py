import datetime

from sqlalchemy import MetaData, Table, Column, String, DateTime, UUID

from services.memes.aliases import AMem

metadata = MetaData()

memes = Table(
    "memes",
    metadata,
    Column(AMem.ID, UUID(as_uuid=True), primary_key=True, nullable=False, unique=True),
    Column(AMem.TITLE, String, nullable=False),
    Column(AMem.CONTENT_TYPE, String, nullable=False),
    Column(AMem.EXT, String, nullable=False),
    Column(AMem.ORIGINAL_NAME, String, nullable=False),
    # Column(AMem.FILE_URL, String, nullable=False),
    Column(AMem.ADDED_DATE, DateTime, nullable=False, default=datetime.datetime.now())
)

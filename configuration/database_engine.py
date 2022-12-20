from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from settings.settings_reader import base_settings

POOL_SIZE = 20

async_engine: AsyncEngine = create_async_engine(
    url=base_settings.async_database_url,
    pool_size=POOL_SIZE,
    pool_pre_ping=True,
)

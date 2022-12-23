from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from app.config.config_reader import app_config

POOL_SIZE = 20

async_engine: AsyncEngine = create_async_engine(
    url=app_config.async_database_url,
    pool_size=POOL_SIZE,
    pool_pre_ping=True,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(bind=async_engine) as async_session:
        async with async_session.begin():
            yield async_session

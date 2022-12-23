from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from configuration.database_engine import async_engine


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(bind=async_engine) as async_session:
        async with async_session.begin():
            yield async_session

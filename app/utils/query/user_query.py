from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import UserModel
from app.utils.password import get_password_hash


async def get_user(
    async_session: AsyncSession,
    username: str,
) -> UserModel | None:

    user_query = select(UserModel).where(UserModel.username == username)

    user_result: Result = await async_session.execute(user_query)

    return user_result.scalar_one_or_none()


async def create_user(
    async_session: AsyncSession,
    username: str,
    password: str,
) -> UserModel:

    user = UserModel(
        username=username,
        password_hash=get_password_hash(
            password=password,
        ),
    )
    async_session.add(user)

    await async_session.flush()

    return user

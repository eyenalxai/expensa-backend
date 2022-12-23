from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from lib.password import get_password_hash
from models.models import UserModel


async def get_user(
    async_session: AsyncSession,
    username: str,
) -> UserModel | None:
    """
    Get user by username or user_id.

    Args:
        async_session (AsyncSession): Async database session.
        username (str): Username or user_id.

    Returns:
        UserModel | None: User models or None.
    """
    user_query = select(UserModel).where(UserModel.username == username)

    user_result: Result = await async_session.execute(user_query)

    return user_result.scalar_one_or_none()


async def create_user(
    async_session: AsyncSession,
    username: str,
    password: str,
) -> UserModel:
    """
    Create user.

    Args:
        async_session (AsyncSession): Async database session.
        username (str): Username.
        password (str): Password.

    Returns:
        UserModel: User models.
    """
    user = UserModel(
        username=username,
        password_hash=get_password_hash(
            password=password,
        ),
    )
    async_session.add(user)

    await async_session.flush()

    return user

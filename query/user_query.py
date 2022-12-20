from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from lib.password import get_password_hash
from models.user import UserModel


def build_get_user_query(
    identifier: str | int,
) -> Select:
    """
    Build get user query.

    Args:
        identifier (str | int): Username or user_id.

    Returns:
        Select: User query.

    Raises:
        ValueError: If identifier is not str or int.
    """
    if isinstance(identifier, str):
        return select(UserModel).where(UserModel.username == identifier)

    if isinstance(identifier, int):
        return select(UserModel).where(UserModel.user_id == identifier)

    raise ValueError("Username or user_id must be provided.")


async def get_user(
    async_session: AsyncSession,
    identifier: str | int,
) -> UserModel | None:
    """
    Get user by username or user_id.

    Args:
        async_session (AsyncSession): Async database session.
        identifier (str | int): Username or user_id.

    Returns:
        UserModel | None: User models or None.
    """
    user_query = build_get_user_query(identifier=identifier)

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

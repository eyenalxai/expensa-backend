from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from configuration.logger import logger
from lib.auth.token import decode_jwt_token
from lib.database import get_session
from lib.password import verify_password
from models.models import UserModel
from query.user_query import create_user, get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


async def get_current_user(
    async_session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> UserModel:
    payload = decode_jwt_token(token=token)
    user = await get_user(async_session=async_session, username=payload.sub)

    if user is None:
        logger.error(
            "User with username {username} not found".format(username=payload.sub),
        )
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    return user


async def authenticate_user(
    async_session: AsyncSession,
    username: str,
    password: str,
) -> UserModel:
    user = await get_user(async_session=async_session, username=username)

    if not user:
        return await create_user(
            async_session=async_session,
            username=username,
            password=password,
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from dto.auth import AccessToken
from lib.auth.authenticate import authenticate_user
from lib.auth.token import create_tokens_response, decode_jwt_token
from lib.database import get_session

auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/refresh", response_model=AccessToken)
async def refresh_tokens(
    response: Response,
    refresh_token: str | None = Cookie(default=None),
) -> AccessToken:
    if not refresh_token:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    payload = decode_jwt_token(token=refresh_token)

    return create_tokens_response(
        response=response,
        username=payload.sub,
    )


@auth_router.post("/auth", response_model=AccessToken)
async def auth(
    response: Response,
    auth_data: OAuth2PasswordRequestForm = Depends(),
    async_session: AsyncSession = Depends(get_session),
) -> AccessToken:
    user = await authenticate_user(
        async_session=async_session,
        username=auth_data.username,
        password=auth_data.password,
    )

    return create_tokens_response(response=response, username=user.username)

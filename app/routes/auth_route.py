from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config.config_reader import app_config
from app.schema.user_schema import UserSchemaAdd
from app.utils.auth import authenticate_user
from app.utils.database import get_session
from app.utils.token import AccessToken, create_tokens_response, decode_jwt_token

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/refresh_tokens", response_model=AccessToken)
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


@auth_router.post("/login", response_model=AccessToken)
async def login(
    response: Response,
    auth_data: UserSchemaAdd,
    async_session: AsyncSession = Depends(get_session),
) -> AccessToken:
    user = await authenticate_user(
        async_session=async_session,
        username=auth_data.username,
        password=auth_data.password,
    )

    return create_tokens_response(response=response, username=user.username)


@auth_router.post("/logout")
async def logout(response: Response) -> Response:
    response.delete_cookie(key=app_config.refresh_token_cookie_key)
    response.status_code = 204
    return response

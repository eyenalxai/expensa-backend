from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError, jwt
from jose.exceptions import JWTClaimsError
from pydantic import Field
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

from app.config.config_reader import app_config
from app.utils.immutable import Immutable


class JSONWebToken(Immutable):
    sub: str
    exp: float


class AccessToken(Immutable):
    class Config:
        allow_population_by_field_name = True

    access_token: str = Field(alias="accessToken")
    token_type: str = Field(alias="tokenType", default="bearer")


def create_jwt_token(username: str, expires_delta: timedelta) -> str:
    expire = (datetime.now() + expires_delta).timestamp()
    to_encode = JSONWebToken(sub=username, exp=expire)
    return jwt.encode(
        to_encode.dict(),
        app_config.hashing_secret,
        algorithm=app_config.algorithm,
    )


def create_tokens(username: str) -> tuple[str, str]:
    access_token_expires = timedelta(minutes=app_config.access_token_expire_minutes)
    refresh_token_expires = timedelta(
        minutes=app_config.refresh_token_expire_minutes,
    )

    access_token = create_jwt_token(
        username=username,
        expires_delta=access_token_expires,
    )

    refresh_token = create_jwt_token(
        username=username,
        expires_delta=refresh_token_expires,
    )

    return access_token, refresh_token


def create_tokens_response(response: Response, username: str) -> AccessToken:
    access_token, refresh_token = create_tokens(username=username)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=app_config.refresh_token_expire_minutes * 60,
        httponly=True,
        samesite="strict",
    )

    return AccessToken(access_token=access_token)


def decode_jwt_token(token: str) -> JSONWebToken:
    try:
        return JSONWebToken(
            **jwt.decode(
                token=token,
                key=app_config.hashing_secret,
                algorithms=app_config.algorithms,
            ),
        )
    except (JWTClaimsError, ExpiredSignatureError, JWTError):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

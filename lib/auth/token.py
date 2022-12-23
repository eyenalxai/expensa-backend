from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import ExpiredSignatureError, JWTError, jwt
from jose.exceptions import JWTClaimsError
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

from dto.auth import AccessToken, Token
from settings.settings_reader import base_settings


def create_jwt_token(username: str, expires_delta: timedelta) -> str:
    """
    Create JWT token.

    Args:
        username (str): Username.
        expires_delta (timedelta): Token expires delta.

    Returns:
        str: JWT token.
    """
    expire = (datetime.now() + expires_delta).timestamp()
    to_encode = Token(sub=username, exp=expire)
    return jwt.encode(
        to_encode.dict(),
        base_settings.hashing_secret,
        algorithm=base_settings.algorithm,
    )


def create_tokens(username: str) -> tuple[str, str]:
    """
    Create access and refresh tokens.

    Args:
        username (str): Username.

    Returns:
        tokens (tuple[str, str]): Access and refresh tokens tuple.
    """
    access_token_expires = timedelta(minutes=base_settings.access_token_expire_minutes)
    refresh_token_expires = timedelta(
        minutes=base_settings.refresh_token_expire_minutes,
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
    """
    Create access and refresh tokens.

    Sets refresh token to HttpOnly cookie.
    Returns access token as JSON.

    Args:
        response (Response): Response.
        username (str): User ID.

    Returns:
        AccessToken (AccessToken): Access token.

    """
    access_token, refresh_token = create_tokens(username=username)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=base_settings.refresh_token_expire_minutes * 60,
        httponly=True,
        samesite="strict",
    )

    return AccessToken(access_token=access_token)


def decode_jwt_token(token: str) -> Token:
    """
    Decode JWT token.

    Args:
        token (str): JWT token.

    Returns:
        Token (Token): Decoded token.

    Raises:
        HTTPException: 401 status code if token is invalid.
    """
    try:
        return Token(
            **jwt.decode(
                token=token,
                key=base_settings.hashing_secret,
                algorithms=base_settings.algorithms,
            ),
        )
    except (JWTClaimsError, ExpiredSignatureError, JWTError):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

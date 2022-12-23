from pydantic import Field

from configuration.immutable import Immutable


class Token(Immutable):
    sub: str
    exp: float


class AccessToken(Immutable):
    class Config:  # noqa: D106 Missing docstring in public nested class
        allow_population_by_field_name = True

    access_token: str = Field(alias="accessToken")
    token_type: str = Field(alias="tokenType", default="bearer")

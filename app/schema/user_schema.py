from pydantic import ConstrainedStr, Field, validator

from app.config.config_reader import app_config
from app.utils.immutable import Immutable


class UserSchema(Immutable):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True

    user_id: int = Field(alias="userId")
    username: str


class UserSchemaAdd(Immutable):
    class Username(ConstrainedStr):
        to_lower = True
        strip_whitespace = True

    class Password(ConstrainedStr):
        strip_whitespace = True

    username: Username
    password: Password

    @validator("username")
    def username_must_be_ok(
        cls,  # noqa: N805 first argument of a method should be named 'self'
        v: str,  # noqa: WPS111 Found too short name: v < 2
    ) -> str:
        if len(v) < 1:  # noqa: WPS507 Found useless `len()` compare
            raise ValueError("username is too short")

        if len(v) > app_config.username_length:
            raise ValueError("username is too long")

        return v

    @validator("password")
    def password_must_be_strong_enough(  # noqa: WPS238 Found too many raises
        cls,  # noqa: N805 first argument of a method should be named 'self'
        v: str,  # noqa: WPS111 Found too short name: v < 2
    ) -> str:
        if len(v) < app_config.password_min_length:
            raise ValueError("password is too short")

        if not any(char.isdigit() for char in v):
            raise ValueError("password must contain at least one digit")

        if not any(char.islower() for char in v):
            raise ValueError("password must contain at least one lowercase letter")

        if not any(char.isupper() for char in v):
            raise ValueError("password must contain at least one uppercase letter")

        if not any(not char.isalnum() for char in v):
            raise ValueError("password must contain at least one punctuation symbol")

        return v

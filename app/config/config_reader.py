from pydantic import BaseSettings, Field, validator


class AppConfig(BaseSettings):
    database_url: str = Field(env="DATABASE_URL")
    port: int = Field(env="PORT")
    host: str | None = Field(env="HOST", default="0.0.0.0")
    is_localhost: bool = Field(env="IS_LOCALHOST", default=True)
    frontend_domain: str = Field(env="FRONTEND_DOMAIN")

    algorithm: str = "HS256"
    hashing_secret: str = Field(env="HASHING_SECRET")
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7

    refresh_token_cookie_key: str = "refresh_token"

    category_name_length: int = 16
    password_hash_length: int = 60
    username_length: int = 24
    password_min_length: int = 12

    @property
    def algorithms(self) -> list[str]:
        return [self.algorithm]

    @property
    def async_database_url(self: "AppConfig") -> str:
        async_database_url = self.database_url.replace(
            "postgresql://",
            "postgresql+asyncpg://",
        )

        if not async_database_url.startswith("postgresql+asyncpg://"):
            raise ValueError("async_database_url must start with postgresql+asyncpg://")

        return async_database_url

    @property
    def frontend_origin(self: "AppConfig") -> str:
        if self.is_localhost:
            return "http://{frontend_domain}".format(
                frontend_domain=self.frontend_domain,
            )
        return "https://{frontend_domain}".format(frontend_domain=self.frontend_domain)

    @property
    def allowed_origins(self: "AppConfig") -> list:
        return [self.frontend_origin]

    @validator("database_url")
    def _database_url_must_start_with_postgresql(
        cls: "AppConfig",  # noqa: N805 First argument of a method should be 'self'
        v: str,  # noqa: WPS111 Found too short name
    ) -> str:
        if not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must start with postgresql://")
        return v


app_config = AppConfig()

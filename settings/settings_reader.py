from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    database_url: str = Field(env="DATABASE_URL")
    port: int = Field(env="PORT")
    is_localhost: bool = Field(env="IS_LOCALHOST", default=True)
    frontend_domain: str = Field(env="FRONTEND_DOMAIN")
    hashing_secret: str = Field(env="HASHING_SECRET")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_minutes: int = 60 * 24 * 7

    @property
    def algorithms(self) -> list[str]:
        return [self.algorithm]

    @property
    def async_database_url(self: "Settings") -> str:
        async_database_url = self.database_url.replace(
            "postgresql://",
            "postgresql+asyncpg://",
        )

        if not async_database_url.startswith("postgresql+asyncpg://"):
            raise ValueError("async_database_url must start with postgresql+asyncpg://")

        return async_database_url

    @property
    def frontend_origin(self: "Settings") -> str:
        if self.is_localhost:
            return "http://{frontend_domain}".format(
                frontend_domain=self.frontend_domain,
            )
        return "https://{frontend_domain}".format(frontend_domain=self.frontend_domain)

    @property
    def allowed_origins(self: "Settings") -> list:
        return [self.frontend_origin]

    @validator("database_url")
    def _database_url_must_start_with_postgresql(
        cls: "Settings",  # noqa: N805 First argument of a method should be named 'self'
        v: str,  # noqa: WPS111 Found too short name
    ) -> str:
        if not v.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must start with postgresql://")
        return v


base_settings = Settings()

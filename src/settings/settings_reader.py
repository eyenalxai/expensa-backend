"""Module that contains the Settings class."""

from pydantic import BaseSettings, Field, validator

from settings.settings_utils import parse_boolean


class Settings(BaseSettings):
    """Settings for the application."""

    database_url: str = Field(env="DATABASE_URL")
    port: int = Field(env="PORT")
    is_localhost_value: str | None = Field(env="IS_LOCALHOST")
    frontend_domain: str = Field(env="FRONTEND_DOMAIN")

    @property
    def async_database_url(self: "Settings") -> str:
        """
        Return the database url with the asyncpg driver.

        Returns:
            str: The database url with the asyncpg driver.
        """
        return self.database_url.replace("postgresql://", "postgresql+asyncpg://")

    @property
    def is_localhost(self: "Settings") -> bool:
        """
        Check whether the application is running on localhost.

        Returns:
            bool: Whether the application is running on localhost.

        """
        return parse_boolean(string=self.is_localhost_value)

    @property
    def frontend_origin(self: "Settings") -> str:
        """
        Get the frontend origin.

        Returns:
            str: The frontend origin.

        """
        if self.is_localhost:
            return "http://{frontend_domain}".format(frontend_domain=self.frontend_domain)
        return "https://{frontend_domain}".format(frontend_domain=self.frontend_domain)

    @property
    def allowed_origins(self: "Settings") -> list:
        """
        Get the allowed origins.

        Returns:
            list: The allowed origins.
        """
        return [self.frontend_origin]

    @validator("database_url")
    def _database_url_must_start_correctly(
        self: "Settings",
        database_url: str,
    ) -> str:
        if not database_url.startswith("postgresql://"):
            raise ValueError("DATABASE_URL must start with postgresql://")
        return database_url

    @validator("async_database_url")
    def _async_database_url_must_start_correctly(
        self: "Settings",
        async_database_url: str,
    ) -> str:
        if not async_database_url.startswith("postgresql+asyncpg://"):
            raise ValueError("async_database_url must start with postgresql+asyncpg://")
        return async_database_url


base_settings = Settings()

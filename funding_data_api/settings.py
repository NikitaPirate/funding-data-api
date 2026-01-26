from typing import Any, Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# =============================================================================
# Shared Settings Pattern (multiple apps, common resources)
# =============================================================================
#
# When multiple apps (FDA, FT, ...) share resources like database:
#
#   DB_HOST=localhost           # Shared by all apps
#   FDA_CORS_ALLOW_ORIGINS=*    # App-specific
#
# Use AliasChoices for fallback from prefixed to unprefixed variables:
#
#   class DBSettings(BaseModel):
#       host: str = Field(validation_alias=AliasChoices('FDA_DB_host', 'DB_host'))
#       port: int = Field(validation_alias=AliasChoices('FDA_DB_port', 'DB_port'))
#
# This tries FDA_DB_host first, falls back to DB_host if not found.
# =============================================================================


class DBSettings(BaseModel):
    """Database connection settings."""

    # Connection parts
    host: str
    port: int
    user: str
    password: str
    dbname: str

    # Optional kwargs
    engine_kwargs: dict[str, Any] | None = None
    session_kwargs: dict[str, Any] | None = None

    @property
    def connection_url(self) -> str:
        """Builds TimescaleDB connection URL from parts."""
        return f"timescaledb+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


class CORSSettings(BaseModel):
    """CORS middleware configuration.

    All fields are Optional - None means use middleware default.
    Use to_middleware_kwargs() to pass only explicitly set values.
    """

    allow_origins: list[str] | Literal["*"] | None = None
    allow_origin_regex: str | None = None
    allow_methods: list[str] | Literal["*"] | None = None
    allow_headers: list[str] | Literal["*"] | None = None
    allow_credentials: bool | None = None
    allow_private_network: bool | None = None
    expose_headers: list[str] | None = None
    max_age: int | None = None

    def to_middleware_kwargs(self) -> dict[str, object]:
        """Returns only explicitly set parameters (filters None)."""
        return {k: v for k, v in self.model_dump().items() if v is not None}


class Settings(BaseSettings):
    """Funding Data API configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="FDA_",  # FDA_ prefix for all env vars
        env_nested_delimiter="_",  # _ separator for nested fields
        env_nested_max_split=1,  # Split only once (FDA_CORS_* → cors.*)
    )

    cors: CORSSettings
    db: DBSettings


settings = Settings()  # pyright: ignore[reportCallIssue]

"""Backend's Runtime Configuration contract (task P3-G12-T1).

Backend defines and validates the values it requires here. Values are sourced from the
Platform-delivered Runtime Binding (environment variables prefixed `BACKEND_`); nothing
here is a secret, and no default silently supplies a value the Target requires an
operator to set explicitly.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Backend's complete required Runtime Configuration."""

    model_config = SettingsConfigDict(env_prefix="BACKEND_", extra="forbid")

    # Required: no default. Platform's Runtime Binding must supply this explicitly
    # rather than Backend silently defaulting to a permissive or empty CORS policy.
    cors_allowed_origins: list[str] = Field(
        description="Allowlisted origins for Cross-Origin Resource Sharing."
    )

    host: str = Field(default="0.0.0.0", description="Bind address for the HTTP server.")
    port: int = Field(default=8000, description="Bind port for the HTTP server.")
    api_version: str = Field(default="v1", description="The API Interface's published version.")
    database_instance: str = Field(
        default="general", description="The Database Instance Backend persists through."
    )
    request_timeout_seconds: float = Field(
        default=5.0, gt=0, description="Finite timeout applied to every persistence interaction."
    )
    max_retry_attempts: int = Field(
        default=3, ge=1, description="Bound on automatic retry for a safe or idempotent operation."
    )
    shutdown_timeout_seconds: float = Field(
        default=30.0, gt=0, description="Graceful shutdown boundary from Platform."
    )


def load_settings() -> Settings:
    """Load and validate Settings from the environment, failing fast when invalid."""
    return Settings()  # type: ignore[call-arg]

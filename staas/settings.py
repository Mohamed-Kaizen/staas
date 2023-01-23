"""Settings file for staas."""
from typing import Literal

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Base Settings."""

    PROJECT_NAME: str = "Staas"

    PROJECT_DESCRIPTION: str = "A auth service that work with supertokens"

    PROJECT_VERSION: str = "0.1.0"

    DOCS_URL: str = "/docs"

    REDOC_URL: str = "/redoc"

    OPENAPI_URL: str = "/openapi.json"

    ALLOWED_HOSTS: list[str] = ["*"]

    CORS_ORIGINS: list[str] = ["*"]

    CORS_ALLOW_METHODS: list[str] = ["*"]

    CORS_ALLOW_HEADERS: list[str] = ["*"]

    CORS_ALLOW_CREDENTIALS: bool = True

    DEBUG: bool = True

    PORT: int = 8000

    BACKEND_URL: str = "http://localhost:8000"

    FRONTEND_URL: str = "http://localhost:3000"

    BACKEND_BASE_PATH: str = "/"

    FRONTEND_BASE_PATH: str = "/auth"

    SUPER_TOKENS_URI: str = "http://localhost:3567"

    GITHUB_CLIENT_ID: str | None

    GITHUB_CLIENT_SECRET: str | None

    GOOGLE_CLIENT_ID: str | None

    GOOGLE_CLIENT_SECRET: str | None

    APPLE_CLIENT_ID: str | None

    APPLE_CLIENT_KEY_ID: str | None

    APPLE_CLIENT_TEAM_ID: str | None

    APPLE_CLIENT_PRIVATE_KEY: str | None

    FACEBOOK_CLIENT_ID: str | None

    FACEBOOK_CLIENT_SECRET: str | None

    DISCORD_CLIENT_ID: str | None

    DISCORD_CLIENT_SECRET: str | None

    EMAIL_VERIFICATION: Literal["REQUIRED", "OPTIONAL"] = "REQUIRED"

    HASURA_ALLOWED_ROLES: list[str] = ["user", "me"]

    HASURA_DEFAULT_ROLE: str = "user"

    class Config:
        """Override the default config."""

        env_file = ".env"


settings = Settings()

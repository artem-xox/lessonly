from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv(usecwd=True), override=True)


class Settings(BaseSettings):
    """
    Central app configuration.
    - Reads from environment (already populated by dotenv above).
    - Provides helpers for wiring external clients (OpenAI).
    """

    # pydantic-settings config
    model_config = SettingsConfigDict(
        env_prefix="LESSONLY_",  # allows LESSONLY_* envs
        extra="ignore",
    )

    # ---- App basics ----
    env: Literal["dev", "staging", "prod"] = "dev"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    # ---- Paths ----
    base_dir: Path = Field(default_factory=lambda: Path.cwd())
    data_dir: Path = Field(
        default_factory=lambda: os.path.join(Path.cwd(), Path("data"))
    )
    cache_dir: Path = Field(
        default_factory=lambda: os.path.join(Path.cwd(), Path(".cache/lessonly"))
    )

    # ---- OpenAI (accept both plain OPENAI_* and LESSONLY_OPENAI_* envs) ----
    openai_api_key: SecretStr = Field(
        ...,
        validation_alias=AliasChoices("OPENAI_API_KEY"),
    )
    openai_api_timeout: int = Field(
        default=60,
    )

    # Convenience: ensure dirs exist (safe on repeated calls)
    def ensure_dirs(self) -> None:
        for p in (self.data_dir, self.cache_dir):
            Path(p).mkdir(parents=True, exist_ok=True)

    # Helper: build and return an OpenAI client
    def make_openai_client(self):
        """
        Instantiate and return the OpenAI client.
        We set env vars first so the SDK can pick them up no matter the version.
        """
        os.environ.setdefault("OPENAI_API_KEY", self.openai_api_key.get_secret_value())

        # Lazy import to avoid hard dependency during tests
        from openai import OpenAI  # type: ignore

        client = OpenAI(timeout=self.openai_api_timeout)
        return client

    # Optional: dump a redacted view for debugging
    def pretty(self) -> str:
        return self.model_dump_json(indent=2)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings instance for the whole app."""
    settings = Settings()
    settings.ensure_dirs()
    return settings


# Handy manual check:
if __name__ == "__main__":
    print(get_settings().pretty())

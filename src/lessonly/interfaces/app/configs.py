import os
from pathlib import Path

from dotenv import load_dotenv


def load_env_file(env_file_path: str = ".env") -> None:
    env_path = Path(env_file_path)
    if env_path.exists():
        load_dotenv(env_path, override=False)


# Load .env file when module is imported
load_env_file()


def get_streamlit_config() -> dict:
    return {
        "page_title": os.getenv("STREAMLIT_PAGE_TITLE", "Lessonly"),
        "page_icon": os.getenv("STREAMLIT_PAGE_ICON", "📙"),
        "layout": os.getenv("STREAMLIT_LAYOUT", "wide"),
    }


def get_app_config() -> dict:
    """
    Initialize general application configuration from environment variables.

    Environment variables:
    - APP_ENV: Environment (development, production, etc.)
    - APP_DEBUG: Debug mode (default: False)
    - APP_LOG_LEVEL: Logging level (default: INFO)

    Returns:
        dict: Application configuration settings
    """
    return {
        "env": os.getenv("APP_ENV", "development"),
        "debug": os.getenv("APP_DEBUG", "false").lower() == "true",
        "log_level": os.getenv("APP_LOG_LEVEL", "INFO"),
    }


# Convenience function to get all configs at once
def get_all_configs() -> dict:
    """
    Get all configuration objects in a single call.

    Returns:
        dict: Dictionary containing all configuration objects
    """
    return {
        "streamlit": get_streamlit_config(),
        "app": get_app_config(),
    }

import re

import streamlit as st

from src.lessonly.interfaces.app.configs import get_streamlit_config
from src.lessonly.settings import get_settings


def slugify(text: str) -> str:
    """
    Convert a string to a slug.
    """

    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


def setup_streamlit_page() -> None:
    """
    Apply a consistent Streamlit page configuration across all pages.
    Must be called before any other Streamlit commands on a page.
    """
    cfg = get_streamlit_config()
    st.set_page_config(
        page_title=cfg["page_title"],
        page_icon=cfg["page_icon"],
        layout=cfg["layout"],
    )


def ensure_openai_client():
    """
    Create and return an OpenAI client using application settings.
    Shows a Streamlit error and stops execution if initialization fails.
    """
    settings = get_settings()
    try:
        client = settings.make_openai_client()
        return client
    except Exception:
        st.error(
            "OpenAI client could not be initialized. Ensure `OPENAI_API_KEY` (or `LESSONLY_OPENAI_API_KEY`) is set."
        )
        st.stop()

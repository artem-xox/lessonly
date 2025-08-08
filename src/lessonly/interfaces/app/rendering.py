from __future__ import annotations

import time

import streamlit as st

from src.lessonly.domain.models.lesson import LessonBlock
from src.lessonly.interfaces.app.utils import slugify


def render_block(block: LessonBlock) -> None:
    """Render a single lesson block in a visually pleasant way."""

    st.divider()

    meta_cols = st.columns([1, 1, 2])
    with meta_cols[0]:
        st.metric(label="Type", value=block.type.value.title())
    with meta_cols[1]:
        st.metric(label="Level", value=block.info.level.value)
    with meta_cols[2]:
        st.metric(label="Topic", value=block.info.topic)

    st.divider()

    with st.container(border=True):
        if isinstance(block.content, str):
            st.markdown(block.content)
        else:
            for item in block.content:
                st.markdown(f"- {item}")

    # Download convenience
    md = block.content if isinstance(block.content, str) else "\n".join(block.content)
    filename = (
        f"{block.info.level.value}_{block.type.value}_{slugify(block.info.topic)}.md"
    )
    st.download_button(
        "Download as .md",
        data=md.encode("utf-8"),
        file_name=filename,
        mime="text/markdown",
        key=f"download-btn-{block.id}-{time.time()}",
        use_container_width=True,
    )

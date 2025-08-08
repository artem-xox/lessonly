from __future__ import annotations

from dataclasses import asdict
from typing import Optional, cast

import streamlit as st

from src.lessonly.agents.intructionalist.agent import InstructionalistAgent
from src.lessonly.domain.models.lesson import (
    LessonBlock,
    LessonBlockRequest,
    LessonBlockType,
    LessonInfo,
    LessonLevel,
)
from src.lessonly.interfaces.app.rendering import render_block
from src.lessonly.interfaces.app.utils import ensure_openai_client, setup_streamlit_page

# Apply page config as the very first Streamlit call on this page
setup_streamlit_page()


def _sidebar_form() -> tuple[
    Optional[LessonBlockType], Optional[LessonLevel], str, Optional[str], bool
]:
    with st.sidebar.form("lesson_request_form"):
        block_type = st.selectbox(
            "Block type",
            options=list(LessonBlockType),
            format_func=lambda lt: lt.value.title(),
        )
        level = st.selectbox(
            "Level",
            options=list(LessonLevel),
            index=3,  # B2 is the default level
            format_func=lambda lv: lv.value,
        )
        topic = st.text_area("Topic", height=60, value="linkin park")
        comment = st.text_area("Comment", height=100)
        submitted = st.form_submit_button("Generate", use_container_width=True)
    return (
        cast(Optional[LessonBlockType], block_type),
        cast(Optional[LessonLevel], level),
        topic,
        comment,
        submitted,
    )


def main() -> None:
    st.write("# One-block Lesson Generator")

    # Sidebar form
    block_type, level, topic, comment, submitted = _sidebar_form()

    # Persist last result in session to avoid re-calling the model on reruns
    if "last_block" not in st.session_state:
        st.session_state.last_block = None
        st.session_state.last_request = None

    if submitted:
        if not topic.strip():
            st.warning("Please provide a topic.")
            st.stop()

        client = ensure_openai_client()
        agent = InstructionalistAgent(llm=client)
        request = LessonBlockRequest(
            type=cast(LessonBlockType, block_type),
            info=LessonInfo(
                title=topic.strip(),
                topic=topic.strip(),
                level=cast(LessonLevel, level),
            ),
            comment=comment.strip() if comment else None,
        )

        with st.spinner("Generating lesson block..."):
            block = agent.generate_lesson_block(request)

        st.session_state.last_block = block
        st.session_state.last_request = asdict(request)

    # Render last result if available
    last_block: Optional[LessonBlock] = st.session_state.get("last_block")
    last_req_dict: Optional[dict] = st.session_state.get("last_request")
    if last_block and last_req_dict:
        render_block(last_block)
    else:
        st.info("Use the sidebar to generate a lesson block.")


if __name__ == "__main__":
    main()

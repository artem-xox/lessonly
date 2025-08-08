from __future__ import annotations

from dataclasses import asdict
from typing import Optional, cast

import streamlit as st

from src.lessonly.agents.intructionalist.agent import InstructionalistAgent
from src.lessonly.domain.models.defs import LessonBlockType, LessonLevel
from src.lessonly.domain.models.lesson import LessonBlock, LessonBlockRequest
from src.lessonly.interfaces.app.utils import setup_streamlit_page, slugify
from src.lessonly.settings import get_settings

# Apply page config as the very first Streamlit call on this page
setup_streamlit_page()


def render_block(block: LessonBlock, *, level: LessonLevel, topic: str) -> None:
    """Render a single lesson block in a visually pleasant way."""

    st.divider()

    meta_cols = st.columns([1, 1, 2])
    with meta_cols[0]:
        st.metric(label="Type", value=block.type.value.title())
    with meta_cols[1]:
        st.metric(label="Level", value=level.value)
    with meta_cols[2]:
        st.metric(label="Topic", value=topic)

    st.divider()

    with st.container(border=True):
        if isinstance(block.content, str):
            st.markdown(block.content)
        else:
            for item in block.content:
                st.markdown(f"- {item}")

    # Download convenience
    md = block.content if isinstance(block.content, str) else "\n".join(block.content)
    filename = f"{level.value}_{block.type.value}_{slugify(topic)}.md"
    st.download_button(
        "Download as .md",
        data=md.encode("utf-8"),
        file_name=filename,
        mime="text/markdown",
        use_container_width=True,
    )


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


def _ensure_openai_client():
    settings = get_settings()
    try:
        client = settings.make_openai_client()
        return client
    except Exception:  # pydantic or client init errors
        st.error(
            "OpenAI client could not be initialized. Ensure `OPENAI_API_KEY` (or `LESSONLY_OPENAI_API_KEY`) is set."
        )
        st.stop()


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

        client = _ensure_openai_client()
        agent = InstructionalistAgent(llm=client)
        request = LessonBlockRequest(
            type=cast(LessonBlockType, block_type),
            level=cast(LessonLevel, level),
            topic=topic.strip(),
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
        render_block(
            last_block,
            level=LessonLevel(last_req_dict["level"]),
            topic=last_req_dict["topic"],
        )
    else:
        st.info("Use the sidebar to generate a lesson block.")


if __name__ == "__main__":
    main()

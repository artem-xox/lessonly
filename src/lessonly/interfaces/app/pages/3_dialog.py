from __future__ import annotations

from typing import List

import streamlit as st

from src.lessonly.agents.manager.agent import ManagerAgent
from src.lessonly.domain.models.defs import Role
from src.lessonly.domain.models.dialog import ChatRequest, Dialog, Message
from src.lessonly.interfaces.app.utils import ensure_openai_client, setup_streamlit_page

# Apply page config as the very first Streamlit call on this page
setup_streamlit_page()


def _init_memory() -> None:
    if "dialog" not in st.session_state:
        st.session_state.dialog = Dialog(messages=[])


def _render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## Controls")
        if st.button("Clear conversation", use_container_width=True):
            st.session_state.dialog = Dialog(messages=[])
            st.rerun()
        st.markdown("This chat is stored in-memory for the current session only.")


def _render_assistant_hidden_message(message: Message) -> None:
    """Render assistant message hidden behind a click-to-reveal popover (fallback to expander).

    Also render a separate bordered block with a short text "hello world".
    """
    popover_ctx = st.popover("Click to reveal your lesson", use_container_width=True)

    # Now the hidden content is the short text, and the visible block shows the bot's message
    with popover_ctx:
        st.write("hello world")

    # Visible assistant message
    with st.container(border=True):
        st.write(message.text)


def _render_history(messages: List[Message]) -> None:
    for m in messages:
        if m.role is Role.ASSISTANT:
            with st.chat_message(Role.ASSISTANT.value):
                _render_assistant_hidden_message(m)
        elif m.role is Role.USER:
            with st.chat_message(Role.USER.value):
                st.write(m.text)
        else:
            with st.chat_message(m.role.value):
                st.write(m.text)


def main() -> None:
    st.write("# Dialog")

    _init_memory()
    _render_sidebar()

    dialog: Dialog = st.session_state.dialog
    _render_history(dialog.messages)

    prompt = st.chat_input("Text me what you want to create…")
    if prompt:
        # Immediately show user's message
        user_msg = Message(role=Role.USER, text=prompt)
        dialog.messages.append(user_msg)
        with st.chat_message(Role.USER.value):
            st.write(prompt)

        # Call agent with full context and show a live placeholder while thinking
        client = ensure_openai_client()
        agent = ManagerAgent(llm=client)
        with st.spinner("Thinking…"):
            response = agent.chat(ChatRequest(messages=dialog.messages))
            assistant_msg = response.messages[-1]

        # Persist assistant message and rerun so it renders once via history
        dialog.messages.append(assistant_msg)
        st.rerun()


if __name__ == "__main__":
    main()

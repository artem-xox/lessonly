import streamlit as st

from src.lessonly.interfaces.app.utils import setup_streamlit_page

setup_streamlit_page()

st.write("# Lessonly")

st.markdown(
    """
✨ AI-powered app leveraging GPT technology to automatically create customized, engaging English lesson plans for students and teachers.

---

### Pages
- 🧩 **Block**: Generate a single lesson block (vocabulary, grammar, activity, reading, homework) for a chosen level and topic.
- 📚 **Lesson**: Generate a complete lesson composed of multiple blocks tailored to a level and theme.
- 💬🤖 **Dialog**: Chat with an AI lesson manager to refine, expand, or regenerate parts of a lesson interactively.
"""
)

from openai import OpenAI

from src.lessonly.domain.models.lesson import Lesson, LessonRequest
from src.lessonly.shared.logging import get_logger


class OrchestratorAgent:
    """
    Main agent that generates Lesson based on LessonRequest.
    """

    MODEL = "gpt-5-mini"

    def __init__(self, llm: OpenAI):
        self.llm = llm
        self.logger = get_logger(__name__)

    def generate_lesson_block(self, lesson_request: LessonRequest) -> Lesson:
        pass

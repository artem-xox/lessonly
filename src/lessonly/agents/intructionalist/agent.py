from openai import OpenAI

from src.lessonly.agents.intructionalist import prompts
from src.lessonly.domain.models.lesson import LessonBlock, LessonBlockRequest
from src.lessonly.shared.logging import get_logger, log_calls


class InstructionalistAgent:
    """
    Agent that generates LessonBlocks based on LessonRequests.
    """

    MODEL = "gpt-5-mini"

    def __init__(self, llm: OpenAI):
        self.llm = llm
        self.logger = get_logger(__name__)

    @log_calls(
        before=lambda self, lesson_request: (
            f"Generating lesson block | type={lesson_request.type} "
            f"level={lesson_request.info.level.value} topic={lesson_request.info.topic}"
        ),
        after=lambda result, self, lesson_request: (
            f"Lesson block generated | uuid={result.id} block_type={result.type} content_length={len(result.content)}"
        ),
    )
    def generate_lesson_block(self, lesson_request: LessonBlockRequest) -> LessonBlock:
        prompt = prompts.prompt_for(lesson_request)

        messages = [
            {
                "role": "system",
                "content": prompts.SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]
        if lesson_request.comment:
            messages.append(
                {
                    "role": "user",
                    "content": prompts.ADDITIONAL_INSTRUCTIONS.format(
                        comment=lesson_request.comment
                    ),
                }
            )

        response = self.llm.chat.completions.create(
            model=self.MODEL,
            messages=messages,
        )

        content = response.choices[0].message.content.strip()

        return LessonBlock(
            type=lesson_request.type,
            info=lesson_request.info,
            content=content,
        )

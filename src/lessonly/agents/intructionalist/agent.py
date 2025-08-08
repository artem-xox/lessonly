import uuid

from openai import OpenAI

from src.lessonly.agents.intructionalist import prompts
from src.lessonly.domain.models.lesson import LessonBlock, LessonBlockRequest


class InstructionalistAgent:
    """
    Agent that generates LessonBlocks based on LessonRequests.
    """

    MODEL = "gpt-5-mini"

    def __init__(self, llm: OpenAI):
        self.llm = llm

    def generate_lesson_block(self, lesson_request: LessonBlockRequest) -> LessonBlock:
        prompt = prompts.prompt_for(
            lesson_request.type,
            level=lesson_request.level.value,
            topic=lesson_request.topic,
            target_grammar="Second Conditional",
            motion=f"This house believes {lesson_request.topic}",
        )

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
            id=str(uuid.uuid4()),
            type=lesson_request.type,
            content=content,
        )

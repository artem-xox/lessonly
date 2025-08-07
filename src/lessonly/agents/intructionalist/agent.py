import uuid

from openai import OpenAI

from src.lessonly.agents.intructionalist.prompts import prompt_for
from src.lessonly.domain.models.lesson import LessonBlock, LessonBlockRequest


class InstructionalistAgent:
    """
    Agent that generates LessonBlocks based on LessonRequests.
    """

    MODEL = "gpt-5"

    def __init__(self, llm: OpenAI):
        self.llm = llm

    def generate_lesson_block(self, lesson_request: LessonBlockRequest) -> LessonBlock:
        prompt = prompt_for(
            lesson_request.type,
            level=lesson_request.level.value,
            topic=lesson_request.topic,
            target_grammar="Second Conditional",
            motion=f"This house believes {lesson_request.topic}",
        )

        response = self.llm.chat.completions.create(
            model=self.MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced ESL teacher.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        content = response.choices[0].message.content.strip()

        return LessonBlock(
            id=str(uuid.uuid4()),
            type=lesson_request.type,
            content=content,
        )

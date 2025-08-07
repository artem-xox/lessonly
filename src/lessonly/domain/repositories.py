from typing import Protocol

from src.lessonly.domain.models.lesson import (
    Lesson,
    LessonBlock,
    LessonBlockRequest,
    LessonRequest,
)


class LessonRepository(Protocol):
    def create_lesson(self, lesson: LessonRequest) -> Lesson: ...


class LessonBlockRepository(Protocol):
    def create_lesson_block(self, lesson_block: LessonBlockRequest) -> LessonBlock: ...

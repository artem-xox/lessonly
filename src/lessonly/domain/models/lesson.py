from __future__ import annotations

from dataclasses import dataclass

from src.lessonly.domain.models.defs import LessonBlockType, LessonLevel


@dataclass
class Lesson:
    title: str
    theme: str
    level: LessonLevel

    blocks: list[LessonBlock]

    def add_block(self, block: LessonBlock) -> None:
        self.blocks.append(block)

    def print_blocks(self) -> None:
        for block in self.blocks:
            print(block)


@dataclass
class LessonBlock:
    id: str
    type: LessonBlockType
    content: str | list[str]

    def __str__(self) -> str:
        return f"LessonBlock(id={self.id}, type={self.type}, content={self.content})"

    def __repr__(self) -> str:
        return f"LessonBlock(id={self.id}, type={self.type}, content={self.content})"


@dataclass
class LessonRequest:
    title: str
    level: LessonLevel
    topic: str


@dataclass
class LessonBlockRequest:
    type: LessonBlockType
    level: LessonLevel
    topic: str
    comment: str | None = None

    target_grammar: str | None = None
    word_count: int | None = None
    num_items: int | None = None
    minutes: int | None = None

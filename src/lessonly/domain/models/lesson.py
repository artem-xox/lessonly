from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from src.lessonly.domain.models.defs import LessonBlockType, LessonLevel


@dataclass
class LessonInfo:
    title: str
    topic: str
    level: LessonLevel


@dataclass
class Lesson:
    info: LessonInfo
    blocks: list[LessonBlock]

    def add_block(self, block: LessonBlock) -> None:
        self.blocks.append(block)

    def print_blocks(self) -> None:
        for block in self.blocks:
            print(block)


@dataclass
class LessonBlock:
    type: LessonBlockType
    info: LessonInfo
    content: str | list[str]

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def __str__(self) -> str:
        return f"LessonBlock(id={self.id}, type={self.type}, content={self.content})"

    def __repr__(self) -> str:
        return f"LessonBlock(id={self.id}, type={self.type}, content={self.content})"

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = str(uuid.uuid4())


@dataclass
class LessonRequest:
    title: str
    topic: str
    level: LessonLevel


@dataclass
class LessonBlockRequest:
    type: LessonBlockType
    info: LessonInfo
    comment: str | None = None

    target_grammar: str | None = None
    word_count: int | None = None
    num_items: int | None = None
    minutes: int | None = None

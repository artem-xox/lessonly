from __future__ import annotations

from dataclasses import dataclass

from lessonly.domain.models.defs import Role
from lessonly.domain.models.lesson import Lesson


@dataclass
class Message:
    role: Role
    text: str
    content: Context | None = None


@dataclass
class Context:
    lesson: Lesson


@dataclass
class ChatRequest:
    messages: list[Message]


@dataclass
class ChatResponse:
    messages: list[Message]

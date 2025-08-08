from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from src.lessonly.domain.models.defs import Role
from src.lessonly.domain.models.lesson import LessonBlock


@dataclass
class Message:
    role: Role
    text: str
    context: Context | None = None


@dataclass
class Context:
    block: LessonBlock


@dataclass
class ChatRequest:
    messages: list[Message]


@dataclass
class ChatResponse:
    messages: list[Message]


@dataclass
class Dialog:
    messages: list[Message]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

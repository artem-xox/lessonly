import argparse
import json
import os
from pathlib import Path
from typing import List

from openai import OpenAI

from src.lessonly.agents.intructionalist.agent import InstructionalistAgent
from src.lessonly.domain.models.lesson import (
    Lesson,
    LessonBlockRequest,
    LessonBlockType,
    LessonLevel,
)
from src.lessonly.settings import get_settings  # loads OPENAI_API_KEY (env or .env)

settings = get_settings()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Lessonly Instructionalist — quick CLI to generate lesson blocks."
    )
    parser.add_argument(
        "--topic", required=True, help='Lesson topic, e.g. "Environmental Protection"'
    )
    parser.add_argument(
        "--title", default=None, help="Lesson title (defaults to '<topic> — <level>')"
    )
    parser.add_argument(
        "--level",
        default="B2",
        choices=[lvl.value for lvl in LessonLevel],
        help="CEFR level",
    )
    parser.add_argument(
        "--blocks",
        nargs="+",
        default=["vocabulary"],
        choices=[bt.value for bt in LessonBlockType],
        help="One or more block types to generate",
    )
    parser.add_argument(
        "--out", default=None, help="Optional output path (.md or .json)"
    )
    return parser.parse_args()


def ensure_openai_client() -> OpenAI:
    api_key = getattr(settings, "OPENAI_API_KEY", None) or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Missing OPENAI_API_KEY. Set it in your environment or settings.py."
        )
    return OpenAI(api_key=api_key)


def pretty_print_lesson(lesson: Lesson) -> None:
    bar = "─" * 80
    print(
        f"\n{bar}\nTITLE: {lesson.title}\nTOPIC: {lesson.theme}\nLEVEL: {lesson.level.value}\n{bar}"
    )
    for block in lesson.blocks:
        print(f"\n[{block.type.value.upper()}]  id={block.id}")
        print("-" * 80)
        if isinstance(block.content, list):
            for i, line in enumerate(block.content, 1):
                print(f"{i}. {line}")
        else:
            print(block.content)


def lesson_to_dict(lesson: Lesson) -> dict:
    return {
        "title": lesson.title,
        "topic": lesson.theme,
        "level": lesson.level.value,
        "blocks": [
            {
                "id": b.id,
                "type": b.type.value,
                "content": b.content,
            }
            for b in lesson.blocks
        ],
    }


def lesson_to_markdown(lesson: Lesson) -> str:
    lines: List[str] = []
    lines.append(f"# {lesson.title}")
    lines.append("")
    lines.append(f"**Topic:** {lesson.theme}  ")
    lines.append(f"**Level:** {lesson.level.value}")
    lines.append("")
    for block in lesson.blocks:
        lines.append(f"## {block.type.value.title()}")
        lines.append("")
        if isinstance(block.content, list):
            for item in block.content:
                lines.append(f"- {item}")
            lines.append("")
        else:
            lines.append(block.content)
            lines.append("")
    return "\n".join(lines).strip() + "\n"


def main():
    args = parse_args()

    level = LessonLevel(args.level)
    blocks = [LessonBlockType(b) for b in args.blocks]
    title = args.title or f"{args.topic} — {level.value}"

    # Init LLM + agent
    llm = ensure_openai_client()
    agent = InstructionalistAgent(llm=llm)

    # Build lesson and generate blocks
    lesson = Lesson(title=title, theme=args.topic, level=level, blocks=[])
    for bt in blocks:
        req = LessonBlockRequest(topic=args.topic, level=level, type=bt)
        block = agent.generate_lesson_block(req)
        lesson.add_block(block)

    # Print to console
    pretty_print_lesson(lesson)

    # Optionally save
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        if out_path.suffix.lower() == ".json":
            out_path.write_text(
                json.dumps(lesson_to_dict(lesson), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        else:
            # default to markdown if not .json
            out_path.write_text(lesson_to_markdown(lesson), encoding="utf-8")
        print(f"\nSaved to: {out_path.resolve()}")


if __name__ == "__main__":
    main()

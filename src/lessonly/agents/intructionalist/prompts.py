from src.lessonly.domain.models.defs import LessonBlockType
from src.lessonly.domain.models.lesson import LessonBlockRequest

SYSTEM_PROMPT = (
    "You are a 10-year veteran ESL educator. Create CEFR-aligned English teaching content that is clear, concise, and classroom-ready. "
    "Use natural, contemporary English; avoid ambiguity and filler. Always include model language and answer keys when tasks require them. "
    "Default to Markdown with short sections and bullet points. "
    "DO NOT INCLUDE ANY OTHER TEXT (especcially the title, level, or type) THAT IS NOT PART OF THE CONTENT."
)

ADDITIONAL_INSTRUCTIONS = (
    "I also have a very important comment. Please use it with the highest priority to guide your response. "
    "Comment: {comment}"
)


PROMPTS: dict[LessonBlockType, str] = {
    LessonBlockType.VOCABULARY: (
        'Generate a CEFR {level} vocabulary block on "{topic}" with 5 items. For each provide '
        "brief CEFR-appropriate definition including 1 natural example sentence. English only."
    ),
    LessonBlockType.GRAMMAR: (
        'Create a CEFR {level} grammar block on "{target_grammar}" within the topic "{topic}". '
        "Include: (1) one-paragraph explanation (form + use), (2) 3 minimal-pair examples (✔/✖), "
        "(3) 6 controlled-practice sentences (gap-fill/transform), (4) 2 short freer prompts. Provide an answer key. English only."
    ),
    LessonBlockType.READING: (
        'Write a CEFR {level} reading passage (~10 words) on "{topic}". Then add: 2 gist questions, 4 detail '
        "questions, 2 vocabulary-in-context items (underline the word). Finish with a 2-sentence model answer for the gist. "
        "Provide an answer key. English only."
    ),
    LessonBlockType.SPEAKING: (
        'Create a CEFR {level} speaking block on "{topic}". Include: (1) 6 conversation prompts escalating in difficulty, '
        "(2) 1 role-play scenario with clear roles and goal, (3) 6 useful phrases/functions (e.g., asking for opinions, agreeing, "
        "hedging). Keep instructions concise. English only."
    ),
    LessonBlockType.DEBATE: (
        'Design a CEFR {level} debate task on "{motion}". Provide: (1) a neutral, 2-sentence background, (2) 3 arguments For '
        "and 3 Against (each with 1 supporting example), (3) a 3-step debate procedure and timing, (4) 6 academic phrases for "
        "debating. English only."
    ),
    LessonBlockType.QUIZ: (
        'Create a CEFR {level} quiz for "{topic}" with 5 multiple-choice questions (A–D). Mix reading/vocab/grammar '
        "comprehension. Keep stems clear, distractors plausible, only one correct answer per item. After the items, output an "
        "answer key with brief 1-line rationales. English only."
    ),
    LessonBlockType.WARMUP: (
        'Create a 2-minute warm-up for CEFR {level} on "{topic}". '
        "Include: (1) 3 short discussion questions that build schema, (2) 1 quick pair activity, "
        "(3) 3 target phrases students might use. Keep it engaging and concise. English only."
    ),
}


def prompt_for(lesson_request: LessonBlockRequest) -> str:
    """Build a prompt string for the given lesson block request.

    The function hides individual formatting parameters behind the
    `LessonBlockRequest` object, deriving sensible defaults where needed.
    """
    template = PROMPTS[lesson_request.type]

    # Provide a comprehensive kwargs set; unused keys are ignored by str.format
    kwargs = {
        "level": lesson_request.info.level.value,
        "topic": lesson_request.info.topic,
        # Default grammar target if not provided
        "target_grammar": lesson_request.target_grammar or "First Conditional",
        # Debate motion derived from topic by default
        "motion": f"This house believes {lesson_request.info.topic}",
    }

    return template.format(**kwargs)

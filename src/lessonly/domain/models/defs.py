from enum import Enum


class LessonBlockType(Enum):
    # Warmup – quick activity to get students engaged.
    WARMUP = "warmup"

    # Vocabulary – topic-specific words + example sentences.
    VOCABULARY = "vocabulary"

    # Grammar – short explanation + practice tasks.
    GRAMMAR = "grammar"

    # Reading Comprehension – short text + understanding questions.
    READING = "reading"

    # Listening Comprehension – audio/video clip + questions.
    LISTENING = "listening"

    # Speaking Practice – conversation prompts or role-play.
    SPEAKING = "speaking"

    # Debate – discussion of a topic with opposing views.
    DEBATE = "debate"

    # Quiz – multiple-choice questions.
    QUIZ = "quiz"


class LessonLevel(str, Enum):
    # Beginner – can understand and use very basic expressions and phrases.
    A1 = "A1"

    # Elementary – can understand sentences and frequently used expressions.
    A2 = "A2"

    # Pre-Intermediate – can handle basic communication in familiar situations.
    B1 = "B1"

    # Intermediate – can interact with a degree of fluency and spontaneity.
    B2 = "B2"

    # Upper Intermediate – can understand complex texts and express ideas fluently.
    C1 = "C1"

    # Advanced – can understand virtually everything and express themselves precisely.
    C2 = "C2"

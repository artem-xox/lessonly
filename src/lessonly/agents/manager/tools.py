CREATE_LESSON_BLOCK_TOOL_NAME = "create_lesson_block"

CREATE_LESSON_BLOCK_TOOL = {
    "type": "function",
    "function": {
        "name": CREATE_LESSON_BLOCK_TOOL_NAME,
        "description": "Create a lesson block using the Instructionalist agent. Manager should not write lesson content itself.",
        "parameters": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "description": "Lesson block type",
                    "enum": [
                        "vocabulary",
                        "grammar",
                        "reading",
                        "listening",
                        "speaking",
                        "debate",
                        "quiz",
                        "warmup",
                    ],
                },
                "info": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "Lesson title (optional; defaults to topic)",
                        },
                        "topic": {"type": "string", "description": "Lesson topic"},
                        "level": {
                            "type": "string",
                            "description": "Learner level",
                            "enum": ["A1", "A2", "B1", "B2", "C1", "C2"],
                        },
                    },
                    "required": ["topic", "level"],
                    "additionalProperties": False,
                },
                "comment": {
                    "type": ["string", "null"],
                    "description": "Optional. Only include if explicitly provided by the user; do not synthesize or paraphrase.",
                },
            },
            "required": ["type", "info"],
            "additionalProperties": False,
        },
    },
}

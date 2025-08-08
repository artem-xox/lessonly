import json

from openai import OpenAI

from src.lessonly.agents.intructionalist.agent import InstructionalistAgent
from src.lessonly.agents.manager import prompts
from src.lessonly.agents.manager.tools import CREATE_LESSON_BLOCK_TOOL
from src.lessonly.domain.models.defs import LessonBlockType, LessonLevel
from src.lessonly.domain.models.dialog import (
    ChatRequest,
    ChatResponse,
    Context,
    Message,
    Role,
)
from src.lessonly.domain.models.lesson import LessonBlockRequest, LessonInfo
from src.lessonly.shared.logging import get_logger


class ManagerAgent:
    """ """

    MODEL = "gpt-5"

    def __init__(self, llm: OpenAI):
        self.llm = llm
        self.logger = get_logger(__name__)

    def chat(self, request: ChatRequest) -> ChatResponse:
        """
        Chat with the manager agent.
        """
        self.logger.info(f"Received chat request with {len(request.messages)} messages")

        # Convert domain messages to OpenAI format
        openai_messages = [
            {
                "role": Role.SYSTEM.value,
                "content": prompts.SYSTEM_PROMPT,
            },
        ]
        for msg in request.messages:
            message = {"role": msg.role.value, "content": msg.text}
            if msg.context:
                message["content"] += "your lesson is: " + msg.context.block.content
            openai_messages.append(message)

        # Ask the model to produce structured args for the function call; do not force the tool call.
        response = self.llm.chat.completions.create(
            model=self.MODEL,
            messages=openai_messages,
            tools=[CREATE_LESSON_BLOCK_TOOL],
        )

        choice = response.choices[0]

        tool_calls = getattr(choice.message, "tool_calls", None) or []
        if not tool_calls:
            assistant_message = Message(
                role=Role.ASSISTANT, text=choice.message.content.strip()
            )
            self.logger.info("No tool call returned")
            return ChatResponse(messages=request.messages + [assistant_message])

        tool_call = tool_calls[0]
        args_str = (
            tool_call.function.arguments if tool_call.type == "function" else "{}"
        )
        try:
            args = json.loads(args_str)
        except Exception:
            args = {}

        # Map arguments to domain request for the InstructionalistAgent
        try:
            block_type = LessonBlockType(args["type"])  # value-based constructor
            level = LessonLevel(args["info"]["level"])  # value-based constructor
            lesson_info = LessonInfo(
                title=args["info"].get("title") or args["info"]["topic"],
                topic=args["info"]["topic"],
                level=level,
            )
            lesson_block_request = LessonBlockRequest(
                type=block_type,
                info=lesson_info,
                comment=args.get("comment"),
            )
        except Exception as exc:
            self.logger.exception(
                "Failed to map tool arguments to domain request: %s", exc
            )
            assistant_message = Message(role=Role.ASSISTANT, text="I did it!")
            return ChatResponse(messages=request.messages + [assistant_message])

        # Delegate content generation to InstructionalistAgent
        instructionalist = InstructionalistAgent(llm=self.llm)
        block = instructionalist.generate_lesson_block(lesson_block_request)

        # Return minimal text and include the prepared block in the message context
        assistant_message = Message(
            role=Role.ASSISTANT,
            text="Look at what I've done!",
            context=Context(block=block),
        )

        self.logger.info("Generated assistant response with delegated lesson block")
        return ChatResponse(messages=request.messages + [assistant_message])

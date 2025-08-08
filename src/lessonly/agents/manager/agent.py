from openai import OpenAI

from src.lessonly.agents.manager import prompts
from src.lessonly.domain.models.dialog import ChatRequest, ChatResponse, Message, Role
from src.lessonly.shared.logging import get_logger


class ManagerAgent:
    """ """

    MODEL = "gpt-5-mini"

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
            openai_messages.append({"role": msg.role.value, "content": msg.text})

        response = self.llm.chat.completions.create(
            model=self.MODEL,
            messages=openai_messages,
        )

        content = response.choices[0].message.content.strip()

        # Convert back to domain format
        assistant_message = Message(
            role=Role.ASSISTANT,
            text=content,
        )

        self.logger.info("Generated assistant response")
        return ChatResponse(messages=request.messages + [assistant_message])

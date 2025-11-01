"""Dependency provider for the LLM service.

This module defines a factory function that initializes and returns
an instance of OpenAILLMService using application settings.
"""

from knowledge_chat.config.settings import Settings
from knowledge_chat.domain.interfaces.llm_service import LLMService
from knowledge_chat.infrastructure.llm_service.openai_llm_service import \
    OpenAILLMService


def get_llm_service() -> LLMService:
    """Create and return a configured LLM service instance.

    Loads the API credentials and related configuration from environment
    variables via the Settings class.

    Returns:
        LLMService: An initialized instance of the language model service
            powered by the OpenAI API.
    """
    settings = Settings()
    return OpenAILLMService(settings=settings)

"""Dependency provider for the embedding service.

This module defines a factory function that initializes and returns
an instance of OpenAIEmbeddingService using application settings.
"""

from knowledge_chat.config.settings import Settings
from knowledge_chat.infrastructure.embedding_service.openai_embedding_service import \
    OpenAIEmbeddingService


def get_embedding_service() -> OpenAIEmbeddingService:
    """Create and return a configured OpenAIEmbeddingService instance.

    Loads API credentials and configuration from environment variables
    via the Settings class.

    Returns:
        OpenAIEmbeddingService: An initialized embedding service ready
            for use in the application.
    """
    settings = Settings()
    return OpenAIEmbeddingService(settings=settings)

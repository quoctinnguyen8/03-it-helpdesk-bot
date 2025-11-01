"""OpenAI-based embedding service implementation.

This module provides an implementation of the EmbeddingService
interface using the OpenAI API for generating text embeddings.
"""

from typing import List

from openai import OpenAI

from knowledge_chat.config.settings import Settings
from knowledge_chat.domain.interfaces.embedding_service import EmbeddingService


class OpenAIEmbeddingService(EmbeddingService):
    """Embedding generation service using the OpenAI API."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the OpenAI client.

        Args:
            settings (Settings): The application settings containing
                API key and model configuration.
        """
        self.client = OpenAI(
            base_url=settings.openai_embedding_base_url,
            api_key=settings.openai_embedding_key
        )
        self.model = settings.openai_embedding_model

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of input texts.

        Args:
            texts (List[str]): A list of text strings to embed.

        Returns:
            List[List[float]]: A list of vector embeddings, where each
                embedding is represented as a list of floats.
        """
        response = self.client.embeddings.create(
            model=self.model,
            input=texts,
        )
        return [item.embedding for item in response.data]

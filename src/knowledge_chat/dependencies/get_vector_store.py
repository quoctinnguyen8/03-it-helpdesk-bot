"""Dependency provider for the vector store service.

This module defines a factory function that initializes and returns
an instance of ChromaVectorStore using application settings.
"""

from knowledge_chat.config.settings import Settings
from knowledge_chat.domain.interfaces.vector_store import VectorStore
from knowledge_chat.infrastructure.vector_store.chroma_vector_store import \
    ChromaVectorStore


def get_vector_store() -> VectorStore:
    """Create and return a configured vector store instance.

    Loads the persistent storage path from environment variables using
    the Settings class.

    Returns:
        VectorStore: An initialized vector store backed by ChromaDB.
    """
    settings = Settings()
    return ChromaVectorStore(settings=settings)

"""Dependency provider for the document chunker.

This module defines a factory function that initializes and returns
an instance of RecursiveCharacterChunker using application settings.
"""

from knowledge_chat.config.settings import Settings
from knowledge_chat.domain.interfaces.document_chunker import DocumentChunker
from knowledge_chat.infrastructure.chunking.recursive_character_chunker import \
    RecursiveCharacterChunker


def get_chunker() -> DocumentChunker:
    """Create and return a configured RecursiveCharacterChunker instance.

    Loads chunking configuration from environment variables via the
    Settings class to avoid hard-coded values.

    Returns:
        DocumentChunker: A configured chunker ready for use in the
            ingestion pipeline.
    """
    settings = Settings()

    return RecursiveCharacterChunker(
        chunk_size=settings.chunker_chunk_size,
        chunk_overlap=settings.chunker_chunk_overlap,
        separators=list(settings.chunker_separators),
    )

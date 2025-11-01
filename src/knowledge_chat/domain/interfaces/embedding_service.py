"""Abstract embedding service interface.

This module defines an abstract base class for embedding services
that generate vector representations for input texts.
"""

from abc import ABC, abstractmethod
from typing import List


class EmbeddingService(ABC):
    """Abstract interface for text embedding services."""

    @abstractmethod
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for a list of input texts.

        Args:
            texts (List[str]): A list of text strings to embed.

        Returns:
            List[List[float]]: A list of vector embeddings, where each
                embedding is represented as a list of floats.
        """

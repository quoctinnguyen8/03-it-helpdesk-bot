"""Abstract interface for document chunking.

This module defines an abstract base class for services that handle
text chunking operations, preparing documents for embedding or retrieval.
"""

from abc import ABC, abstractmethod
from typing import List


class DocumentChunker(ABC):
    """Abstract interface for document chunking services."""

    @abstractmethod
    def chunk_text(self, text: str) -> List[str]:
        """Split input text into smaller chunks.

        Args:
            text (str): The input document text to be split.

        Returns:
            List[str]: A list of text chunks.
        """

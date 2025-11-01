"""Recursive character-based document chunking implementation.

This module provides an implementation of the DocumentChunker interface
using LangChain's RecursiveCharacterTextSplitter. It ensures that large
texts are divided into manageable chunks with semantic continuity.
"""

from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter

from knowledge_chat.domain.interfaces.document_chunker import DocumentChunker


class RecursiveCharacterChunker(DocumentChunker):
    """Document chunking service using RecursiveCharacterTextSplitter."""

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separators: List[str] | None = None,
    ) -> None:
        """Initialize the chunker with configuration parameters.

        Args:
            chunk_size (int): Maximum number of characters per chunk.
            chunk_overlap (int): Number of overlapping characters
                between consecutive chunks.
            separators (List[str] | None): Optional list of custom
                separators to guide text splitting.
        """
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=separators or ["\n\n", "\n", ".", " ", ""],
        )

    def chunk_text(self, text: str) -> List[str]:
        """Split input text into smaller overlapping chunks.

        Args:
            text (str): The input document text to be split.

        Returns:
            List[str]: A list of text chunks.
        """
        return self._splitter.split_text(text)

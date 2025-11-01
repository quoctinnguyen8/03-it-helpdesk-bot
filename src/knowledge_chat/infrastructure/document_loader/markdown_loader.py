"""Markdown document loader implementation.

This module provides an implementation of the DocumentLoader interface
for reading Markdown (.md) files using Python's built-in markdown library.
"""

from typing import List

from langchain_core.documents import Document

from knowledge_chat.domain.interfaces.document_loader import DocumentLoader


class MarkdownLoader(DocumentLoader):
    """Document loader for Markdown files."""

    def load(self, file_path: str) -> List[Document]:
        """Load a Markdown file and return its content as LangChain Documents.

        Args:
            file_path (str): Path to the Markdown file.

        Returns:
            List[Document]: A list containing LangChain Document objects
                with text content and metadata.
        """
        # Read markdown file as plain text
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Create document with metadata
        document = Document(
            page_content=content,
            metadata={
                "source": file_path.split("\\")[-1].split("/")[-1],
                "file_type": "markdown",
            },
        )

        return [document]

"""Multi-format document loader implementation.

This module provides a unified document loader that automatically detects
file types and uses the appropriate loader (Text, PDF, Markdown, JSON).
"""

from pathlib import Path
from typing import List

from langchain_core.documents import Document

from knowledge_chat.domain.interfaces.document_loader import DocumentLoader
from knowledge_chat.infrastructure.document_loader.json_loader import JSONLoader
from knowledge_chat.infrastructure.document_loader.markdown_loader import \
    MarkdownLoader
from knowledge_chat.infrastructure.document_loader.pdf_loader import PDFLoader
from knowledge_chat.infrastructure.document_loader.text_file_loader import \
    TextFileLoader


class MultiFormatLoader(DocumentLoader):
    """Document loader that supports multiple file formats.

    Automatically detects file type by extension and uses the appropriate loader:
    - .txt: TextFileLoader
    - .pdf: PDFLoader
    - .md, .markdown: MarkdownLoader
    - .json: JSONLoader
    """

    def __init__(self) -> None:
        """Initialize loaders for all supported formats."""
        self._text_loader = TextFileLoader()
        self._pdf_loader = PDFLoader()
        self._markdown_loader = MarkdownLoader()
        self._json_loader = JSONLoader()

    def load(self, file_path: str) -> List[Document]:
        """Load a document using the appropriate loader based on file extension.

        Args:
            file_path (str): Path to the document file.

        Returns:
            List[Document]: A list of LangChain Document objects
                containing the loaded content and metadata.

        Raises:
            ValueError: If the file format is not supported.
        """
        file_extension = Path(file_path).suffix.lower()

        if file_extension == ".txt":
            return self._text_loader.load(file_path)
        elif file_extension == ".pdf":
            return self._pdf_loader.load(file_path)
        elif file_extension in [".md", ".markdown"]:
            return self._markdown_loader.load(file_path)
        elif file_extension == ".json":
            return self._json_loader.load(file_path)
        else:
            raise ValueError(
                f"Unsupported file format: {file_extension}. "
                f"Supported formats: .txt, .pdf, .md, .markdown, .json"
            )

    @staticmethod
    def get_supported_extensions() -> List[str]:
        """Get list of supported file extensions.

        Returns:
            List[str]: List of supported file extensions with dots.
        """
        return [".txt", ".pdf", ".md", ".markdown", ".json"]

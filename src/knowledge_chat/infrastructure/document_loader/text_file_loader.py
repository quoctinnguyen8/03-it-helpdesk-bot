"""Text file document loader implementation.

This module provides an implementation of the DocumentLoader interface
using LangChain's TextLoader to read plain text files.
"""

from typing import List

from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

from knowledge_chat.domain.interfaces.document_loader import DocumentLoader


class TextFileLoader(DocumentLoader):
    """Document loader for plain text files."""

    def load(self, file_path: str) -> List[Document]:
        """Load a text file and return its content as LangChain Documents.

        Args:
            file_path (str): Path to the text file.

        Returns:
            List[Document]: A list containing one or more LangChain
                Document objects, each with text content and metadata.
        """
        loader = TextLoader(file_path, encoding="utf-8")
        documents = loader.load()

        # Ensure each document has at least the filename in metadata
        for doc in documents:
            doc.metadata["source"] = file_path.split("\\")[-1].split("/")[-1]
            doc.metadata["file_type"] = "text"

        return documents

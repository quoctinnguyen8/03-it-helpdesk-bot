"""PDF document loader implementation.

This module provides an implementation of the DocumentLoader interface
for reading PDF files using LangChain's PyPDFLoader.
"""

from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from knowledge_chat.domain.interfaces.document_loader import DocumentLoader


class PDFLoader(DocumentLoader):
    """Document loader for PDF files."""

    def load(self, file_path: str) -> List[Document]:
        """Load a PDF file and return its content as LangChain Documents.

        Args:
            file_path (str): Path to the PDF file.

        Returns:
            List[Document]: A list of LangChain Document objects,
                one per page, each with text content and metadata.
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # Add filename to metadata for each page
        for doc in documents:
            doc.metadata["source"] = file_path.split("\\")[-1].split("/")[-1]
            doc.metadata["file_type"] = "pdf"

        return documents

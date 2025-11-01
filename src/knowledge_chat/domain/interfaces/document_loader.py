"""Abstract interface for document loading.

This module defines an abstract base class for services that handle
loading documents from various file formats into text representations.
"""

from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document


class DocumentLoader(ABC):
    """Abstract interface for document loading services."""

    @abstractmethod
    def load(self, file_path: str) -> List[Document]:
        """Load a document from a given file path.

        Args:
            file_path (str): Path to the document file.

        Returns:
            List[Document]: A list of LangChain Document objects
                containing the loaded content and metadata.
        """

"""Vector store interface module.

This module defines the abstract VectorStore interface, which outlines
the required methods for adding and querying document embeddings in
a vector database.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class VectorStore(ABC):
    """Abstract interface for vector database operations."""

    @abstractmethod
    def add_documents(
        self,
        ids: List[str],
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: List[Dict[str, Any]],
    ) -> None:
        """Add documents, their embeddings, and metadata to the ChromaDB collection.

        Args:
            ids (List[str]): Unique identifiers for each document.
            embeddings (List[List[float]]): Vector embeddings of documents.
            documents (List[str]): Original document texts to be stored.
            metadatas (List[Dict[str, Any]]): Metadata dictionaries
                describing each document.
        """

    @abstractmethod
    def query_similar(
        self,
        embedding: List[float],
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """Query the vector store for the most similar documents.

        Args:
            embedding (List[float]): A single embedding vector to
                compare against the stored documents.
            top_k (int, optional): Number of top results to return.
                Defaults to 5.

        Returns:
            Dict[str, Any]: A dictionary containing matched document
                IDs, distances, and metadata.
        """

    @abstractmethod
    def delete_all(self) -> None:
        """Delete all stored movie embeddings from the vector store.

        This method clears the ChromaDB collection completely.
        It's useful when reimporting a new dataset or resetting the app state.
        """

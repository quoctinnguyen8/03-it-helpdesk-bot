"""ChromaDB-based vector store implementation.

This module provides an implementation of the VectorStore interface
using ChromaDB for storing and querying vector embeddings and documents.
"""

from typing import Any, Dict, List

import chromadb

from knowledge_chat.config.settings import Settings
from knowledge_chat.domain.interfaces.vector_store import VectorStore


class ChromaVectorStore(VectorStore):
    """Vector store implementation using ChromaDB."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the ChromaDB persistent client.

        Args:
            settings (Settings): Application configuration instance
                containing database path and collection name.
        """
        self._collection_name = settings.chromadb_collection_name
        self._client = chromadb.PersistentClient(path=settings.chroma_db_path)
        self._collection = self._client.get_or_create_collection(
            self._collection_name,
            configuration={"hnsw": {"space": "cosine"}},
        )

    # ------------------------------------------------------------------
    # Core Methods
    # ------------------------------------------------------------------

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
        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

    def query_similar(
        self,
        embedding: List[float],
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """Query the most similar documents for a given embedding.

        Args:
            embedding (List[float]): The query embedding vector.
            top_k (int, optional): The number of top results to return.
                Defaults to 5.

        Returns:
            Dict[str, Any]: Query results containing matched document IDs,
                distances, metadata, and original document texts.
        """
        return self._collection.query(
            query_embeddings=[embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

    def delete_all(self) -> None:
        """Delete all stored embeddings and documents from the vector store.

        This method clears the entire ChromaDB collection.
        It's useful when reimporting a new dataset or resetting the app state.
        """
        self._client.delete_collection(self._collection_name)
        self._collection = self._client.get_or_create_collection(self._collection_name)

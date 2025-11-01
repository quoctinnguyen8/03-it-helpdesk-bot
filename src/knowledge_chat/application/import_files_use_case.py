"""Use case for importing text documents into the vector store.

This module defines the ImportFilesUseCase class, which loads
text files, splits them into chunks, generates embeddings, and stores
the results in a vector database along with metadata and original text.
"""

import uuid
from typing import Any, List

from knowledge_chat.domain.interfaces.document_chunker import DocumentChunker
from knowledge_chat.domain.interfaces.document_loader import DocumentLoader
from knowledge_chat.domain.interfaces.embedding_service import EmbeddingService
from knowledge_chat.domain.interfaces.vector_store import VectorStore


class ImportFilesUseCase:
    """Application use case for importing text files into the vector store."""

    def __init__(
        self,
        document_loader: DocumentLoader,
        chunker: DocumentChunker,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ) -> None:
        """Initialize the use case with its dependencies.

        Args:
            document_loader (DocumentLoader): Loader for reading text files.
            chunker (DocumentChunker): Service for splitting text into chunks.
            embedding_service (EmbeddingService): Embedding generation service.
            vector_store (VectorStore): Persistent vector database service.
        """
        self._document_loader = document_loader
        self._chunker = chunker
        self._embedding_service = embedding_service
        self._vector_store = vector_store

    # -----------------------------------------------------
    # Public entry point
    # -----------------------------------------------------

    def invoke(self, file_paths: List[str]) -> None:
        """Import one or more text files into the vector store.

        Args:
            file_paths (List[str]): List of paths to text files.

        Raises:
            ValueError: If no valid files are provided.
        """
        if not file_paths:
            raise ValueError("At least one file path must be provided.")

        # Delete all documents from previous import
        self._vector_store.delete_all()

        all_chunks: List[str] = []
        all_metadatas: List[dict[str, Any]] = []
        all_documents: List[str] = []

        for path in file_paths:
            documents = self._document_loader.load(path)
            for doc in documents:
                chunks = self._chunker.chunk_text(doc.page_content)

                for i, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    all_metadatas.append(
                        {
                            "source": doc.metadata.get("source", path),
                            "chunk_index": i,
                        }
                    )
                    all_documents.append(doc.page_content)

        # Generate embeddings for each chunk
        embeddings = self._embedding_service.embed_texts(all_chunks)

        # Persist to vector store
        self._persist_to_vector_store(
            documents=all_documents,
            texts=all_chunks,
            embeddings=embeddings,
            metadatas=all_metadatas,
        )

    # -----------------------------------------------------
    # Private helper methods
    # -----------------------------------------------------

    def _persist_to_vector_store(
        self,
        documents: List[str],
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[dict[str, Any]],
    ) -> None:
        """Persist the chunks, embeddings, metadata, and documents into the vector store."""
        ids = [str(uuid.uuid4()) for _ in range(len(texts))]

        self._vector_store.add_documents(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

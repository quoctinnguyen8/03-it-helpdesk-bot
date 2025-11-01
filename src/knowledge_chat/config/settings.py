"""Application configuration module.

This module defines the Settings class that manages configuration
values loaded from environment variables or an optional .env file.
"""

from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables.

    Attributes:
        openai_base_url (str): Base URL for OpenAI API requests.
        openai_api_key (str): API key for OpenAI chat/completion services.
        openai_model (str): Default model name for OpenAI chat/completion.

        openai_embedding_base_url (str): Base URL for OpenAI embedding API.
        openai_embedding_key (str): API key for OpenAI embedding service.
        openai_embedding_model (str): Embedding model name.

        chroma_db_path (str): Path to the local Chroma database directory.
        chromadb_collection_name (str): Collection name for Chroma vector DB.

        hf_token (str): Hugging Face API token.
        hf_tts_model (str): Model name for Hugging Face text-to-speech.

        chunker_chunk_size (int): Maximum number of characters per chunk.
        chunker_chunk_overlap (int): Overlapping characters between chunks.
        chunker_separators (List[str]): List of separators for chunking.
    """

    # ----------------- OpenAI Configuration -----------------
    openai_base_url: str
    openai_api_key: str
    openai_model: str

    openai_embedding_base_url: str
    openai_embedding_key: str
    openai_embedding_model: str = "text-embedding-3-small"

    # ----------------- Vector Database Configuration -----------------
    chroma_db_path: str = "./data/chroma_db"
    chromadb_collection_name: str = "it_helpdesk_documents"

    # ----------------- Chunker Configuration -----------------
    chunker_chunk_size: int = 1000
    chunker_chunk_overlap: int = 200
    chunker_separators: List[str] = ["\n\n", "\n", ".", " ", ""]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

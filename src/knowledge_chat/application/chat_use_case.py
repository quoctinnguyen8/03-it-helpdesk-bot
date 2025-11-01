"""Use case for AI conversational chat with retrieval-augmented generation (RAG).

This module defines the `ChatUseCase` class, which orchestrates a full
Retrieval-Augmented Generation (RAG) workflow:

1. Receives a conversational message history from the user.
2. Embeds the most recent user query into a dense vector using the
   configured embedding service.
3. Retrieves semantically similar documents from the vector database.
4. Filters those documents using a cosine similarity threshold.
5. Builds a contextual prompt combining the retrieved content and
   the chat history.
6. Generates a response via a Large Language Model (LLM).
7. Appends a numbered list of referenced source documents to the output.

This approach enables context-aware, grounded, and explainable AI responses.
"""

import json
from typing import Any, List

from knowledge_chat.config.prompts import (CHAT_PROMPT_TEMPLATE,
                                           RERANK_FILTER_PROMPT_TEMPLATE)
from knowledge_chat.domain.entities.message import Message, MessageType
from knowledge_chat.domain.interfaces.embedding_service import EmbeddingService
from knowledge_chat.domain.interfaces.llm_service import LLMService
from knowledge_chat.domain.interfaces.vector_store import VectorStore


class ChatUseCase:
    """Use case for conversational chat powered by Retrieval-Augmented Generation (RAG).

    This class acts as the orchestration layer between:
        - The **Embedding Service**, which transforms queries into dense vectors.
        - The **Vector Store**, which retrieves similar document embeddings.
        - The **LLM Service**, which generates the final AI response.

    It ensures that only contextually relevant documents (based on cosine
    similarity) are used to ground the model's response, and appends a
    reference list for transparency.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
        llm_service: LLMService,
    ) -> None:
        """Initialize the chat use case and its dependencies.

        Args:
            embedding_service (EmbeddingService):
                Component responsible for encoding text queries into vector embeddings.
            vector_store (VectorStore):
                Component responsible for similarity-based retrieval of embedded documents.
            llm_service (LLMService):
                Component responsible for generating language-model responses.
        """
        self._embedding_service = embedding_service
        self._vector_store = vector_store
        self._llm_service = llm_service

    # ----------------------------------------------------------------------
    # Public entry point
    # ----------------------------------------------------------------------

    def invoke(self, messages: List[Message], top_k: int = 3) -> Message:
        """Generate an AI response to a user's message using RAG.

        The pipeline:
            1. Extracts the user's latest query.
            2. Computes its embedding.
            3. Retrieves and filters similar documents from the vector store.
            4. Builds a context-enriched prompt.
            5. Calls the LLM for generation.
            6. Returns a `Message` entity containing the AI's answer.

        Args:
            messages (List[Message]):
                The full conversation history, where the last message must
                be from the user.
            top_k (int, optional):
                Maximum number of top retrieved documents to consider.
                Defaults to 3.

        Returns:
            Message: An AI message containing the generated text and optional
            reference list.

        Raises:
            ValueError: If message history is empty or the last message is not from the user.
        """
        if not messages:
            raise ValueError("Message history cannot be empty.")

        last_message = messages[-1]
        if last_message.type != MessageType.USER:
            raise ValueError("The last message must be from the user.")

        query_text = last_message.content
        query_embedding = self._embedding_service.embed_texts([query_text])[0]

        # Retrieve candidate documents
        retrieved_docs = self._vector_store.query_similar(
            embedding=query_embedding,
            top_k=top_k,
        )

        # Filter only relevant ones
        filtered_docs = self._filter_relevant_docs(retrieved_docs, query_text)
        if not filtered_docs["documents"] or not filtered_docs["documents"][0]:
            ai_text = (
                "Xin lỗi, tôi không thể tìm thấy thông tin liên quan. (I'm sorry, I could not find relevant information in the knowledge base.)"
            )
            return Message(type=MessageType.AI, content=ai_text)

        # Build contextual prompt
        context_text = self._build_context_text(filtered_docs)
        references = self._extract_references(filtered_docs)
        prompt = self._build_prompt(context_text, messages)

        # Generate AI response
        ai_response = self._llm_service.generate(prompt)

        # Append reference section if any
        if references:
            reference_lines = "\n".join(
                f"[{i + 1}] {ref}" for i, ref in enumerate(references)
            )
            ai_response += f"\n\nReferences:\n{reference_lines}"

        return Message(type=MessageType.AI, content=ai_response)

    # ----------------------------------------------------------------------
    # Private helper methods
    # ----------------------------------------------------------------------

    def _filter_relevant_docs(self, retrieved_docs: dict[str, Any], query_text: str) -> dict[str, Any]:
        """Filter and re-rank retrieved documents using an LLM for semantic relevance.

        Instead of relying purely on vector similarity distances, this step delegates
        semantic filtering to the LLM. It asks the model to identify which of the
        retrieved chunks are *truly relevant* to the user's intent, based on meaning
        rather than numeric proximity.

        Steps:
            1. Format all retrieved documents as an indexed list.
            2. Ask the LLM to return a JSON array of indices that are relevant.
            3. Parse and keep only those documents.

        Args:
            retrieved_docs (dict[str, Any]):
                The raw retrieval results from the vector store, containing:
                    - documents: [[str, ...]]
                    - metadatas: [[dict, ...]]
                    - distances: [[float, ...]] (not used for filtering here)
            query_text (str):
                The user's question or query text.

        Returns:
            dict[str, Any]: A dictionary of filtered results:
                {
                    "documents": [[...]],
                    "metadatas": [[...]]
                }
        """
        docs = retrieved_docs.get("documents", [[]])
        metas = retrieved_docs.get("metadatas", [[]])

        if not docs or not docs[0]:
            return {"documents": [[]], "metadatas": [[]]}

        # --- Step 1: Prepare prompt for LLM filtering ---
        formatted_docs = "\n\n".join(f"[{i}] {chunk}" for i, chunk in enumerate(docs[0]))
        ranking_prompt = RERANK_FILTER_PROMPT_TEMPLATE.format(
            query=query_text,
            documents=formatted_docs,
        )

        # --- Step 2: LLM-based semantic selection ---
        llm_output = self._llm_service.generate(ranking_prompt)

        try:
            relevant_indices = json.loads(llm_output)
            if not isinstance(relevant_indices, list):
                relevant_indices = []
        #pylint: disable=broad-exception-caught
        except Exception:
            relevant_indices = []

        # --- Step 3: Filter only the relevant chunks ---
        filtered_docs = [docs[0][i] for i in relevant_indices if i < len(docs[0])]
        filtered_metas = [metas[0][i] for i in relevant_indices if i < len(metas[0])]

        return {"documents": [filtered_docs], "metadatas": [filtered_metas]}

    def _build_context_text(self, retrieved_docs: dict[str, Any]) -> str:
        """Build a context section for the LLM prompt.

        Args:
            retrieved_docs (dict[str, Any]): Filtered results with documents and metadata.

        Returns:
            str: A formatted multi-line string combining document text and source names.
        """
        documents = retrieved_docs.get("documents", [[]])
        metadatas = retrieved_docs.get("metadatas", [[]])

        if not documents or not documents[0]:
            return "No relevant context found."

        context_lines: List[str] = []
        for i, doc in enumerate(documents[0]):
            file_name = metadatas[0][i].get("source", "Unknown file")
            context_lines.append(f"[{file_name}] {doc}")

        return "\n".join(context_lines)

    def _extract_references(self, retrieved_docs: dict[str, Any]) -> List[str]:
        """Extract a unique list of source filenames from metadata.

        Args:
            retrieved_docs (dict[str, Any]): Query results containing metadatas.

        Returns:
            List[str]: Unique list of referenced filenames used for context.
        """
        metadatas = retrieved_docs.get("metadatas", [[]])
        if not metadatas or not metadatas[0]:
            return []

        sources = []
        for meta in metadatas[0]:
            source = meta.get("source")
            if source and source not in sources:
                sources.append(source)
        return sources

    def _build_prompt(self, context: str, messages: List[Message]) -> str:
        """Construct the final prompt to be passed to the LLM.

        Args:
            context (str): Concatenated, filtered contextual text from retrieved documents.
            messages (List[Message]): Full conversation history, including user and AI turns.

        Returns:
            str: A fully formatted prompt string ready for LLM generation.
        """
        conversation_text = "\n".join(
            f"{msg.type.value.title()}: {msg.content}" for msg in messages
        )

        return CHAT_PROMPT_TEMPLATE.format(
            context=context,
            conversation=conversation_text,
        )

"""Main entry point for the Knowledge Chatbot system.

This module initializes dependencies, constructs the use cases,
and launches the Gradio-based user interface.
"""

from knowledge_chat.application.chat_use_case import ChatUseCase
from knowledge_chat.application.import_files_use_case import ImportFilesUseCase
from knowledge_chat.dependencies.get_chunker import get_chunker
from knowledge_chat.dependencies.get_document_loader import get_document_loader
from knowledge_chat.dependencies.get_embedding_service import \
    get_embedding_service
from knowledge_chat.dependencies.get_llm_service import get_llm_service
from knowledge_chat.dependencies.get_vector_store import get_vector_store
from knowledge_chat.presentation.ui_gradio import KnowledgeChatUI


def main() -> None:
    """Initialize dependencies and start the Gradio interface."""
    # -----------------------------------------------------
    # Dependency Injection
    # -----------------------------------------------------
    document_loader = get_document_loader()
    chunker = get_chunker()
    embedding_service = get_embedding_service()
    vector_store = get_vector_store()
    llm_service = get_llm_service()

    # -----------------------------------------------------
    # Application Use Cases
    # -----------------------------------------------------
    import_use_case = ImportFilesUseCase(
        document_loader=document_loader,
        chunker=chunker,
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    chat_use_case = ChatUseCase(
        embedding_service=embedding_service,
        vector_store=vector_store,
        llm_service=llm_service,
    )

    # -----------------------------------------------------
    # Presentation Layer (UI)
    # -----------------------------------------------------
    ui = KnowledgeChatUI(import_use_case=import_use_case, chat_use_case=chat_use_case)
    app = ui.create_interface()

    # -----------------------------------------------------
    # Launch Gradio App
    # -----------------------------------------------------
    app.launch(server_name="0.0.0.0", server_port=3000)


if __name__ == "__main__":
    main()

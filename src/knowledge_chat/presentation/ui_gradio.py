"""Gradio-based user interface for the IT Helpdesk Bot with RAG.

This UI allows users to:
1. Upload multiple text documents to build a knowledge base.
2. Chat directly with the AI assistant with streaming responses,
   which retrieves context from the vector store and provides
   referenced, context-aware answers in multiple languages.

Enhanced features:
- Streaming responses (typewriter effect)
- Progress bar for document import
- Multi-language support (English/Vietnamese)
"""

import time
from typing import Generator, List

import gradio as gr

from knowledge_chat.application.chat_use_case import ChatUseCase
from knowledge_chat.application.import_files_use_case import ImportFilesUseCase
from knowledge_chat.domain.entities.message import Message, MessageType


class KnowledgeChatUI:
    """Gradio-based UI for IT Helpdesk Bot with document ingestion and AI chat."""

    def __init__(
        self,
        import_use_case: ImportFilesUseCase,
        chat_use_case: ChatUseCase,
    ) -> None:
        """Initialize the UI with application use cases."""
        self._import_use_case = import_use_case
        self._chat_use_case = chat_use_case
        self._messages: List[Message] = []
        self._uploaded_files: List[str] = []

    # -----------------------------------------------------
    # UI Construction
    # -----------------------------------------------------

    def create_interface(self) -> gr.Blocks:
        """Create and return the Gradio UI layout with enhanced features."""
        theme = gr.themes.Soft(
            primary_hue="blue",
            secondary_hue="sky",
            neutral_hue="gray",
            font=[gr.themes.GoogleFont("Roboto")],
        )

        with gr.Blocks(
            theme=theme,
            title="IT Helpdesk Bot (RAG)",
            css="""
                #title {
                    text-align: center;
                    font-size: 2em;
                    color: #2563eb;
                    margin-bottom: 10px;
                }
                #subtitle {
                    text-align: center;
                    font-size: 1.1em;
                    color: #555;
                    margin-bottom: 30px;
                }
                .gr-button {
                    border-radius: 10px !important;
                    font-weight: 600;
                }
                .gradio-container {
                    background-color: #fafafa !important;
                }
                .chatbox {
                    min-height: 500px;
                    max-height: 600px;
                    overflow-y: auto;
                }
            """,
            js="""
                function focusInput() {
                    const textbox = document.querySelector('textarea[placeholder*="Type your message"]');
                    if (textbox) {
                        setTimeout(() => textbox.focus(), 100);
                    }
                }
            """,
        ) as demo:
            gr.Markdown("<h1 id='title'>IT Helpdesk Bot</h1>")
            gr.Markdown(
                "<p id='subtitle'>Upload IT troubleshooting documents and chat with AI — powered by RAG</p>"
            )

            with gr.Tabs():
                # =============================================================
                # TAB 1: DOCUMENT UPLOAD WITH PROGRESS BAR
                # =============================================================
                with gr.TabItem("📁 Import Documents"):
                    gr.Markdown("### Step 1: Upload documents to build the knowledge base.")
                    gr.Markdown("_Supported formats: TXT, PDF, Markdown (.md), JSON_")
                    gr.Markdown("_Supported languages: English, Vietnamese_")

                    file_input = gr.File(
                        file_types=[".txt", ".pdf", ".md", ".markdown", ".json"],
                        file_count="multiple",
                        label="Upload files (TXT, PDF, MD, JSON)",
                    )
                    import_status = gr.Markdown("ℹ️ _Waiting for files..._")
                    import_progress = gr.Progress()
                    file_table = gr.DataFrame(
                        headers=["File Name"],
                        label="Imported Documents",
                        interactive=False,
                    )

                    def import_files(files, progress=gr.Progress()):
                        """Handle file upload and document import with progress bar."""
                        if not files:
                            return "⚠️ Please upload at least one file.", None
                        
                        try:
                            paths = [f.name for f in files]
                            self._uploaded_files = [f.name.split("/")[-1].split("\\")[-1] for f in files]
                            
                            # Show progress for import process
                            progress(0, desc="Starting import...")
                            time.sleep(0.5)
                            
                            progress(0.2, desc="Loading documents...")
                            time.sleep(0.3)
                            
                            progress(0.4, desc="Chunking text...")
                            time.sleep(0.3)
                            
                            progress(0.6, desc="Generating embeddings...")
                            self._import_use_case.invoke(paths)
                            
                            progress(0.9, desc="Storing in database...")
                            time.sleep(0.3)
                            
                            progress(1.0, desc="Import completed!")
                            
                            table_data = [[name] for name in self._uploaded_files]
                            return (
                                f"✅ Successfully imported {len(paths)} file(s) into the vector store. | "
                                f"Đã nhập thành công {len(paths)} file vào cơ sở kiến thức.",
                                table_data,
                            )
                        # pylint: disable=broad-exception-caught
                        except Exception as e:
                            return f"❌ Error while importing files: {str(e)}", None

                    file_input.change(  # pylint: disable=no-member
                        fn=import_files,
                        inputs=file_input,
                        outputs=[import_status, file_table],
                    )

                # =============================================================
                # TAB 2: CHAT INTERFACE WITH STREAMING
                # =============================================================
                with gr.TabItem("💬 Chat with AI"):
                    gr.Markdown("### Step 2: Start chatting with your IT Helpdesk AI assistant!")
                    gr.Markdown("_Ask questions in English or Vietnamese")

                    chat_box = gr.Chatbot(
                        label="Chat Window",
                        elem_classes=["chatbox"],
                        height=350,
                    )

                    with gr.Row():
                        user_input = gr.Textbox(
                            placeholder="Type your message here... (Press Enter to send)",
                            label="Your Message",
                            lines=1,
                            autofocus=True,
                        )
                    send_button = gr.Button("🚀 Send", variant="primary")
                    clear_button = gr.Button("🧹 Clear Chat", variant="secondary")

                    # ------------------ Chat Logic with Streaming ------------------
                    def chat_stream(user_message: str, history: List[List[str]]) -> Generator:
                        """Handle user input and generate AI response with streaming effect."""
                        if not user_message.strip():
                            yield history
                            return

                        self._messages.append(
                            Message(type=MessageType.USER, content=user_message)
                        )

                        try:
                            # Get AI response
                            ai_message = self._chat_use_case.invoke(self._messages)
                            self._messages.append(ai_message)
                            
                            # Add user message to history
                            history.append(["🧑‍💬 " + user_message, ""])
                            
                            # Stream AI response character by character (typewriter effect)
                            response_text = "🤖 " + ai_message.content
                            displayed_text = ""
                            
                            for char in response_text:
                                displayed_text += char
                                history[-1][1] = displayed_text
                                time.sleep(0.01)  # Adjust speed here
                                yield history
                                
                        # pylint: disable=broad-exception-caught
                        except Exception as e:
                            history.append(
                                ["🧑‍💬 " + user_message, f"❌ Error while processing: {str(e)}"]
                            )
                            yield history

                    def clear_chat():
                        """Reset the entire chat session."""
                        self._messages.clear()
                        return []

                    # Bind events - Use submit_btn to control Enter behavior
                    chat_interface = user_input.submit(  # pylint: disable=no-member
                        fn=chat_stream,
                        inputs=[user_input, chat_box],
                        outputs=chat_box,
                    ).then(
                        fn=lambda: "",  # Clear input after sending
                        inputs=None,
                        outputs=user_input,
                    ).then(
                        fn=None,
                        inputs=None,
                        outputs=None,
                        js="focusInput",  # Refocus on input box
                    )

                    send_button.click(  # pylint: disable=no-member
                        fn=chat_stream,
                        inputs=[user_input, chat_box],
                        outputs=chat_box,
                    ).then(
                        fn=lambda: "",  # Clear input after sending
                        inputs=None,
                        outputs=user_input,
                    ).then(
                        fn=None,
                        inputs=None,
                        outputs=None,
                        js="focusInput",  # Refocus on input box
                    )

                    clear_button.click(  # pylint: disable=no-member
                        fn=clear_chat,
                        inputs=None,
                        outputs=chat_box,
                    )

        return demo

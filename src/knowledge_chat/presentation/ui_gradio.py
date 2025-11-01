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
        ) as demo:
            gr.Markdown("<h1 id='title'>IT Helpdesk Bot</h1>")
            gr.Markdown(
                "<p id='subtitle'>Upload IT troubleshooting documents and chat with AI — powered by RAG | "
                "Hỗ trợ tiếng Việt & English</p>"
            )

            with gr.Tabs():
                # =============================================================
                # TAB 1: DOCUMENT UPLOAD WITH PROGRESS BAR
                # =============================================================
                with gr.TabItem("📁 Import Documents"):
                    gr.Markdown("### Step 1: Upload documents to build the knowledge base.")
                    gr.Markdown("_Supported formats: TXT, PDF, Markdown (.md), JSON | Định dạng hỗ trợ: TXT, PDF, Markdown (.md), JSON_")
                    gr.Markdown("_Supported languages: English, Vietnamese | Hỗ trợ: Tiếng Anh, Tiếng Việt_")
                    
                    file_input = gr.File(
                        file_types=[".txt", ".pdf", ".md", ".markdown", ".json"],
                        file_count="multiple",
                        label="Upload files (TXT, PDF, MD, JSON) | Tải lên file (TXT, PDF, MD, JSON)",
                    )
                    import_status = gr.Markdown("ℹ️ _Waiting for files... | Đang chờ file..._")
                    import_progress = gr.Progress()
                    file_table = gr.DataFrame(
                        headers=["File Name"],
                        label="Imported Documents | Tài liệu đã nhập",
                        interactive=False,
                    )

                    def import_files(files, progress=gr.Progress()):
                        """Handle file upload and document import with progress bar."""
                        if not files:
                            return "⚠️ Please upload at least one file. | Vui lòng tải lên ít nhất một file.", None
                        
                        try:
                            paths = [f.name for f in files]
                            self._uploaded_files = [f.name.split("/")[-1].split("\\")[-1] for f in files]
                            
                            # Show progress for import process
                            progress(0, desc="Starting import... | Bắt đầu nhập...")
                            time.sleep(0.5)
                            
                            progress(0.2, desc="Loading documents... | Đang tải tài liệu...")
                            time.sleep(0.3)
                            
                            progress(0.4, desc="Chunking text... | Đang chia nhỏ văn bản...")
                            time.sleep(0.3)
                            
                            progress(0.6, desc="Generating embeddings... | Đang tạo embeddings...")
                            self._import_use_case.invoke(paths)
                            
                            progress(0.9, desc="Storing in database... | Đang lưu vào database...")
                            time.sleep(0.3)
                            
                            progress(1.0, desc="Import completed! | Hoàn thành!")
                            
                            table_data = [[name] for name in self._uploaded_files]
                            return (
                                f"✅ Successfully imported {len(paths)} file(s) into the vector store. | "
                                f"Đã nhập thành công {len(paths)} file vào cơ sở kiến thức.",
                                table_data,
                            )
                        # pylint: disable=broad-exception-caught
                        except Exception as e:
                            return f"❌ Error while importing files: {str(e)} | Lỗi khi nhập file: {str(e)}", None

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
                    gr.Markdown("_Ask questions in English or Vietnamese | Hỏi bằng tiếng Anh hoặc tiếng Việt_")

                    chat_box = gr.Chatbot(
                        label="Chat Window | Cửa sổ chat",
                        elem_classes=["chatbox"],
                        height=400,
                    )

                    user_input = gr.Textbox(
                        placeholder="Type your message and press Enter... | Nhập tin nhắn và nhấn Enter...",
                        label="Your Message | Tin nhắn của bạn",
                        lines=2,
                    )

                    send_button = gr.Button("🚀 Send | Gửi", variant="primary")
                    clear_button = gr.Button("🧹 Clear Chat | Xóa chat", variant="secondary")

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
                                ["🧑‍💬 " + user_message, f"❌ Error | Lỗi: {str(e)}"]
                            )
                            yield history

                    def clear_chat():
                        """Reset the entire chat session."""
                        self._messages.clear()
                        return []

                    # Bind events
                    send_button.click(  # pylint: disable=no-member
                        fn=chat_stream,
                        inputs=[user_input, chat_box],
                        outputs=chat_box,
                    ).then(
                        fn=lambda: "",  # Clear input after sending
                        inputs=None,
                        outputs=user_input,
                    )

                    user_input.submit(  # pylint: disable=no-member
                        fn=chat_stream,
                        inputs=[user_input, chat_box],
                        outputs=chat_box,
                    ).then(
                        fn=lambda: "",  # Clear input after sending
                        inputs=None,
                        outputs=user_input,
                    )

                    clear_button.click(  # pylint: disable=no-member
                        fn=clear_chat,
                        inputs=None,
                        outputs=chat_box,
                    )

        return demo

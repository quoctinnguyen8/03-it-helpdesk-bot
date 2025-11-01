# 🛠️ IT Helpdesk Bot - RAG-Powered Technical Support# 💬 Knowledge Chatbot - RAG System



Hệ thống chatbot hỗ trợ kỹ thuật IT thông minh sử dụng **Retrieval-Augmented Generation (RAG)** để trả lời câu hỏi về troubleshooting, cung cấp giải pháp kỹ thuật dựa trên cơ sở kiến thức IT chuyên sâu. **Hỗ trợ đa ngôn ngữ (Tiếng Việt & English)**.Hệ thống chatbot AI thông minh sử dụng **Retrieval-Augmented Generation (RAG)** để trả lời câu hỏi dựa trên cơ sở kiến thức được tải lên. Chatbot có khả năng truy xuất thông tin từ tài liệu, kết hợp với sức mạnh của LLM để đưa ra câu trả lời chính xác và có nguồn tham chiếu rõ ràng.



------



## 🎯 Mục Tiêu Dự Án## 🎯 Mục Tiêu Dự Án



### Mục Tiêu Chính### Mục Tiêu Chính

- **Xây dựng hệ thống IT Helpdesk tự động** với khả năng trả lời câu hỏi kỹ thuật chính xác- **Xây dựng hệ thống chatbot RAG hoàn chỉnh** với khả năng truy xuất và tạo sinh câu trả lời dựa trên ngữ cảnh

- **Cung cấp giải pháp troubleshooting** cho Windows, Network, Hardware, Software, Security- **Quản lý cơ sở kiến thức** từ các file văn bản, cho phép import và lưu trữ tài liệu

- **Hỗ trợ đa ngôn ngữ** - Người dùng có thể hỏi bằng tiếng Việt hoặc English, bot sẽ trả lời bằng ngôn ngữ tương ứng- **Cung cấp giao diện thân thiện** để người dùng tương tác với chatbot

- **Trải nghiệm người dùng tốt** với streaming response (hiệu ứng đánh máy) và progress bar- **Đảm bảo tính minh bạch** bằng cách hiển thị nguồn tài liệu tham khảo cho mỗi câu trả lời



### Tính Năng Nổi Bật### Tính Năng Chính

✅ **Multi-format support** - Hỗ trợ nhiều định dạng file: TXT, PDF, Markdown (.md), JSON  
✅ **Multi-language support** - Tự động phát hiện và phản hồi bằng ngôn ngữ của người dùng  ✅ Upload nhiều file văn bản để xây dựng knowledge base  

✅ **Streaming responses** - Hiệu ứng typewriter effect cho trải nghiệm tự nhiên  ✅ Tự động chia nhỏ (chunking) và embedding tài liệu  

✅ **Progress bar** - Hiển thị tiến trình khi import tài liệu  ✅ Tìm kiếm ngữ nghĩa (semantic search) với ChromaDB  

✅ **RAG architecture** - Kết hợp vector search và LLM để đưa ra câu trả lời chính xác  ✅ Lọc và xếp hạng tài liệu liên quan bằng LLM  

✅ **IT-specific knowledge** - Tài liệu chuyên sâu về troubleshooting  ✅ Tạo sinh câu trả lời có nguồn gốc (grounded response)  

✅ **Step-by-step guidance** - Hướng dẫn từng bước giải quyết vấn đề  ✅ Giao diện Gradio đơn giản và dễ sử dụng  

✅ **Source references** - Hiển thị nguồn tài liệu tham khảo  ✅ Hỗ trợ Docker deployment  



------



## 🚀 Cách Chạy Dự Án## 🏗️ Kiến Trúc Dự Án



### Yêu Cầu Hệ ThốngDự án được xây dựng theo mô hình **Clean Architecture** với các lớp rõ ràng:

- Python 3.11+

- OpenAI API key```

- 2GB RAM+02-knowledge-chat-compressed/

- 1GB disk space│

├── src/knowledge_chat/

### Phương Pháp 1: Chạy Local│   ├── domain/              # Entities & Interfaces (Core Business Logic)

│   │   ├── entities/        # Message, Movie entities

#### Bước 1: Cài đặt│   │   └── interfaces/      # Abstract interfaces cho services

```bash│   │

cd 03-it-helpdesk-bot│   ├── application/         # Use Cases (Business Logic)

pip install -e .│   │   ├── chat_use_case.py           # RAG chat workflow

```│   │   └── import_files_use_case.py   # Document ingestion

│   │

#### Bước 2: Cấu hình `.env`│   ├── infrastructure/      # External Services Implementation

```bash│   │   ├── embedding_service/   # OpenAI embeddings

cp .env.example .env│   │   ├── llm_service/         # OpenAI LLM

# Chỉnh sửa .env với API keys│   │   ├── vector_store/        # ChromaDB

```│   │   ├── chunking/            # Text chunking

│   │   └── document_loader/     # Text file loader

#### Bước 3: Chạy│   │

```bash│   ├── presentation/        # UI Layer

python main.py│   │   └── ui_gradio.py     # Gradio interface

```│   │

│   ├── config/              # Configuration & Settings

Mở: **http://localhost:7860**│   │   ├── settings.py      # Environment config

│   │   └── prompts.py       # LLM prompt templates

### Phương Pháp 2: Docker│   │

```bash│   └── dependencies/        # Dependency Injection

docker build -t it-helpdesk-bot:v1 .│       └── get_*.py         # Factory functions

docker run -p 3000:3000 --env-file .env it-helpdesk-bot:v1│

```├── data/

│   ├── text_files/          # Sample documents

Mở: **http://localhost:3000**│   └── chroma_db/           # Vector database storage

│

---├── main.py                  # Application entry point

├── pyproject.toml          # Dependencies & project config

## 📖 Hướng Dẫn Sử Dụng├── Dockerfile              # Container configuration

└── .env.example            # Environment variables template

### 1. Import Documents```

- Upload file `.txt` 

- Xem progress bar### Luồng Hoạt Động (Workflow)

- Kiểm tra file đã import

#### 1️⃣ **Import Documents**

### 2. Chat với AI```

- Nhập câu hỏi (Tiếng Việt hoặc English)Upload Files → Load Text → Chunk Text → Generate Embeddings → Store in ChromaDB

- Xem streaming response```

- Bot tự động trả lời bằng ngôn ngữ bạn hỏi

#### 2️⃣ **Chat with RAG**

### Ví dụ:```

**English:** "How do I fix Windows blue screen error?"  User Query → Embed Query → Search Similar Docs → Filter with LLM → 

**Tiếng Việt:** "Làm sao sửa lỗi màn hình xanh Windows?"Generate Response → Return Answer + Sources

```

---

---

## 📊 Knowledge Base (8 files)

## 🛠️ Công Nghệ Sử Dụng

1. **windows_troubleshooting.txt** - BSOD, slow performance, WiFi, updates

2. **network_troubleshooting.txt** - No internet, slow speed, DNS, VPN### Core Technologies

3. **hardware_troubleshooting.txt** - Won't boot, overheating, RAM, HDD/SSD| Công nghệ | Phiên bản | Mục đích |

4. **software_troubleshooting.txt** - App crashes, Office, browsers|-----------|-----------|----------|

5. **security_antivirus.txt** - Malware, ransomware, phishing| **Python** | 3.11+ | Ngôn ngữ lập trình chính |

6. **email_communication.txt** - Outlook, Gmail, Zoom| **Gradio** | 5.49.1+ | Giao diện web tương tác |

7. **data_backup_recovery.txt** - Backup, recovery, cloning| **ChromaDB** | 1.2.1+ | Vector database cho similarity search |

8. **mobile_devices.txt** - Android, iPhone, tablets| **OpenAI API** | 2.6.1+ | LLM và embedding service |

| **LangChain** | 1.0.3+ | Framework xử lý LLM và RAG |

Mỗi file: **Bilingual (EN/VI)** + **Step-by-step solutions**| **Pydantic** | - | Validation và settings management |



---### Key Libraries

- **langchain-text-splitters** (1.0.0+): Chunking tài liệu

## 🔧 Các Điểm Đã Cải Thiện- **langchain-community** (0.4.1+): Các utility cho document loading

- **pydantic-settings** (2.11.0+): Quản lý environment configuration

### ✅ Hoàn Thành

### Development Tools

1. **Streaming Response** - Typewriter effect- **Docker**: Containerization

2. **Progress Bar** - Real-time import progress- **UV**: Fast Python package installer

3. **Multi-language** - EN/VI auto-detect & response- **isort** (7.0.0+): Code formatting

4. **IT-specific** - Technical support domain

5. **Enhanced UX** - Polished interface---



### 🔮 Có Thể Thêm## 🚀 Cách Chạy Dự Án



- Voice input/output### Yêu Cầu Hệ Thống

- Code syntax highlighting- Python 3.11 trở lên

- Export chat history- OpenAI API key (hoặc compatible endpoint)

- Hybrid search- 2GB RAM trở lên

- Analytics dashboard- 1GB disk space (cho vector database)

- Feedback system

### Phương Pháp 1: Chạy Trực Tiếp (Local)

---

#### Bước 1: Clone và cài đặt dependencies

## 🛠️ Tech Stack```bash

cd 02-knowledge-chat-compressed

- **Python 3.11+**pip install -e .

- **Gradio 5.49.1+** - UI với streaming```

- **ChromaDB 1.2.1+** - Vector database

- **OpenAI API 2.6.1+** - LLM & embeddings#### Bước 2: Cấu hình biến môi trường

- **LangChain 1.0.3+** - RAG frameworkTạo file `.env` từ `.env.example`:

```bash

---cp .env.example .env

```

## 🆚 So Sánh Phiên Bản

Chỉnh sửa file `.env`:

| Feature | Original | IT Helpdesk Bot ✨ |```bash

|---------|----------|-------------------|# Python path

| Streaming | ❌ | ✅ |PYTHONPATH=./src

| Progress Bar | ❌ | ✅ |

| Multi-language | ❌ | ✅ EN/VI |# OpenAI Configuration

| Domain | General | ✅ IT-specific |OPENAI_BASE_URL=https://aiportalapi.stu-platform.live/jpe

OPENAI_API_KEY=your_api_key_here

---OPENAI_MODEL=gpt-4o-mini



## 📚 Documentation# Embedding Configuration

OPENAI_EMBEDDING_BASE_URL=https://aiportalapi.stu-platform.live/jpe

Full documentation in README with:OPENAI_EMBEDDING_KEY=your_api_key_here

- Architecture details```

- Configuration options

- Testing guidelines#### Bước 3: Chạy ứng dụng

- Troubleshooting tips```bash

- Comparison with originalpython main.py

```

---

Ứng dụng sẽ khởi động tại: **http://localhost:7860**

**Made with ❤️ for IT Support Teams**  

**Được tạo với ❤️ cho Đội ngũ Hỗ trợ IT**---


### Phương Pháp 2: Chạy với Docker 🐳

#### Bước 1: Build Docker image
```bash
docker build -t knowledge-chat:v1 .
```

#### Bước 2: Chạy container
```bash
docker run -p 3000:3000 --name knowledge-chat-v1 --env-file .env knowledge-chat:v1
```

Hoặc với docker-compose (nếu có):
```bash
docker-compose up -d
```

Ứng dụng sẽ khởi động tại: **http://localhost:3000**

---

## 📖 Hướng Dẫn Sử Dụng

### 1. Import Documents (Xây dựng Knowledge Base)

1. Mở tab **"📁 Import Documents"**
2. Click **"Upload one or more .txt files"**
3. Chọn các file văn bản từ thư mục `data/text_files/` (hoặc file của bạn)
4. Hệ thống sẽ:
   - Đọc nội dung các file
   - Chia nhỏ thành chunks (mặc định 1000 ký tự, overlap 200)
   - Tạo embeddings cho mỗi chunk
   - Lưu vào ChromaDB vector store

### 2. Chat với AI

1. Mở tab **"💬 Chat"**
2. Nhập câu hỏi vào ô chat
3. Chatbot sẽ:
   - Tìm kiếm các tài liệu liên quan
   - Lọc và xếp hạng theo độ phù hợp
   - Tạo câu trả lời dựa trên ngữ cảnh
   - Hiển thị nguồn tài liệu tham khảo

### Ví dụ câu hỏi:
- "What is RAG and how does it work?"
- "Explain blockchain technology"
- "What are the effects of climate change?"
- "Tell me about quantum computing"

---

## 📊 Sample Data

Dự án đi kèm với 12 file văn bản mẫu trong `data/text_files/`:

| File | Nội dung |
|------|----------|
| `ai_overview.txt` | Tổng quan về AI |
| `blockchain_intro.txt` | Giới thiệu Blockchain |
| `climate_change.txt` | Biến đổi khí hậu |
| `cybersecurity_basics.txt` | Bảo mật mạng cơ bản |
| `history_of_internet.txt` | Lịch sử Internet |
| `langchain_intro.txt` | Giới thiệu LangChain |
| `mental_health_awareness.txt` | Nhận thức sức khỏe tâm thần |
| `neuroscience_brain.txt` | Khoa học thần kinh |
| `quantum_computing.txt` | Máy tính lượng tử |
| `rag_concept.txt` | Khái niệm RAG |
| `renewable_energy.txt` | Năng lượng tái tạo |
| `space_exploration.txt` | Khám phá vũ trụ |

Bạn có thể thay thế hoặc thêm các file `.txt` của riêng mình.

---

## ⚙️ Cấu Hình Chi Tiết

### Environment Variables

Tất cả cấu hình được quản lý trong file `.env`:

```bash
# ==================== OpenAI LLM ====================
OPENAI_BASE_URL=https://aiportalapi.stu-platform.live/jpe
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o-mini

# ==================== Embeddings ====================
OPENAI_EMBEDDING_BASE_URL=https://aiportalapi.stu-platform.live/jpe
OPENAI_EMBEDDING_KEY=sk-xxx
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

# ==================== Vector Database ====================
CHROMA_DB_PATH=./data/chroma_db
CHROMADB_COLLECTION_NAME=knowledge_documents

# ==================== Text Chunking ====================
CHUNKER_CHUNK_SIZE=1000
CHUNKER_CHUNK_OVERLAP=200
CHUNKER_SEPARATORS=["\n\n", "\n", ".", " ", ""]
```

### Tùy Chỉnh Chunking

Trong file `settings.py`, bạn có thể điều chỉnh:
- `chunker_chunk_size`: Kích thước mỗi chunk (ký tự)
- `chunker_chunk_overlap`: Độ chồng lấp giữa các chunks
- `chunker_separators`: Các ký tự dùng để chia văn bản

### Tùy Chỉnh Prompts

Chỉnh sửa file `src/knowledge_chat/config/prompts.py` để thay đổi:
- `CHAT_PROMPT_TEMPLATE`: Prompt cho chat response
- `RERANK_FILTER_PROMPT_TEMPLATE`: Prompt cho filtering documents

---

## 🔧 Các Điểm Có Thể Cải Thiện

### 1. **Hỗ trợ nhiều định dạng file hơn**
   - ❌ Hiện tại: Chỉ hỗ trợ `.txt`
   - ✅ Cải thiện: Thêm PDF, DOCX, Markdown, HTML
   - **Implementation**: 
     - Sử dụng `PyPDF2`, `python-docx`, `markdown`
     - Tạo loaders mới trong `infrastructure/document_loader/`

### 2. **Cải thiện chiến lược Chunking**
   - ❌ Hiện tại: Chunking cố định theo ký tự
   - ✅ Cải thiện: Semantic chunking, sentence-aware chunking
   - **Implementation**:
     - Sử dụng `langchain.text_splitters.SemanticChunker`
     - Thêm NLP-based chunking với spaCy

### 3. **Advanced Retrieval Techniques**
   - ❌ Hiện tại: Simple similarity search
   - ✅ Cải thiện: 
     - Hybrid search (keyword + semantic)
     - Re-ranking với Cross-encoder
     - Query expansion
     - Multi-query retrieval
   - **Implementation**:
     - Tích hợp `Cohere Rerank` hoặc `sentence-transformers/cross-encoder`
     - Thêm BM25 với `rank_bm25`

### 4. **Caching và Performance**
   - ❌ Hiện tại: Embed query mỗi lần chat
   - ✅ Cải thiện:
     - Cache embeddings cho queries phổ biến
     - Batch processing cho import
     - Lazy loading
   - **Implementation**:
     - Redis hoặc `functools.lru_cache`
     - Async processing với `asyncio`

### 5. **User Experience Improvements**
   - ✅ Thêm streaming response (typewriter effect)
   - ✅ Hiển thị progress bar khi import
   - ✅ Export chat history
   - ✅ Highlight relevant text trong documents
   - ✅ Thêm feedback mechanism (👍/👎)
   - **Implementation**:
     - Sử dụng Gradio streaming
     - SQLite để lưu chat history

### 6. **Multi-language Support**
   - ❌ Hiện tại: Chủ yếu English
   - ✅ Cải thiện: Hỗ trợ tiếng Việt và các ngôn ngữ khác
   - **Implementation**:
     - Multi-lingual embedding models
     - Language detection
     - Translation layer

### 7. **Authentication & Multi-user**
   - ❌ Hiện tại: Single-user, no auth
   - ✅ Cải thiện:
     - User authentication
     - Per-user knowledge bases
     - Role-based access control
   - **Implementation**:
     - JWT authentication
     - User management database
     - Separate ChromaDB collections per user

### 8. **Monitoring & Analytics**
   - ✅ Log user queries
   - ✅ Track response quality
   - ✅ Monitor API costs
   - ✅ Query analytics dashboard
   - **Implementation**:
     - Prometheus + Grafana
     - ELK stack
     - Custom analytics dashboard

### 9. **Advanced RAG Techniques**
   - ✅ **RAPTOR**: Recursive chunking với clustering
   - ✅ **GraphRAG**: Knowledge graph-based retrieval
   - ✅ **Agentic RAG**: Self-reflective RAG với agents
   - ✅ **Corrective RAG**: Tự động sửa lỗi retrieval
   - **Implementation**:
     - Integrate LangGraph
     - Neo4j cho graph database
     - Custom agent frameworks

### 10. **Testing & Quality Assurance**
   - ❌ Hiện tại: Không có tests
   - ✅ Cải thiện:
     - Unit tests cho mỗi component
     - Integration tests
     - End-to-end tests
     - RAG evaluation metrics (faithfulness, relevance)
   - **Implementation**:
     - `pytest`, `pytest-cov`
     - RAGAs framework cho evaluation

### 11. **Scalability**
   - ❌ Hiện tại: Single instance
   - ✅ Cải thiện:
     - Horizontal scaling
     - Load balancing
     - Distributed vector database
   - **Implementation**:
     - Kubernetes deployment
     - Pinecone/Weaviate thay vì ChromaDB
     - Message queue (RabbitMQ/Kafka)

### 12. **Cost Optimization**
   - ✅ Sử dụng local LLM (Ollama, LLaMA)
   - ✅ Caching để giảm API calls
   - ✅ Batch requests
   - **Implementation**:
     - Ollama integration
     - LangChain cache backends

---

## 🧪 Testing

### Chạy Unit Tests (Nếu có)
```bash
pytest tests/ -v --cov=src/knowledge_chat
```

### Manual Testing
1. Upload file và kiểm tra import
2. Test với các câu hỏi khác nhau
3. Kiểm tra accuracy của references
4. Test với large documents

---

## 🐛 Troubleshooting

### Lỗi thường gặp:

#### 1. **ChromaDB Connection Error**
```
Solution: Xóa thư mục data/chroma_db và restart
```

#### 2. **OpenAI API Error**
```
- Kiểm tra API key trong .env
- Kiểm tra OPENAI_BASE_URL
- Verify quota và credits
```

#### 3. **Import thất bại**
```
- Kiểm tra format file (.txt)
- Verify encoding (UTF-8)
- Check file size
```

#### 4. **Docker port conflict**
```bash
# Thay đổi port
docker run -p 8080:3000 knowledge-chat:v1
```

---

## 📚 Tài Liệu Tham Khảo

- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Gradio Documentation](https://www.gradio.app/docs/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [RAG Paper (Lewis et al., 2020)](https://arxiv.org/abs/2005.11401)

---

## 👥 Đóng Góp

Mọi đóng góp đều được hoan nghênh! Vui lòng:
1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 📧 Contact

Nếu có câu hỏi hoặc góp ý, vui lòng liên hệ qua:
- GitHub Issues
- Email: your-email@example.com

---

## 🙏 Acknowledgments

- OpenAI cho LLM và embedding models
- LangChain team cho framework tuyệt vời
- ChromaDB cho vector database
- Gradio cho giao diện thân thiện

---

**Made with ❤️ for the AI Community**

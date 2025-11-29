# 🛠️ MÔ TẢ CÁC CÔNG NGHỆ ĐƯỢC SỬ DỤNG TRONG WEB APPLICATION

Tài liệu này mô tả chi tiết từng công nghệ, framework, và thư viện được sử dụng trong dự án SenpaiAI, cùng với cách chúng được áp dụng trong từng phần của ứng dụng.

---

## 📋 MỤC LỤC

1. [Frontend Technologies](#frontend-technologies)
2. [Backend Technologies](#backend-technologies)
3. [Database & Storage](#database--storage)
4. [AI & Machine Learning](#ai--machine-learning)
5. [Development Tools](#development-tools)
6. [Security & Authentication](#security--authentication)
7. [API & Communication](#api--communication)

---

## 🎨 FRONTEND TECHNOLOGIES

### 1. React 18.2.0
**Mục đích**: UI Framework chính cho giao diện người dùng

**Cách sử dụng**:
- Xây dựng các component tái sử dụng (Layout, LoadingSpinner)
- Quản lý state với React Hooks (useState, useEffect, useContext)
- Tạo các trang: Login, Chat, Grammar, Library, Profile
- Xử lý routing và navigation giữa các trang

**Vị trí trong code**:
- `frontend/src/pages/` - Các trang chính
- `frontend/src/components/` - Components tái sử dụng
- `frontend/src/App.tsx` - Component root

**Ví dụ sử dụng**:
```typescript
// frontend/src/pages/Chat.tsx
import { useState, useRef, useEffect } from 'react'

export default function Chat() {
  const [searchQuery, setSearchQuery] = useState('')
  // ... component logic
}
```

---

### 2. TypeScript 5.2.2
**Mục đích**: Type safety và code quality

**Cách sử dụng**:
- Định nghĩa interfaces cho props, state, và API responses
- Type checking tại compile time
- IntelliSense và autocomplete trong IDE
- Giảm lỗi runtime bằng type validation

**Vị trí trong code**:
- `frontend/tsconfig.json` - TypeScript configuration
- Tất cả file `.tsx` và `.ts` trong `frontend/src/`

**Ví dụ sử dụng**:
```typescript
// frontend/src/pages/Chat.tsx
interface ChatMessage {
  id: number
  question: string
  answer: string
  jlpt_level?: string
  grammar_points?: any[]
  created_at: string
}
```

---

### 3. Vite 4.5.0
**Mục đích**: Build tool và development server

**Cách sử dụng**:
- Development server với Hot Module Replacement (HMR)
- Build production bundle tối ưu
- Fast refresh khi code thay đổi
- Module bundling và code splitting

**Vị trí trong code**:
- `frontend/vite.config.ts` - Vite configuration
- `frontend/package.json` - Scripts: `npm run dev`, `npm run build`

**Tính năng**:
- ES modules support
- Fast cold start
- Optimized production builds
- Plugin system (React plugin)

---

### 4. React Router DOM 6.20.1
**Mục đích**: Client-side routing và navigation

**Cách sử dụng**:
- Định nghĩa routes cho các trang
- Protected routes (yêu cầu authentication)
- Navigation giữa các trang
- URL parameters và query strings

**Vị trí trong code**:
- `frontend/src/App.tsx` - Route definitions

**Ví dụ sử dụng**:
```typescript
// frontend/src/App.tsx
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'

<Routes>
  <Route path="/login" element={<Login />} />
  <Route path="/chat" element={<ProtectedRoute><Chat /></ProtectedRoute>} />
</Routes>
```

---

### 5. React Query (TanStack Query) 3.39.3
**Mục đích**: Data fetching, caching, và state management cho server state

**Cách sử dụng**:
- Fetch data từ API endpoints
- Automatic caching và refetching
- Optimistic updates
- Loading và error states
- Background data synchronization

**Vị trí trong code**:
- `frontend/src/pages/Chat.tsx` - Chat history fetching
- `frontend/src/pages/Library.tsx` - Document fetching
- `frontend/src/services/api.ts` - API calls với React Query

**Ví dụ sử dụng**:
```typescript
// frontend/src/pages/Chat.tsx
import { useQuery, useMutation } from 'react-query'

const { data: chatHistory, isLoading } = useQuery(
  ['chatHistory'],
  () => chatAPI.getHistory(limit, offset)
)
```

---

### 6. React Hook Form 7.48.2
**Mục đích**: Form handling và validation

**Cách sử dụng**:
- Quản lý form state
- Form validation
- Error handling
- Performance optimization (uncontrolled components)

**Vị trí trong code**:
- `frontend/src/pages/Login.tsx` - Login form
- `frontend/src/pages/Grammar.tsx` - Grammar analysis form
- `frontend/src/pages/Profile.tsx` - Profile update form

**Ví dụ sử dụng**:
```typescript
// frontend/src/pages/Login.tsx
import { useForm } from 'react-hook-form'

const form = useForm<LoginFormData>({
  defaultValues: { email: '', password: '' }
})

<form onSubmit={form.handleSubmit(handleSubmit)}>
  <input {...form.register('email', { required: true })} />
</form>
```

---

### 7. Axios 1.6.2
**Mục đích**: HTTP client cho API calls

**Cách sử dụng**:
- Gửi HTTP requests (GET, POST, PUT, DELETE)
- Request/Response interceptors
- Automatic JSON parsing
- Error handling
- Request cancellation

**Vị trí trong code**:
- `frontend/src/services/api.ts` - Centralized API client

**Ví dụ sử dụng**:
```typescript
// frontend/src/services/api.ts
import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' }
})

// Interceptor để thêm JWT token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

---

### 8. TailwindCSS 3.3.5
**Mục đích**: Utility-first CSS framework

**Cách sử dụng**:
- Styling components với utility classes
- Responsive design
- Custom theme configuration
- Dark mode support (nếu cần)

**Vị trí trong code**:
- `frontend/tailwind.config.js` - Tailwind configuration
- `frontend/src/index.css` - Tailwind directives
- Tất cả file `.tsx` - Sử dụng Tailwind classes

**Ví dụ sử dụng**:
```tsx
// frontend/src/pages/Chat.tsx
<div className="bg-white border border-gray-200 rounded-lg p-3">
  <p className="text-sm text-gray-900">Message content</p>
</div>
```

---

### 9. Lucide React 0.294.0
**Mục đích**: Icon library

**Cách sử dụng**:
- Hiển thị icons trong UI
- Consistent icon design
- Tree-shakeable (chỉ import icons cần dùng)

**Vị trí trong code**:
- Tất cả file components và pages

**Ví dụ sử dụng**:
```typescript
import { Send, Bot, User, BookOpen } from 'lucide-react'

<Send className="h-4 w-4" />
<Bot className="h-8 w-8 text-white" />
```

---

### 10. React Hot Toast 2.4.1
**Mục đích**: Toast notifications

**Cách sử dụng**:
- Hiển thị success/error messages
- Non-intrusive notifications
- Auto-dismiss
- Customizable styling

**Vị trí trong code**:
- `frontend/src/App.tsx` - Toast provider
- Tất cả pages - Sử dụng `toast.success()`, `toast.error()`

**Ví dụ sử dụng**:
```typescript
import toast from 'react-hot-toast'

toast.success('Message sent successfully!')
toast.error('Failed to send message')
```

---

### 11. clsx & tailwind-merge
**Mục đích**: Conditional className utilities

**Cách sử dụng**:
- Combine Tailwind classes conditionally
- Merge conflicting Tailwind classes
- Dynamic styling

**Ví dụ sử dụng**:
```typescript
import clsx from 'clsx'
import { twMerge } from 'tailwind-merge'

<div className={twMerge(clsx(
  'base-class',
  condition && 'conditional-class'
))} />
```

---

## ⚙️ BACKEND TECHNOLOGIES

### 1. FastAPI 0.104.1
**Mục đích**: Modern Python web framework cho REST API

**Cách sử dụng**:
- Định nghĩa API endpoints
- Automatic API documentation (Swagger/OpenAPI)
- Request/Response validation với Pydantic
- Async/await support
- Dependency injection

**Vị trí trong code**:
- `backend/app/main.py` - FastAPI app instance
- `backend/app/api/` - API routers (auth, chat, analysis, library)

**Ví dụ sử dụng**:
```python
# backend/app/api/chat.py
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/message", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    current_user: User = Depends(get_current_active_user)
):
    # ... endpoint logic
```

**Tính năng**:
- Automatic OpenAPI docs tại `/docs`
- Type hints cho validation
- Fast performance (tương đương Node.js)
- WebSocket support (nếu cần)

---

### 2. Uvicorn 0.24.0
**Mục đích**: ASGI server để chạy FastAPI

**Cách sử dụng**:
- Development server với auto-reload
- Production server với workers
- ASGI protocol support

**Vị trí trong code**:
- `backend/start.ps1`, `backend/start.bat` - Startup scripts
- Command: `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

**Tính năng**:
- Hot reload trong development
- Multiple workers trong production
- HTTP/1.1 và HTTP/2 support

---

### 3. SQLAlchemy 2.0.23
**Mục đích**: Python ORM (Object-Relational Mapping)

**Cách sử dụng**:
- Định nghĩa database models
- Database queries (CRUD operations)
- Relationship management
- Session management

**Vị trí trong code**:
- `backend/app/models/database.py` - Database models
- `backend/app/core/database.py` - Database connection và session

**Ví dụ sử dụng**:
```python
# backend/app/models/database.py
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    # ...

# backend/app/api/auth.py
db_user = db.query(UserDB).filter(UserDB.email == email).first()
```

---

### 4. Alembic 1.13.1
**Mục đích**: Database migration tool

**Cách sử dụng**:
- Tạo database migrations
- Apply migrations
- Rollback migrations
- Version control cho database schema

**Vị trí trong code**:
- `backend/alembic/` - Migration files
- `backend/alembic.ini` - Alembic configuration

**Commands**:
```bash
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1
```

---

### 5. Pydantic 2.5.0
**Mục đích**: Data validation và settings management

**Cách sử dụng**:
- Request/Response validation
- Settings management
- Type conversion
- Serialization/Deserialization

**Vị trí trong code**:
- `backend/app/models/schemas.py` - Pydantic models
- `backend/app/core/config.py` - Settings với Pydantic Settings

**Ví dụ sử dụng**:
```python
# backend/app/models/schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

# FastAPI tự động validate request body
@router.post("/register", response_model=User)
async def register(user: UserCreate):
    # user đã được validate
```

---

### 6. Python-dotenv 1.0.0
**Mục đích**: Load environment variables từ .env file

**Cách sử dụng**:
- Load configuration từ `.env`
- Keep secrets out of code
- Different configs cho dev/prod

**Vị trí trong code**:
- `backend/app/core/config.py` - Load .env file
- `backend/.env` - Environment variables

**Ví dụ sử dụng**:
```python
# backend/app/core/config.py
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    # ...
```

---

### 7. Python-multipart 0.0.6
**Mục đích**: Parse multipart/form-data (file uploads)

**Cách sử dụng**:
- Handle file uploads
- Form data parsing

**Vị trí trong code**:
- Sử dụng khi cần upload files (nếu có)

---

### 8. Aiofiles 23.2.1
**Mục đích**: Async file operations

**Cách sử dụng**:
- Read/write files asynchronously
- Non-blocking file I/O

**Vị trí trong code**:
- Sử dụng khi cần async file operations

---

### 9. Jinja2 3.1.2
**Mục đích**: Template engine

**Cách sử dụng**:
- Generate HTML templates
- Email templates (nếu có)
- Dynamic content rendering

**Vị trí trong code**:
- Có thể sử dụng cho email templates hoặc HTML reports

---

## 🗄️ DATABASE & STORAGE

### 1. PostgreSQL
**Mục đích**: Relational database chính

**Cách sử dụng**:
- Lưu trữ users, chat history, learning sessions
- ACID transactions
- Complex queries
- Foreign keys và relationships

**Vị trí trong code**:
- `backend/app/core/database.py` - Database connection
- `backend/app/models/database.py` - Table definitions
- Connection string trong `.env`: `DATABASE_URL`

**Schema chính**:
- `users` - User accounts
- `chat_history` - Chat messages
- `learning_sessions` - Learning session data
- `documents` - Learning library documents

---

### 2. ChromaDB 0.4.18
**Mục đích**: Vector database cho RAG (Retrieval-Augmented Generation) và semantic search

**Cách sử dụng**:
- Lưu trữ document embeddings (vector representations)
- Semantic similarity search
- Metadata filtering (JLPT level, document type)
- RAG context retrieval cho AI responses

**Vị trí trong code**:
- `backend/app/services/vector_db.py` - ChromaDB service implementation
- `backend/app/core/config.py` - ChromaDB configuration (persist_directory)

**Kiến trúc**:
- **Persistent Storage**: Lưu trữ local tại `./chroma_db`
- **Collection**: "japanese_learning" collection
- **Similarity Metric**: Cosine similarity (hnsw:space)
- **Automatic Embeddings**: ChromaDB tự động tạo embeddings từ text

**Ví dụ sử dụng**:
```python
# backend/app/services/vector_db.py
import chromadb
from chromadb.config import Settings as ChromaSettings

# Initialize persistent client
client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=ChromaSettings(
        anonymized_telemetry=False,
        allow_reset=True
    )
)

# Get or create collection
collection = client.get_or_create_collection(
    name="japanese_learning",
    metadata={"hnsw:space": "cosine"}  # Cosine similarity
)

# Add documents (embeddings tự động)
collection.add(
    documents=["Japanese grammar explanation..."],
    metadatas=[{
        "document_id": "1",
        "title": "Grammar Guide",
        "jlpt_level": "N5",
        "document_type": "grammar"
    }],
    ids=["doc_1_chunk_0"]
)

# Semantic search
results = collection.query(
    query_texts=["What is は particle?"],
    n_results=3,
    where={"jlpt_level": "N5"}  # Metadata filter
)
```

**Tính năng nâng cao**:
- **Chunking**: Documents được split thành chunks (1000 chars, 200 overlap)
- **Metadata Filtering**: Filter theo JLPT level, document type, tags
- **Similarity Scoring**: Cosine distance → similarity score (1 - distance)
- **Telemetry Disabled**: Privacy-first, không gửi data đi đâu
- **HNSW Index**: Fast approximate nearest neighbor search

**Integration với AI**:
- Documents được embed và lưu trong ChromaDB
- User queries được embed và search trong ChromaDB
- Top-k relevant documents được retrieve làm context
- Context được inject vào LLM prompt cho RAG

**Xem thêm**: Chi tiết về RAG và Semantic Search trong phần [AI & Machine Learning](#-ai--machine-learning)

---

## 🤖 AI & MACHINE LEARNING

### 1. Ollama 0.1.7
**Mục đích**: Local LLM runtime - Chạy Large Language Models trên máy local

**Cách sử dụng**:
- Chạy LLM models locally (không cần API key, miễn phí)
- Chat completions với system và user messages
- Text generation cho các tác vụ AI
- Grammar analysis và translation
- JLPT level prediction

**Vị trí trong code**:
- `backend/app/services/ollama_service.py` - Ollama service implementation
- `backend/app/core/config.py` - Ollama configuration (model, base_url)

**Ví dụ sử dụng**:
```python
# backend/app/services/ollama_service.py
import ollama

# Chat completion
response = ollama.chat(
    model='gemma:2b',
    messages=[
        {'role': 'system', 'content': 'You are SenpaiAI, a Japanese tutor.'},
        {'role': 'user', 'content': 'Explain は and が particles'}
    ]
)
answer = response['message']['content']

# Generate text
response = ollama.generate(
    model='gemma:2b',
    prompt='Translate to Japanese: Hello'
)
```

**Models được sử dụng**:
- **gemma:2b** (Mặc định) - Nhẹ, nhanh, phù hợp cho mọi máy
- **gemma:7b** - Chất lượng cao hơn, cần nhiều RAM
- **llama2, llama3** - Models phổ biến
- **mistral** - Model chất lượng cao
- **nomic-embed-text** - Embedding model cho RAG

**Tính năng**:
- Retry logic với error handling
- Connection checking
- Model availability checking
- Fallback mechanisms

**Setup**:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh  # Linux/Mac
# Windows: Download từ https://ollama.ai/download

# Pull models
ollama pull gemma:2b
ollama pull nomic-embed-text  # Cho embeddings
```

---

### 2. LangChain Core & Community
**Mục đích**: LLM framework và abstractions cho AI applications

**Cách sử dụng**:
- LLM provider abstraction (Ollama, OpenAI)
- Prompt templates và message formatting
- Chain composition cho complex workflows
- Text splitting utilities cho RAG
- Message types (SystemMessage, HumanMessage, AIMessage)

**Vị trí trong code**:
- `backend/app/services/llm_service.py` - LangChain integration
- `backend/app/services/vector_db.py` - Text splitting với LangChain

**Ví dụ sử dụng**:
```python
# backend/app/services/llm_service.py
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate

# Prompt template
self.chat_prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are SenpaiAI, a helpful Japanese learning assistant."),
    HumanMessage(content="{question}")
])

# Format và sử dụng
messages = self.chat_prompt.format_messages(question=user_question)
response = await self.llm.agenerate([messages])
```

**Components**:
- `langchain-core` (>=0.1.0) - Core abstractions, prompts, messages
- `langchain-community` (>=0.0.10) - Community integrations (OpenAI, etc.)
- `langchain-text-splitters` (>=0.0.1) - Text splitting cho documents

**Prompt Engineering**:
- System prompts cho role definition
- Context-aware prompts với RAG
- Structured output prompts (JSON format)
- Multi-turn conversation support

---

### 3. RAG (Retrieval-Augmented Generation)
**Mục đích**: Cải thiện chất lượng AI responses bằng cách kết hợp retrieval và generation

**Cách hoạt động**:
1. User query → Semantic search trong vector database
2. Retrieve relevant documents → Build context
3. Combine context với user question → Enhanced prompt
4. LLM generates response với context → More accurate answers

**Vị trí trong code**:
- `backend/app/services/vector_db.py` - RAG retrieval logic
- `backend/app/api/chat.py` - RAG integration trong chat endpoint
- `backend/app/services/ollama_service.py` - Context injection

**Ví dụ sử dụng**:
```python
# backend/app/api/chat.py
# 1. Get relevant context từ vector DB
context = chroma_service.get_relevant_context(
    message.message, 
    message.jlpt_level or current_user.current_jlpt_level
)

# 2. Inject context vào prompt
enhanced_question = f"Context: {context}\n\nQuestion: {question}"

# 3. Generate response với context
response_data = await japanese_service.chat_response(
    question=message.message,
    context=context,
    jlpt_level=jlpt_level
)
```

**Lợi ích**:
- More accurate responses với domain knowledge
- Up-to-date information từ documents
- Reduced hallucinations
- Context-aware answers

---

### 4. ChromaDB 0.4.18 - Vector Database
**Mục đích**: Vector database cho semantic search và RAG

**Cách sử dụng**:
- Lưu trữ document embeddings
- Semantic similarity search
- Metadata filtering (JLPT level, document type)
- Cosine similarity cho relevance scoring

**Vị trí trong code**:
- `backend/app/services/vector_db.py` - ChromaDB service

**Ví dụ sử dụng**:
```python
# backend/app/services/vector_db.py
import chromadb

# Initialize client
client = chromadb.PersistentClient(path="./chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="japanese_learning",
    metadata={"hnsw:space": "cosine"}  # Cosine similarity
)

# Add documents với embeddings tự động
collection.add(
    documents=["Japanese grammar explanation..."],
    metadatas=[{
        "document_id": "1",
        "title": "Grammar Guide",
        "jlpt_level": "N5"
    }],
    ids=["doc_1"]
)

# Semantic search
results = collection.query(
    query_texts=["What is は particle?"],
    n_results=3,
    where={"jlpt_level": "N5"}  # Filter by metadata
)
```

**Tính năng**:
- **Automatic Embeddings**: ChromaDB tự động tạo embeddings
- **Persistent Storage**: Lưu trữ local, không cần server riêng
- **Metadata Filtering**: Filter theo JLPT level, document type
- **Similarity Scoring**: Cosine similarity cho relevance
- **Chunking**: Documents được split thành chunks để tối ưu search

**Embedding Model**:
- Sử dụng ChromaDB's default embedding function
- Có thể cấu hình custom embedding model (nomic-embed-text)

---

### 5. Text Splitting (LangChain Text Splitters)
**Mục đích**: Chia documents thành chunks phù hợp cho vector search

**Cách sử dụng**:
- Split documents thành chunks nhỏ hơn
- Overlap giữa chunks để giữ context
- Optimize chunk size cho embeddings

**Vị trí trong code**:
- `backend/app/services/vector_db.py` - RecursiveCharacterTextSplitter

**Ví dụ sử dụng**:
```python
# backend/app/services/vector_db.py
from langchain_text_splitters import RecursiveCharacterTextSplitter

self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Mỗi chunk ~1000 characters
    chunk_overlap=200,    # Overlap 200 chars giữa chunks
    length_function=len,
)

# Split document
chunks = self.text_splitter.split_text(document_content)

# Mỗi chunk được embed và lưu riêng
for chunk in chunks:
    collection.add(documents=[chunk], ...)
```

**Tại sao cần splitting**:
- Embeddings có giới hạn token length
- Smaller chunks = better semantic search
- Overlap giữ nguyên context giữa các chunks

---

### 6. Semantic Search
**Mục đích**: Tìm kiếm documents dựa trên ý nghĩa, không chỉ keywords

**Cách hoạt động**:
1. User query → Convert thành embedding vector
2. Compare với document embeddings → Similarity scores
3. Return top-k most similar documents

**Vị trí trong code**:
- `backend/app/services/vector_db.py` - `search_documents()` method
- `backend/app/api/library.py` - Library search endpoint

**Ví dụ sử dụng**:
```python
# backend/app/services/vector_db.py
def search_documents(self, query: str, n_results: int = 5):
    results = self.collection.query(
        query_texts=[query],
        n_results=n_results,
        where={"jlpt_level": "N5"}  # Optional filter
    )
    
    # Format results với similarity scores
    for result in results:
        similarity_score = 1 - result['distance']  # Convert to similarity
        # Higher score = more relevant
```

**Ưu điểm so với keyword search**:
- Hiểu được ý nghĩa, không chỉ từ khóa
- Tìm được documents liên quan ngay cả khi không có exact match
- Multilingual support (Japanese, Vietnamese)

---

### 7. Prompt Engineering
**Mục đích**: Thiết kế prompts hiệu quả để LLM hiểu và trả lời chính xác

**Các loại prompts được sử dụng**:

#### a) Chat Prompt
```python
system_prompt = """You are SenpaiAI, a helpful Japanese learning assistant. 
You provide accurate, educational responses about Japanese language, culture, and grammar.
Always include relevant examples and explanations suitable for the user's JLPT level."""
```

#### b) Grammar Analysis Prompt
```python
system_prompt = """You are a Japanese grammar expert. Analyze the given Japanese text and provide:
1. JLPT level assessment (N5-N1)
2. Grammar points with explanations
3. Difficulty score (0-10)
4. Learning suggestions

Format your response as JSON with these fields:
- jlpt_level: string
- grammar_points: array of objects with 'pattern', 'explanation', 'example'
- difficulty_score: number
- suggestions: array of strings"""
```

#### c) Translation Prompt
```python
system_prompt = """You are a professional Japanese-Vietnamese translator.
Provide accurate, natural translations while preserving the original meaning and tone.
For Japanese to Vietnamese: Provide both literal and natural translations."""
```

#### d) JLPT Prediction Prompt
```python
system_prompt = """You are a JLPT level assessment expert. 
Analyze Japanese text and determine the appropriate JLPT level (N5-N1).
Consider vocabulary difficulty, grammar complexity, and kanji usage.
Respond with just the JLPT level (e.g., "N3")."""
```

**Vị trí trong code**:
- `backend/app/services/llm_service.py` - Prompt templates
- `backend/app/services/ollama_service.py` - Prompt definitions

**Best Practices**:
- Clear role definition (system prompt)
- Structured output format (JSON)
- Context injection (RAG context, JLPT level)
- Examples trong prompts (few-shot learning)

---

### 8. Context Management
**Mục đích**: Quản lý context để LLM có đủ thông tin để trả lời

**Các loại context**:

#### a) RAG Context
- Retrieved documents từ vector database
- Relevant information cho user question
- Filtered by JLPT level

#### b) User Context
- Current JLPT level
- Learning goals
- Previous conversation history

#### c) System Context
- Application state
- User preferences
- Session information

**Ví dụ sử dụng**:
```python
# Combine multiple context sources
enhanced_question = f"""
User's JLPT level: {jlpt_level}
Context from documents: {rag_context}

Question: {user_question}
"""
```

---

### 9. NumPy 1.24.3
**Mục đích**: Numerical computing cho vector operations

**Cách sử dụng**:
- Vector operations cho embeddings
- Array operations
- Mathematical computations
- Distance calculations (nếu cần custom)

**Vị trí trong code**:
- Sử dụng trong vector operations (nếu cần custom similarity)
- ChromaDB sử dụng NumPy internally

**Use cases**:
- Custom embedding calculations
- Vector similarity computations
- Data preprocessing

---

### 10. Pandas 2.0.3
**Mục đích**: Data analysis và manipulation

**Cách sử dụng**:
- Data processing cho learning analytics
- CSV/Excel file handling
- Data analysis và statistics
- Learning progress tracking

**Vị trí trong code**:
- Có thể sử dụng cho data analysis features
- Learning statistics và reports

---

### 11. AI Features Implementation

#### a) Chat với AI
- **RAG Integration**: Sử dụng relevant documents để enhance responses
- **Context-aware**: Hiểu user's JLPT level và learning goals
- **Grammar Extraction**: Tự động extract grammar points từ responses

#### b) Grammar Analysis
- **Text Analysis**: Phân tích văn bản tiếng Nhật
- **JLPT Assessment**: Đánh giá trình độ JLPT
- **Pattern Recognition**: Nhận diện grammar patterns
- **Difficulty Scoring**: Đánh giá độ khó (0-10)

#### c) Translation
- **Bidirectional**: Japanese ↔ Vietnamese
- **Natural Translation**: Dịch tự nhiên, không chỉ literal
- **Pronunciation Guides**: Romaji cho Japanese text

#### d) JLPT Level Prediction
- **Text Analysis**: Phân tích vocabulary, grammar, kanji
- **Level Classification**: N5, N4, N3, N2, N1
- **Automatic Detection**: Tự động detect level của text

#### e) Learning Suggestions
- **Personalized**: Dựa trên user level và weak areas
- **Actionable**: Practical, actionable advice
- **Context-aware**: Phù hợp với learning goals

---

## 🔒 SECURITY & AUTHENTICATION

### 1. Python-jose (JWT) 3.3.0
**Mục đích**: JWT token generation và validation

**Cách sử dụng**:
- Create JWT access tokens
- Verify JWT tokens
- Extract user info từ token

**Vị trí trong code**:
- `backend/app/core/auth.py` - JWT functions

**Ví dụ sử dụng**:
```python
# backend/app/core/auth.py
from jose import JWTError, jwt

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
```

---

### 2. Bcrypt 4.0.1
**Mục đích**: Password hashing

**Cách sử dụng**:
- Hash passwords trước khi lưu database
- Verify passwords khi login
- Salt tự động

**Vị trí trong code**:
- `backend/app/core/auth.py` - Password hashing functions

**Ví dụ sử dụng**:
```python
# backend/app/core/auth.py
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

---

### 3. Email-validator
**Mục đích**: Email validation

**Cách sử dụng**:
- Validate email format
- Used với Pydantic EmailStr

**Vị trí trong code**:
- `backend/app/models/schemas.py` - Email validation trong schemas

---

## 📡 API & COMMUNICATION

### 1. HTTPX 0.25.2
**Mục đích**: Async HTTP client

**Cách sử dụng**:
- Make HTTP requests từ backend
- Call external APIs
- Async/await support

**Vị trí trong code**:
- Có thể sử dụng cho external API calls

---

### 2. Requests 2.31.0
**Mục đích**: Synchronous HTTP client

**Cách sử dụng**:
- Simple HTTP requests
- API calls (nếu không cần async)

**Vị trí trong code**:
- Fallback cho synchronous requests

---

### 3. BeautifulSoup4 4.12.2
**Mục đích**: HTML/XML parsing

**Cách sử dụng**:
- Parse HTML content
- Web scraping (nếu cần)
- Extract data từ HTML

**Vị trí trong code**:
- Có thể sử dụng cho document parsing

---

## 🛠️ DEVELOPMENT TOOLS

### 1. ESLint
**Mục đích**: JavaScript/TypeScript linting

**Cách sử dụng**:
- Code quality checks
- Style enforcement
- Error detection

**Vị trí trong code**:
- `frontend/.eslintrc.cjs` - ESLint configuration
- `npm run lint` - Run linter

---

### 2. TypeScript ESLint
**Mục đích**: TypeScript-specific linting

**Cách sử dụng**:
- Type checking
- TypeScript best practices
- Integration với ESLint

**Vị trí trong code**:
- `frontend/package.json` - Dev dependencies

---

### 3. Autoprefixer & PostCSS
**Mục đích**: CSS processing

**Cách sử dụng**:
- Auto-add vendor prefixes
- CSS transformations
- TailwindCSS integration

**Vị trí trong code**:
- `frontend/postcss.config.js` - PostCSS configuration

---

## 📦 PACKAGE MANAGEMENT

### Frontend: npm
- Package manager: npm (Node Package Manager)
- Lock file: `package-lock.json`
- Scripts: `npm install`, `npm run dev`, `npm run build`

### Backend: pip
- Package manager: pip (Python Package Installer)
- Requirements file: `requirements.txt`
- Virtual environment: `.venv/`
- Commands: `pip install -r requirements.txt`

---

## 🔄 DATA FLOW

### 1. User Request Flow
```
User (Browser)
  ↓
React Component (Frontend)
  ↓
Axios API Call
  ↓
FastAPI Endpoint (Backend)
  ↓
Service Layer (Business Logic)
  ↓
Database/VectorDB/LLM
  ↓
Response
  ↓
React Component Update
```

### 2. Authentication Flow
```
User Login
  ↓
POST /auth/login
  ↓
Verify Password (bcrypt)
  ↓
Generate JWT Token (python-jose)
  ↓
Return Token
  ↓
Store in localStorage (Frontend)
  ↓
Include in Authorization Header (Axios interceptor)
```

### 3. RAG (Retrieval-Augmented Generation) Flow
```
User Question
  ↓
Vector Search (ChromaDB)
  ↓
Retrieve Relevant Documents
  ↓
Build Context
  ↓
LLM Prompt (Ollama/LangChain)
  ↓
Generate Response
  ↓
Return to User
```

---

## 🎯 TÓM TẮT

### Frontend Stack
- **UI Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: React Query
- **Forms**: React Hook Form
- **HTTP Client**: Axios
- **Routing**: React Router
- **Icons**: Lucide React
- **Notifications**: React Hot Toast

### Backend Stack
- **Framework**: FastAPI
- **Server**: Uvicorn
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Database**: PostgreSQL
- **Vector DB**: ChromaDB
- **LLM**: Ollama + LangChain

### Security
- **Authentication**: JWT (python-jose)
- **Password Hashing**: bcrypt
- **CORS**: FastAPI CORS middleware
- **Environment Variables**: python-dotenv

### Development
- **Frontend Linting**: ESLint + TypeScript ESLint
- **CSS Processing**: PostCSS + Autoprefixer
- **Package Managers**: npm (Frontend), pip (Backend)

---

*Tài liệu này được tạo tự động dựa trên codebase hiện tại. Cập nhật lần cuối: 2024*


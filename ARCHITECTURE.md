# 📊 KIẾN TRÚC TỔNG QUAN WEB APPLICATION

## Sơ đồ hệ thống

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React + Vite)                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │
│  │  Login   │ │   Chat   │ │ Grammar  │ │ Library  │ │ Profile  │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘   │
│       └────────────┴────────────┴────────────┴────────────┘         │
│                              ↓ API calls                             │
│                     services/api.ts + auth.tsx                       │
└─────────────────────────────────────────────────────────────────────┘
                               ↓ HTTP/REST
┌─────────────────────────────────────────────────────────────────────┐
│                      BACKEND (FastAPI + Python)                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                         API Routes                            │   │
│  │  /auth  │  /chat  │  /analysis  │  /library                  │   │
│  └────┬────────┬────────────┬─────────────┬─────────────────────┘   │
│       ↓        ↓            ↓             ↓                         │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                        SERVICES                               │   │
│  │  llm_service  │  ollama_service  │  vector_db (ChromaDB)     │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
          ↓                        ↓                    ↓
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │     Ollama      │    │    ChromaDB     │
│   (Database)    │    │   (Local LLM)   │    │  (Vector Store) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 📁 CẤU TRÚC THƯ MỤC

```
AIII/
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── pages/              # Các trang: Login, Chat, Grammar, Library, Profile
│   │   ├── components/         # Components: Layout, LoadingSpinner
│   │   ├── services/           # API calls & Authentication
│   │   └── utils/              # Helper functions
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── api/                # API endpoints: auth, chat, analysis, library
│   │   ├── core/               # Config, Database, Auth
│   │   ├── models/             # Database models & Schemas
│   │   ├── services/           # Business logic: LLM, Ollama, VectorDB
│   │   └── main.py             # Entry point
│   ├── alembic/                # Database migrations
│   └── requirements.txt
│
├── database/                    # SQL init scripts
└── docker-compose.yml          # Docker orchestration
```

---

## 📝 MÔ TẢ THÀNH PHẦN

| Thành phần | Công nghệ | Chức năng |
|------------|-----------|-----------|
| **Frontend** | React + TypeScript + Vite + TailwindCSS | Giao diện người dùng |
| **Backend** | FastAPI (Python) | REST API server |
| **Database** | PostgreSQL + Alembic (migration) | Lưu trữ users, chat history |
| **LLM** | Ollama (local) | AI chatbot, phân tích ngữ pháp |
| **Vector DB** | ChromaDB | Tìm kiếm ngữ nghĩa, RAG |

---

## 🔄 LUỒNG HOẠT ĐỘNG

### 1. Đăng nhập (Authentication)
```
User → Login Page → POST /auth/login → JWT Token → Lưu localStorage
```

### 2. Chat với AI
```
User nhập tin nhắn → POST /chat → llm_service → Ollama LLM → Response → Hiển thị
```

### 3. Tìm kiếm thư viện (Library)
```
User tìm kiếm → GET /library → vector_db (ChromaDB) → Kết quả ngữ nghĩa
```

### 4. Phân tích ngữ pháp (Grammar)
```
User nhập văn bản → POST /analysis → LLM phân tích → Kết quả sửa lỗi
```

---

## 🛠️ CÔNG NGHỆ SỬ DỤNG

### Frontend
- **React 18** - UI Framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Axios** - HTTP client

### Backend
- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **LangChain** - LLM integration
- **ChromaDB** - Vector database

### Infrastructure
- **PostgreSQL** - Main database
- **Ollama** - Local LLM runtime
- **Docker** - Containerization

---

## 🚀 CÁCH CHẠY

```bash
# Backend
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

---

## 📌 API ENDPOINTS

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/auth/login` | Đăng nhập |
| POST | `/auth/register` | Đăng ký |
| POST | `/chat` | Gửi tin nhắn chat |
| GET | `/chat/history` | Lấy lịch sử chat |
| POST | `/analysis` | Phân tích ngữ pháp |
| GET | `/library` | Tìm kiếm thư viện |



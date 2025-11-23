# Script sửa file .env
Write-Host "Đang sửa file .env..." -ForegroundColor Yellow

$envContent = @"
# Backend Environment Variables
DATABASE_URL=postgresql://senpai:senpai123@localhost:5432/senpai_db
SECRET_KEY=your-secret-key-change-in-production-please-use-a-strong-random-key

# LLM Configuration
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma:2b

# OpenAI Configuration (fallback)
OPENAI_API_KEY=your-openai-api-key-here

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma_db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
RATE_LIMIT_PER_MINUTE=60
"@

$envContent | Out-File -FilePath ".env" -Encoding utf8 -NoNewline
Write-Host "✅ Đã sửa file .env" -ForegroundColor Green
Write-Host "Lưu ý: ALLOWED_ORIGINS được định nghĩa trong config.py, không cần trong .env" -ForegroundColor Cyan






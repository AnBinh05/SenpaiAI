# 🆓 SenpaiAI với Ollama - Hướng dẫn chi tiết

## Tại sao sử dụng Ollama?

Ollama cho phép bạn chạy SenpaiAI **hoàn toàn miễn phí** với các model LLM local thay vì phải trả phí cho OpenAI API.

### Lợi ích:
- ✅ **Miễn phí** - Không cần API key
- ✅ **Privacy** - Dữ liệu không rời khỏi máy tính
- ✅ **Offline** - Hoạt động không cần internet
- ✅ **Customizable** - Có thể fine-tune models
- ✅ **Fast** - Chạy local nhanh hơn API calls

## Cài đặt Ollama

### 1. Tải và cài đặt Ollama

**Windows:**
```bash
# Tải từ: https://ollama.ai/download
# Hoặc sử dụng winget
winget install Ollama.Ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**macOS:**
```bash
# Tải từ: https://ollama.ai/download
# Hoặc sử dụng Homebrew
brew install ollama
```

### 2. Khởi động Ollama

```bash
# Khởi động Ollama service
ollama serve
```

### 3. Cài đặt models

```bash
# Model chính cho SenpaiAI (khuyến nghị)
ollama pull gemma:2b

# Model chất lượng cao hơn (cần nhiều RAM)
ollama pull gemma:7b

# Model embedding cho RAG
ollama pull nomic-embed-text

# Model khác có thể dùng
ollama pull llama2:7b
ollama pull mistral:7b
```

## Cấu hình SenpaiAI

### 1. Cập nhật file .env

Trong `backend/.env`:
```env
# LLM Configuration
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=gemma:2b

# OpenAI Configuration (fallback)
OPENAI_API_KEY=your-openai-api-key-here
```

### 2. Chạy SenpaiAI

```bash
# Sử dụng script tự động
./start.sh

# Hoặc chạy thủ công
docker-compose up -d
```

## Models được khuyến nghị

### Gemma 2B (Khuyến nghị)
- **Kích thước**: ~1.6GB
- **RAM cần**: 4GB+
- **Tốc độ**: Rất nhanh
- **Chất lượng**: Tốt cho hầu hết tác vụ
- **Sử dụng**: Phù hợp cho mọi máy tính

### Gemma 7B
- **Kích thước**: ~5GB
- **RAM cần**: 8GB+
- **Tốc độ**: Nhanh
- **Chất lượng**: Rất tốt
- **Sử dụng**: Máy tính có RAM cao

### Nomic Embed Text
- **Kích thước**: ~274MB
- **RAM cần**: 1GB+
- **Sử dụng**: Embedding cho RAG
- **Chất lượng**: Tốt cho semantic search

## Troubleshooting

### Ollama không khởi động
```bash
# Kiểm tra Ollama có chạy không
curl http://localhost:11434/api/tags

# Khởi động lại Ollama
ollama serve
```

### Model không tải được
```bash
# Kiểm tra models đã cài
ollama list

# Tải lại model
ollama pull gemma:2b
```

### SenpaiAI không kết nối được Ollama
```bash
# Kiểm tra Docker network
docker network ls

# Restart services
docker-compose down
docker-compose up -d
```

### Performance chậm
- Giảm kích thước model (dùng gemma:2b thay vì gemma:7b)
- Tăng RAM cho Docker
- Đóng các ứng dụng khác

## So sánh với OpenAI

| Tính năng | Ollama | OpenAI |
|-----------|--------|--------|
| **Chi phí** | Miễn phí | Trả phí theo usage |
| **Privacy** | Local | Cloud |
| **Internet** | Không cần | Cần |
| **Tốc độ** | Nhanh (local) | Phụ thuộc network |
| **Customization** | Cao | Thấp |
| **Setup** | Phức tạp hơn | Đơn giản |

## Tips tối ưu

1. **Chọn model phù hợp**: Gemma 2B cho hầu hết trường hợp
2. **Monitor RAM**: Đảm bảo có đủ RAM cho model
3. **GPU acceleration**: Có thể dùng GPU để tăng tốc
4. **Model caching**: Ollama tự động cache models
5. **Batch processing**: Xử lý nhiều requests cùng lúc

## Kết luận

Ollama là lựa chọn tuyệt vời để chạy SenpaiAI miễn phí với chất lượng tốt. Mặc dù setup phức tạp hơn một chút, nhưng lợi ích về privacy và chi phí rất đáng giá.

🎌 **Chúc bạn học tiếng Nhật vui vẻ với SenpaiAI!**


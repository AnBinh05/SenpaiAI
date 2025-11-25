# 🔧 SỬA LỖI OLLAMA MODEL - "model 'gemma:2b' not found"

## ✅ ĐÃ SỬA

**Vấn đề**: Model `gemma:2b` chưa được cài đặt trong Ollama.

**Giải pháp đã áp dụng**:
- ✅ Cải thiện `OllamaJapaneseLearningService` để tự động tìm model dự phòng
- ✅ Nếu model được cấu hình không tồn tại, sẽ tự động dùng model có sẵn
- ✅ Tạo script `check_ollama_models.py` để kiểm tra và cài đặt models
- ✅ Tạo script `install_ollama_model.bat` để tự động cài đặt models

## 🚀 CÁCH SỬA LỖI

### Cách 1: Cài đặt model `gemma:2b` (Khuyến nghị)

```powershell
# Mở terminal mới và chạy:
ollama pull gemma:2b
```

Sau đó **restart backend**:
```powershell
# Dừng backend (Ctrl+C)
# Chạy lại:
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Cách 2: Sử dụng script tự động

```powershell
cd backend
.\install_ollama_model.bat
```

Script này sẽ:
- Kiểm tra Ollama có chạy không
- Cài đặt `gemma:2b` (model chính)
- Cài đặt `nomic-embed-text` (model embedding cho RAG)

### Cách 3: Sử dụng Python script

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python check_ollama_models.py
```

Script này sẽ:
- Kiểm tra Ollama connection
- Liệt kê các models đã cài
- Hỏi bạn có muốn cài model mặc định không

### Cách 4: Đổi sang model khác

Nếu bạn đã có model khác (ví dụ: `llama2`, `mistral`), cập nhật `backend/.env`:

```env
OLLAMA_MODEL=llama2:7b
```

Hoặc sửa trong `backend/app/core/config.py`:
```python
ollama_model: str = "llama2:7b"  # Thay đổi model ở đây
```

## 📋 CÁC MODEL ĐƯỢC KHUYẾN NGHỊ

| Model | Kích thước | RAM cần | Tốc độ | Chất lượng |
|-------|------------|---------|--------|------------|
| `gemma:2b` | ~1.6GB | 4GB+ | ⚡⚡⚡ Rất nhanh | ✅ Tốt |
| `llama2:7b` | ~4GB | 8GB+ | ⚡⚡ Nhanh | ✅✅ Rất tốt |
| `mistral:7b` | ~4GB | 8GB+ | ⚡⚡ Nhanh | ✅✅ Rất tốt |
| `phi:2` | ~2.7GB | 6GB+ | ⚡⚡⚡ Rất nhanh | ✅✅ Tốt |

## ⚠️ LƯU Ý

1. **Ollama phải chạy**: Đảm bảo Ollama service đang chạy trước khi start backend
   ```powershell
   # Kiểm tra:
   ollama list
   
   # Nếu không chạy, start Ollama:
   ollama serve
   ```

2. **Model tự động fallback**: Code đã được cải thiện để tự động tìm model dự phòng nếu model mặc định không tồn tại.

3. **Restart backend**: Sau khi cài model mới, phải restart backend để áp dụng.

## ✅ KIỂM TRA

Sau khi cài model và restart backend, thử chat lại:
- Gửi message: "xin chào"
- Nếu không còn lỗi "model not found", đã thành công! ✅

## 🔍 TROUBLESHOOTING

### Lỗi: "Ollama is not running"
```powershell
# Start Ollama:
ollama serve

# Hoặc kiểm tra trong Task Manager xem có process "ollama" không
```

### Lỗi: "ollama: command not found"
- Cài đặt Ollama từ: https://ollama.ai/download
- Hoặc thêm Ollama vào PATH

### Model download chậm
- Kiểm tra kết nối internet
- Model `gemma:2b` khoảng 1.6GB, cần thời gian download

### Vẫn lỗi sau khi cài model
1. Kiểm tra model đã cài:
   ```powershell
   ollama list
   ```
2. Restart backend
3. Kiểm tra log backend để xem model nào đang được dùng










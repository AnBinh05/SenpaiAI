# 🔧 HƯỚNG DẪN SỬA LỖI OLLAMA

## ❌ Lỗi gặp phải

```
Ollama API error: llama runner process has terminated: exit status 2
```

## 🔍 Nguyên nhân

Lỗi này xảy ra khi:
1. Ollama service không chạy
2. Model không được cài đặt
3. Ollama process bị crash
4. Thiếu bộ nhớ (RAM)

## ✅ Cách khắc phục

### Bước 1: Kiểm tra Ollama đang chạy

```bash
# Kiểm tra Ollama process
ollama list
```

Nếu lỗi, Ollama chưa chạy.

### Bước 2: Khởi động Ollama

**Windows:**
```bash
# Mở terminal mới và chạy
ollama serve
```

**Hoặc khởi động Ollama service:**
- Tìm "Ollama" trong Start Menu
- Click để mở Ollama Desktop App

**Linux/Mac:**
```bash
# Chạy Ollama trong background
ollama serve &
```

### Bước 3: Kiểm tra Model đã được cài đặt

```bash
# Xem danh sách models
ollama list

# Nếu model gemma:2b chưa có, cài đặt:
ollama pull gemma:2b
```

### Bước 4: Kiểm tra kết nối

```bash
# Test API
curl http://localhost:11434/api/tags
```

Nếu trả về JSON, Ollama đang chạy tốt.

### Bước 5: Restart Backend

Sau khi Ollama chạy, restart backend:

```bash
cd backend
python -m uvicorn app.main:app --reload
```

## 🛠️ Đã sửa trong code

1. ✅ **Thêm retry logic** - Tự động thử lại khi lỗi
2. ✅ **Kiểm tra connection** - Kiểm tra Ollama trước khi gọi API
3. ✅ **Error handling tốt hơn** - Không hiển thị error cho user, dùng fallback
4. ✅ **Kiểm tra model** - Cảnh báo nếu model chưa được cài đặt

## 📝 Lưu ý

- Ollama cần chạy **trước** khi start backend
- Model `gemma:2b` cần ít nhất 4GB RAM
- Nếu thiếu RAM, dùng model nhỏ hơn: `gemma:2b` hoặc `tinyllama`

## 🔄 Nếu vẫn lỗi

1. **Restart Ollama:**
   ```bash
   # Dừng Ollama (Ctrl+C)
   # Khởi động lại
   ollama serve
   ```

2. **Reinstall Model:**
   ```bash
   ollama rm gemma:2b
   ollama pull gemma:2b
   ```

3. **Kiểm tra Port:**
   - Ollama mặc định chạy trên port 11434
   - Đảm bảo không có ứng dụng khác dùng port này

4. **Check Logs:**
   - Xem terminal nơi chạy `ollama serve` để biết lỗi chi tiết

## ✅ Sau khi sửa

1. Grammar Analysis sẽ hoạt động bình thường
2. Translation sẽ hoạt động (nếu chọn "Include Translation")
3. Learning Suggestions sẽ hiển thị

---

**Lưu ý:** Nếu Ollama không thể chạy, bạn có thể chuyển sang OpenAI bằng cách:
1. Thêm `OPENAI_API_KEY` vào `backend/.env`
2. Đổi `LLM_PROVIDER=openai` trong `backend/.env`



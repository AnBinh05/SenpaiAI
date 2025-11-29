# 🔧 HƯỚNG DẪN SỬA LỖI LEARNING LIBRARY

## ❌ Vấn đề
Chức năng "Learning Library" hiển thị "0 documents" và không tìm kiếm được vì:
1. **Database chưa có dữ liệu** - Chưa chạy script populate data
2. **Lỗi logic tìm kiếm** - Không thể extract document ID từ ChromaDB results (đã sửa)

## ✅ Đã sửa
- ✅ Sửa logic extract document ID trong `library.py`
- ✅ Thêm `document_id` vào metadata trong `vector_db.py`

## 🚀 Cách khắc phục

### Bước 1: Populate dữ liệu vào Database

Chạy script để thêm dữ liệu mẫu:

```bash
cd backend
python populate_data.py
```

Script này sẽ:
- Tạo các documents mẫu trong PostgreSQL
- Thêm embeddings vào ChromaDB vector store

### Bước 2: Kiểm tra dữ liệu

Sau khi chạy script, kiểm tra:
- Database có documents: `SELECT COUNT(*) FROM documents;`
- ChromaDB có data: Kiểm tra trong `backend/chroma_db/`

### Bước 3: Restart Backend

```bash
# Dừng backend (Ctrl+C)
# Khởi động lại
python -m uvicorn app.main:app --reload
```

### Bước 4: Kiểm tra Frontend

Refresh trang Library, bạn sẽ thấy:
- ✅ Documents hiển thị
- ✅ Search hoạt động
- ✅ Stats hiển thị đúng

## 📝 Lưu ý

1. **Nếu vẫn không có dữ liệu:**
   - Kiểm tra kết nối database: `backend/test_db_connection.py`
   - Kiểm tra ChromaDB folder: `backend/chroma_db/`

2. **Nếu search không hoạt động:**
   - Kiểm tra console browser (F12) xem có lỗi API không
   - Kiểm tra backend logs
   - Đảm bảo ChromaDB đã có embeddings

3. **Thêm documents mới:**
   - Thêm vào `backend/app/utils/sample_corpus.py`
   - Chạy lại `populate_data.py`

## 🔍 Kiểm tra nhanh

```bash
# Kiểm tra database
cd backend
python -c "from app.core.database import SessionLocal; from app.models.database import Document; db = SessionLocal(); print(f'Documents: {db.query(Document).count()}'); db.close()"

# Kiểm tra ChromaDB
python -c "from app.services.vector_db import chroma_service; print(chroma_service.get_collection_stats())"
```



# Hướng dẫn chạy SenpaiAI

## Cách chạy Backend

### Cách 1: Dùng script (Khuyến nghị)
```bash
cd backend
start.bat
```

### Cách 2: Chạy thủ công
```bash
cd backend
.venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**LƯU Ý:** 
- KHÔNG chạy `python main.py` vì file main.py nằm ở `app/main.py`, không phải ở root
- Phải dùng `uvicorn` để chạy FastAPI server
- Backend sẽ chạy tại: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Cách chạy Frontend

```bash
cd frontend
npm install  # Nếu chưa cài
npm run dev
```

Frontend sẽ chạy tại: http://localhost:5173

## Cách chạy tất cả (Docker)

```bash
docker-compose up
```

## Troubleshooting

### Lỗi: ModuleNotFoundError: No module named 'email_validator'
**Giải pháp:** Đã thêm vào requirements.txt, chạy lại:
```bash
cd backend
.venv\Scripts\activate
pip install email-validator==2.1.0
```

### Lỗi: can't open file 'main.py'
**Giải pháp:** Dùng `uvicorn` thay vì `python main.py`:
```bash
uvicorn app.main:app --reload
```

























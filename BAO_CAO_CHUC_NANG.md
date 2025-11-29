# 📚 BÁO CÁO CHỨC NĂNG - SENPAIAI JAPANESE LEARNING PLATFORM

**Ngày tạo:** 2024  
**Phiên bản:** 1.0.0  
**Nền tảng:** Web Application (React + FastAPI)

---

## 📋 MỤC LỤC

1. [Tổng quan](#tổng-quan)
2. [Trang Đăng nhập/Đăng ký](#1-trang-đăng-nhậpđăng-ký)
3. [Trang Chat](#2-trang-chat)
4. [Trang Grammar Analysis](#3-trang-grammar-analysis)
5. [Trang Learning Library](#4-trang-learning-library)
6. [Trang Profile](#5-trang-profile)
7. [Tổng kết](#tổng-kết)

---

## 🎌 TỔNG QUAN

**SenpaiAI** là một nền tảng học tiếng Nhật toàn diện được hỗ trợ bởi công nghệ AI (LLM + RAG), cung cấp các tính năng:

- 💬 **Chat với AI** - Hỏi đáp tiếng Nhật thông minh
- 📖 **Phân tích ngữ pháp** - Giải thích chi tiết ngữ pháp
- 📚 **Thư viện học tập** - Tài liệu và tìm kiếm ngữ nghĩa
- 👤 **Quản lý Profile** - Theo dõi tiến độ học tập
- 🔐 **Xác thực bảo mật** - JWT Authentication

**Công nghệ sử dụng:**
- Frontend: React + TypeScript + Vite + TailwindCSS
- Backend: FastAPI (Python) + LangChain
- Database: PostgreSQL
- Vector DB: ChromaDB
- LLM: Ollama (Local) hoặc OpenAI

---

## 1. TRANG ĐĂNG NHẬP/ĐĂNG KÝ

### 📸 Ảnh chụp màn hình

> **Hướng dẫn chụp ảnh:**
> 1. Mở trình duyệt và truy cập `http://localhost:5173/login`
> 2. Chụp toàn bộ màn hình trang Login
> 3. Chụp thêm khi chuyển sang tab Register
> 4. Lưu ảnh với tên: `01-login-page.png` và `01-register-page.png`

```
[Chèn ảnh: 01-login-page.png]
```

**Mô tả:** Trang đăng nhập với form email và password, có nút chuyển sang đăng ký.

```
[Chèn ảnh: 01-register-page.png]
```

**Mô tả:** Trang đăng ký với form đầy đủ: email, username, password, và confirm password.

### ✨ Chức năng chi tiết

#### 1.1. Đăng nhập (Login)
- **Vị trí:** Tab "Login" (mặc định)
- **Các trường:**
  - Email: Input field với validation
  - Password: Input field với type="password"
- **Nút:** "Sign In" - Gửi request đến `/auth/login`
- **Xử lý:**
  - Validate email format
  - Kiểm tra password
  - Lưu JWT token vào localStorage
  - Redirect đến trang Chat sau khi đăng nhập thành công
- **Error handling:**
  - Hiển thị toast notification khi sai email/password
  - Hiển thị lỗi validation

#### 1.2. Đăng ký (Register)
- **Vị trí:** Tab "Register"
- **Các trường:**
  - Email: Input với validation email
  - Username: Input với validation (3-20 ký tự, chỉ chữ, số, underscore)
  - Password: Input với validation (tối thiểu 6 ký tự)
  - Confirm Password: Input phải khớp với password
- **Nút:** "Sign Up" - Gửi request đến `/auth/register`
- **Xử lý:**
  - Validate tất cả fields
  - Kiểm tra email/username đã tồn tại chưa
  - Hash password trước khi lưu
  - Tự động đăng nhập sau khi đăng ký thành công
- **Error handling:**
  - Hiển thị lỗi nếu email/username đã tồn tại
  - Hiển thị lỗi validation

### 🔗 API Endpoints

- `POST /auth/login` - Đăng nhập
- `POST /auth/register` - Đăng ký

---

## 2. TRANG CHAT

### 📸 Ảnh chụp màn hình

> **Hướng dẫn chụp ảnh:**
> 1. Sau khi đăng nhập, chụp toàn bộ màn hình trang Chat
> 2. Chụp khi đang gửi tin nhắn (có loading spinner)
> 3. Chụp khi có kết quả trả về từ AI
> 4. Chụp sidebar với chat history
> 5. Lưu ảnh: `02-chat-main.png`, `02-chat-loading.png`, `02-chat-response.png`, `02-chat-history.png`

```
[Chèn ảnh: 02-chat-main.png]
```

**Mô tả:** Giao diện chat chính với input box ở dưới, danh sách tin nhắn ở giữa.

```
[Chèn ảnh: 02-chat-response.png]
```

**Mô tả:** Ví dụ một câu hỏi và câu trả lời từ AI với format đẹp.

### ✨ Chức năng chi tiết

#### 2.1. Gửi tin nhắn
- **Input:** Textarea ở cuối trang
- **Nút:** "Send" hoặc Enter để gửi
- **Xử lý:**
  - Gửi request đến `/chat/message`
  - Hiển thị loading spinner khi đang xử lý
  - Hiển thị tin nhắn của user ngay lập tức
  - Hiển thị response từ AI khi có kết quả
- **Tính năng RAG:**
  - Tự động tìm kiếm context từ ChromaDB
  - Sử dụng context để tạo câu trả lời chính xác hơn
  - Hiển thị sources nếu có

#### 2.2. Chat History
- **Vị trí:** Sidebar bên trái hoặc danh sách ở giữa
- **Chức năng:**
  - Hiển thị tất cả cuộc trò chuyện trước đó
  - Click vào để xem lại
  - Tìm kiếm trong lịch sử
  - Xóa từng tin nhắn hoặc xóa toàn bộ
- **Thông tin hiển thị:**
  - Question và Answer
  - Thời gian gửi
  - JLPT level (nếu có)
  - Grammar points (nếu có)

#### 2.3. Tính năng bổ sung
- **Translation:** Có thể yêu cầu dịch câu trả lời sang tiếng Việt
- **JLPT Level:** Tự động dự đoán độ khó của câu hỏi/trả lời
- **Grammar Points:** Tự động trích xuất các điểm ngữ pháp
- **Sources:** Hiển thị nguồn tài liệu được sử dụng (RAG)

### 🔗 API Endpoints

- `POST /chat/message` - Gửi tin nhắn
- `GET /chat/history` - Lấy lịch sử chat
- `GET /chat/search` - Tìm kiếm trong lịch sử
- `DELETE /chat/history/{id}` - Xóa một tin nhắn
- `DELETE /chat/history` - Xóa toàn bộ lịch sử

---

## 3. TRANG GRAMMAR ANALYSIS

### 📸 Ảnh chụp màn hình

> **Hướng dẫn chụp ảnh:**
> 1. Chụp trang Grammar Analysis khi chưa nhập text
> 2. Chụp khi đang phân tích (có loading)
> 3. Chụp kết quả phân tích với các grammar points được highlight
> 4. Chụp phần translation nếu có
> 5. Lưu ảnh: `03-grammar-empty.png`, `03-grammar-loading.png`, `03-grammar-result.png`

```
[Chèn ảnh: 03-grammar-empty.png]
```

**Mô tả:** Trang Grammar với textarea trống, có checkbox "Include Translation".

```
[Chèn ảnh: 03-grammar-result.png]
```

**Mô tả:** Kết quả phân tích với các grammar points được liệt kê, JLPT level, và translation.

### ✨ Chức năng chi tiết

#### 3.1. Phân tích ngữ pháp
- **Input:** Textarea để nhập văn bản tiếng Nhật
- **Options:**
  - Checkbox "Include Translation" - Dịch sang tiếng Việt
- **Nút:** "Analyze Grammar" - Gửi request đến `/analysis/grammar`
- **Kết quả hiển thị:**
  - **JLPT Level:** Dự đoán trình độ (N5-N1)
  - **Grammar Points:** Danh sách các điểm ngữ pháp được tìm thấy
    - Tên điểm ngữ pháp
    - Ý nghĩa
    - Ví dụ sử dụng
  - **Translation:** Bản dịch tiếng Việt (nếu chọn)
  - **Difficulty Score:** Điểm độ khó (0-10)
  - **Suggestions:** Gợi ý học tập

#### 3.2. Tính năng bổ sung
- **JLPT Level Prediction:** Tự động đánh giá độ khó
- **Grammar Extraction:** Tự động nhận diện các điểm ngữ pháp
- **Translation:** Dịch văn bản sang tiếng Việt
- **Learning Suggestions:** Đưa ra gợi ý học tập dựa trên kết quả

### 🔗 API Endpoints

- `POST /analysis/grammar` - Phân tích ngữ pháp
- `POST /analysis/translate` - Dịch thuật
- `POST /analysis/jlpt-level` - Dự đoán JLPT level

---

## 4. TRANG LEARNING LIBRARY

### 📸 Ảnh chụp màn hình

> **Hướng dẫn chụp ảnh:**
> 1. Chụp trang Library với danh sách documents
> 2. Chụp phần Search với các filter
> 3. Chụp kết quả tìm kiếm
> 4. Chụp form "Add New Document"
> 5. Chụp một document card chi tiết
> 6. Lưu ảnh: `04-library-main.png`, `04-library-search.png`, `04-library-add-form.png`, `04-library-document.png`

```
[Chèn ảnh: 04-library-main.png]
```

**Mô tả:** Trang Library với stats cards ở trên, search form, và grid các documents.

```
[Chèn ảnh: 04-library-search.png]
```

**Mô tả:** Kết quả tìm kiếm với semantic search.

```
[Chèn ảnh: 04-library-add-form.png]
```

**Mô tả:** Form thêm document mới với các trường: title, type, JLPT level, tags, content.

### ✨ Chức năng chi tiết

#### 4.1. Statistics Dashboard
- **Vị trí:** Phần đầu trang
- **Hiển thị:**
  - Total Documents: Tổng số tài liệu
  - Document Types: Số loại tài liệu khác nhau
  - JLPT Levels: Số level có tài liệu
  - Vector Chunks: Số chunks trong ChromaDB

#### 4.2. Tìm kiếm Documents
- **Search Form:**
  - **Query:** Input để nhập từ khóa tìm kiếm
  - **Document Type:** Dropdown filter (All Types, vocabulary, grammar, lesson, culture, example)
  - **JLPT Level:** Dropdown filter (All Levels, N5-N1)
  - **Nút Search:** Thực hiện semantic search
- **Tính năng:**
  - Semantic search sử dụng ChromaDB
  - Tìm kiếm theo ngữ nghĩa, không chỉ từ khóa
  - Filter theo type và level
  - Hiển thị kết quả với relevance score

#### 4.3. Danh sách Documents
- **Layout:** Grid layout với cards
- **Mỗi Document Card hiển thị:**
  - Title: Tiêu đề tài liệu
  - Document Type: Loại (vocabulary, grammar, etc.)
  - JLPT Level: Badge màu theo level
  - Content Preview: 150 ký tự đầu
  - Tags: Các tags liên quan
  - Created Date: Ngày tạo
  - Source URL: Link tham khảo (nếu có)
- **Tính năng:**
  - Click để xem chi tiết
  - External link icon nếu có source URL
  - Hover effect

#### 4.4. Thêm Document mới
- **Nút:** "Add New Document" ở đầu trang
- **Form fields:**
  - **Title:** *Bắt buộc - Tiêu đề document
  - **Document Type:** *Bắt buộc - Dropdown (vocabulary, grammar, lesson, culture, example)
  - **JLPT Level:** Tùy chọn - Dropdown (N5-N1)
  - **Tags:** Tùy chọn - Comma-separated
  - **Source URL:** Tùy chọn - Link tham khảo
  - **Content:** *Bắt buộc - Textarea với nội dung
- **Xử lý:**
  - Validate tất cả fields bắt buộc
  - Lưu vào PostgreSQL
  - Tự động thêm vào ChromaDB vector store
  - Refresh danh sách sau khi thêm
- **Error handling:**
  - Hiển thị lỗi validation
  - Toast notification khi thành công/thất bại

#### 4.5. Categories & Filters
- **Get Categories:** API trả về danh sách document types và JLPT levels có sẵn
- **Dynamic Filters:** Dropdown được populate từ database

### 🔗 API Endpoints

- `GET /library/documents` - Lấy danh sách documents
- `GET /library/documents/{id}` - Lấy document theo ID
- `POST /library/documents` - Tạo document mới
- `PUT /library/documents/{id}` - Cập nhật document
- `DELETE /library/documents/{id}` - Xóa document
- `POST /library/search` - Tìm kiếm semantic
- `GET /library/categories` - Lấy categories
- `GET /library/stats` - Lấy statistics

---

## 5. TRANG PROFILE

### 📸 Ảnh chụp màn hình

> **Hướng dẫn chụp ảnh:**
> 1. Chụp trang Profile với form cập nhật thông tin
> 2. Chụp phần Learning Progress với stats
> 3. Chụp phần Quick Actions
> 4. Chụp khi export data (file HTML được tải xuống)
> 5. Chụp confirmation dialog khi reset progress hoặc delete account
> 6. Lưu ảnh: `05-profile-main.png`, `05-profile-stats.png`, `05-profile-actions.png`, `05-profile-export.png`

```
[Chèn ảnh: 05-profile-main.png]
```

**Mô tả:** Trang Profile với form bên trái và stats/actions bên phải.

```
[Chèn ảnh: 05-profile-stats.png]
```

**Mô tả:** Phần Learning Progress với các icon và thông tin.

```
[Chèn ảnh: 05-profile-actions.png]
```

**Mô tả:** Phần Quick Actions với 3 nút: Export, Reset, Delete.

### ✨ Chức năng chi tiết

#### 5.1. Account Information Form
- **Vị trí:** Cột trái (2/3 width)
- **Các trường:**
  - **Email:** Read-only, không thể thay đổi
  - **Username:** *Bắt buộc - Input với validation
    - Tối thiểu 3 ký tự
    - Tối đa 20 ký tự
    - Chỉ chữ, số, underscore
  - **Current JLPT Level:** *Bắt buộc - Dropdown (N5-N1)
  - **Learning Goals:** Array of strings
    - Input để thêm goal mới
    - Hiển thị danh sách goals hiện tại
    - Nút "×" để xóa từng goal
- **Nút:** "Save Changes" - Gửi request đến `/auth/me` (PUT)
- **Xử lý:**
  - Validate tất cả fields
  - Kiểm tra username đã tồn tại chưa
  - Cập nhật database
  - Refresh user data trong AuthContext
  - Toast notification thành công/thất bại

#### 5.2. Account Information Card
- **Vị trí:** Cột phải (1/3 width)
- **Hiển thị:**
  - Avatar: Chữ cái đầu của username
  - Username và Email
  - Member since: Ngày đăng ký
  - Current Level: JLPT level hiện tại
  - Learning Goals: Số lượng goals

#### 5.3. Learning Progress Card
- **Vị trí:** Cột phải, dưới Account Info
- **Hiển thị:**
  - **JLPT Level:** Icon trophy + level + mô tả
  - **Learning Goals:** Icon target + số lượng goals
  - **Chat Sessions:** Icon message + mô tả
  - **Study Materials:** Icon book + mô tả

#### 5.4. Quick Actions
- **Vị trí:** Cột phải, dưới Learning Progress
- **Các actions:**

##### 5.4.1. Export Learning Data
- **Nút:** "Export Learning Data"
- **Chức năng:**
  - Gọi API `/auth/me/export`
  - Tạo file HTML report đẹp
  - Tự động download file: `senpai-ai-report-YYYY-MM-DD.html`
- **Nội dung file HTML:**
  - Header với gradient
  - Profile Information section
  - Statistics cards
  - Chat History với formatting đẹp
  - Learning Sessions table
  - Styling đẹp, responsive
- **Format:** HTML file có thể mở bằng browser

##### 5.4.2. Reset Progress
- **Nút:** "Reset Progress"
- **Chức năng:**
  - Hiển thị confirmation dialog
  - Gọi API `/auth/me/reset-progress` (POST)
  - Xóa toàn bộ chat history
  - Xóa toàn bộ learning sessions
  - Refresh data sau khi reset
- **Warning:** Có confirmation để tránh xóa nhầm

##### 5.4.3. Delete Account
- **Nút:** "Delete Account" (màu đỏ)
- **Chức năng:**
  - Hiển thị 2 lần confirmation (double confirm)
  - Gọi API `/auth/me` (DELETE)
  - Xóa toàn bộ dữ liệu user
  - Logout và redirect về login
- **Warning:** Có double confirmation, action không thể hoàn tác

### 🔗 API Endpoints

- `GET /auth/me` - Lấy thông tin user hiện tại
- `PUT /auth/me` - Cập nhật thông tin user
- `GET /auth/me/export` - Export learning data
- `POST /auth/me/reset-progress` - Reset progress
- `DELETE /auth/me` - Xóa account

---

## 📊 TỔNG KẾT

### 📈 Thống kê chức năng

| Trang | Số lượng chức năng chính | API Endpoints |
|-------|-------------------------|---------------|
| Login/Register | 2 | 2 |
| Chat | 5+ | 5 |
| Grammar | 3 | 3 |
| Library | 6+ | 8 |
| Profile | 6+ | 5 |
| **TỔNG** | **22+** | **23** |

### 🎯 Tính năng nổi bật

1. **RAG (Retrieval-Augmented Generation)**
   - Semantic search trong ChromaDB
   - Context-aware responses
   - Source attribution

2. **AI-Powered Analysis**
   - Grammar extraction
   - JLPT level prediction
   - Translation capabilities

3. **User Management**
   - JWT authentication
   - Profile customization
   - Learning goals tracking

4. **Data Management**
   - Document CRUD operations
   - Export functionality
   - Progress tracking

### 🔐 Bảo mật

- JWT token-based authentication
- Password hashing với bcrypt
- Protected routes
- Input validation
- SQL injection prevention (SQLAlchemy ORM)

### 📱 Responsive Design

- Mobile-friendly layout
- TailwindCSS responsive utilities
- Adaptive components
- Touch-friendly buttons

### 🚀 Performance

- Fast API responses (< 3s)
- Optimized database queries
- Efficient vector search
- Client-side caching (React Query)

---

## 📝 HƯỚNG DẪN CHỤP ẢNH

### Công cụ cần thiết
- Trình duyệt (Chrome, Firefox, Edge)
- Công cụ chụp màn hình (Snipping Tool, ShareX, hoặc Print Screen)
- Ứng dụng đang chạy (Frontend + Backend)

### Quy trình chụp ảnh

1. **Khởi động ứng dụng:**
   ```bash
   # Backend
   cd backend
   python -m uvicorn app.main:app --reload
   
   # Frontend
   cd frontend
   npm run dev
   ```

2. **Chuẩn bị dữ liệu:**
   - Đăng ký/đăng nhập với tài khoản test
   - Tạo một số chat messages
   - Thêm một số documents vào library
   - Cập nhật profile

3. **Chụp ảnh từng trang:**
   - Mở từng trang một
   - Chụp toàn bộ màn hình
   - Chụp các trạng thái khác nhau (empty, loading, có data)
   - Chụp các dialog/confirmation

4. **Đặt tên file:**
   - Format: `[số]-[tên-trang]-[mô-tả].png`
   - Ví dụ: `01-login-page.png`, `02-chat-response.png`

5. **Chèn ảnh vào file markdown:**
   - Sử dụng cú pháp: `![Mô tả](đường-dẫn-ảnh.png)`
   - Hoặc: `<img src="đường-dẫn-ảnh.png" alt="Mô tả" width="800">`

### Lưu ý
- Chụp ở độ phân giải cao (ít nhất 1920x1080)
- Đảm bảo dữ liệu hiển thị đầy đủ
- Chụp cả trạng thái lỗi nếu có
- Chụp cả mobile view nếu responsive

---

## 📞 LIÊN HỆ & HỖ TRỢ

Nếu có thắc mắc về các chức năng, vui lòng:
- Xem API documentation tại: `http://localhost:8000/docs`
- Kiểm tra code trong thư mục `frontend/src/pages/`
- Xem backend API trong `backend/app/api/`

---

**Tài liệu này được tạo tự động bởi SenpaiAI Documentation Generator**  
**Cập nhật lần cuối:** 2024


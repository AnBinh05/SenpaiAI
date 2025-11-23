# SenpaiAI Frontend

Frontend application cho SenpaiAI - Japanese Learning Assistant được xây dựng với React, TypeScript, và Vite.

## Yêu cầu hệ thống

- **Node.js**: phiên bản 16.x trở lên
- **npm** hoặc **yarn** hoặc **pnpm**
- Backend API đang chạy tại `http://localhost:8000` (hoặc URL khác nếu cấu hình)

## Cài đặt

### 1. Cài đặt dependencies

```bash
npm install
```

hoặc nếu sử dụng yarn:

```bash
yarn install
```

hoặc nếu sử dụng pnpm:

```bash
pnpm install
```

### 2. Cấu hình biến môi trường

Tạo file `.env` từ file mẫu:

```bash
# Windows (PowerShell)
Copy-Item env.example .env

# Windows (CMD)
copy env.example .env

# Linux/Mac
cp env.example .env
```

Sau đó chỉnh sửa file `.env` nếu cần:

```env
VITE_API_BASE_URL=http://localhost:8000
```

**Lưu ý**: Nếu backend API chạy ở port khác hoặc URL khác, hãy cập nhật `VITE_API_BASE_URL` trong file `.env`.

## Chạy ứng dụng

### Chế độ Development

Chạy ứng dụng ở chế độ development với hot-reload:

```bash
npm run dev
```

Ứng dụng sẽ chạy tại: **http://localhost:3000**

### Build cho Production

Build ứng dụng để deploy:

```bash
npm run build
```

File build sẽ được tạo trong thư mục `dist/`.

### Preview Production Build

Xem trước bản build production:

```bash
npm run preview
```

### Lint Code

Chạy ESLint để kiểm tra lỗi code:

```bash
npm run lint
```

## Cấu trúc thư mục

```
frontend/
├── src/
│   ├── components/       # Các component tái sử dụng
│   │   ├── Layout.tsx
│   │   └── LoadingSpinner.tsx
│   ├── pages/           # Các trang chính
│   │   ├── Chat.tsx
│   │   ├── Grammar.tsx
│   │   ├── Library.tsx
│   │   ├── Login.tsx
│   │   └── Profile.tsx
│   ├── services/        # API services và authentication
│   │   ├── api.ts
│   │   └── auth.tsx
│   ├── utils/           # Utility functions
│   │   └── helpers.ts
│   ├── App.tsx          # Component chính
│   ├── main.tsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static files
├── index.html           # HTML template
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Tính năng chính

- 🔐 **Authentication**: Đăng nhập/Đăng ký
- 💬 **Chat với AI**: Hỏi đáp về tiếng Nhật
- 📚 **Phân tích ngữ pháp**: Phân tích văn bản tiếng Nhật
- 📖 **Thư viện học tập**: Tìm kiếm và duyệt tài liệu học tập
- 👤 **Hồ sơ người dùng**: Quản lý thông tin và mục tiêu học tập

## Công nghệ sử dụng

- **React 18**: UI framework
- **TypeScript**: Type safety
- **Vite**: Build tool và dev server
- **React Router**: Routing
- **React Query**: Data fetching và caching
- **React Hook Form**: Form handling
- **Axios**: HTTP client
- **Tailwind CSS**: Styling
- **Lucide React**: Icons
- **React Hot Toast**: Notifications

## Troubleshooting

### Lỗi kết nối API

Nếu gặp lỗi kết nối với backend API:

1. Kiểm tra backend API đang chạy tại URL trong file `.env`
2. Kiểm tra CORS settings trên backend
3. Kiểm tra network tab trong browser DevTools

### Lỗi port đã được sử dụng

Nếu port 3000 đã được sử dụng, Vite sẽ tự động chọn port khác. Hoặc bạn có thể chỉ định port trong `vite.config.ts`:

```typescript
server: {
  port: 3001, // Thay đổi port ở đây
}
```

### Lỗi dependencies

Nếu gặp lỗi khi cài đặt dependencies:

```bash
# Xóa node_modules và package-lock.json
rm -rf node_modules package-lock.json

# Cài đặt lại
npm install
```

## Scripts có sẵn

- `npm run dev`: Chạy development server
- `npm run build`: Build cho production
- `npm run preview`: Preview production build
- `npm run lint`: Chạy ESLint

## Liên hệ

Nếu có vấn đề hoặc câu hỏi, vui lòng tạo issue trên repository.


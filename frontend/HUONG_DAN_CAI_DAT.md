# Hướng dẫn cài đặt SenpaiAI Frontend

## ⚠️ Lưu ý: Node.js chưa được cài đặt

Bạn cần cài đặt Node.js trước khi có thể chạy project này.

## Cách 1: Cài đặt tự động (Khuyến nghị)

### Sử dụng script tự động:

**PowerShell:**
```powershell
.\install.ps1
```

**Command Prompt:**
```cmd
install.bat
```

Script sẽ tự động:
- Kiểm tra Node.js đã cài đặt chưa
- Thử cài đặt Node.js bằng winget (nếu có)
- Cài đặt tất cả dependencies

## Cách 2: Cài đặt thủ công Node.js

### Bước 1: Tải Node.js

1. Truy cập: **https://nodejs.org/**
2. Tải phiên bản **LTS (Long Term Support)** - khuyến nghị
3. Chạy file `.msi` đã tải về
4. Làm theo hướng dẫn cài đặt (Next, Next, Install...)
5. **Khởi động lại** PowerShell/Command Prompt sau khi cài đặt

### Bước 2: Kiểm tra cài đặt

Mở PowerShell hoặc Command Prompt mới và chạy:

```bash
node --version
npm --version
```

Nếu hiển thị số phiên bản, bạn đã cài đặt thành công!

### Bước 3: Cài đặt dependencies

```bash
npm install
```

## Cách 3: Sử dụng winget (Windows Package Manager)

Nếu bạn đã có Windows Package Manager:

```bash
winget install OpenJS.NodeJS.LTS
```

Sau đó khởi động lại terminal và chạy:

```bash
npm install
```

## Cách 4: Sử dụng Chocolatey

Nếu bạn đã cài Chocolatey:

```bash
choco install nodejs-lts -y
```

Sau đó khởi động lại terminal và chạy:

```bash
npm install
```

## Sau khi cài đặt Node.js

1. **Tạo file .env:**
   ```bash
   # PowerShell
   Copy-Item env.example .env
   
   # Command Prompt
   copy env.example .env
   ```

2. **Chạy ứng dụng:**
   ```bash
   npm run dev
   ```

3. Mở trình duyệt tại: **http://localhost:3000**

## Yêu cầu hệ thống

- **Windows 10/11**
- **Node.js 16.x trở lên** (npm đi kèm)
- **Backend API** đang chạy tại `http://localhost:8000`

## Troubleshooting

### Lỗi: "npm is not recognized"

- Đảm bảo đã cài đặt Node.js
- Khởi động lại terminal sau khi cài đặt
- Kiểm tra PATH environment variable có chứa Node.js không

### Lỗi: "Permission denied"

- Chạy terminal với quyền Administrator
- Hoặc sử dụng `npm install --legacy-peer-deps`

### Lỗi kết nối khi cài đặt

- Kiểm tra kết nối internet
- Thử sử dụng VPN nếu cần
- Hoặc cấu hình npm registry: `npm config set registry https://registry.npmjs.org/`

## Liên hệ

Nếu gặp vấn đề, vui lòng tạo issue trên repository.


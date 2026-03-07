# 🔧 WSL UPDATE IN PROGRESS

## ✅ Bạn Đang Làm Đúng!

Docker cần WSL2 để chạy. Bạn đã chạy `wsl --update` - tuyệt vời!

---

## 📋 CHECKLIST - Làm Theo Thứ Tự:

### ☑️ Bước 1: Đợi WSL Update Xong
**Screenshot cho thấy đang "Installing: Windows Subsystem for Linux"**

Đợi trong Command Prompt window cho đến khi thấy:
```
The requested operation is successful.
Changes will not be effective until the system is rebooted.
```

### ☐ Bước 2: Restart Máy (BẮT BUỘC!)

Sau khi WSL update xong, **phải restart máy**:

**Option 1:** Nhấn `Windows + R`, gõ:
```
shutdown /r /t 0
```

**Option 2:** Start Menu → Power → Restart

### ☐ Bước 3: Sau Khi Restart

**3.1. Mở Docker Desktop:**
- Start Menu → tìm "Docker Desktop"
- Click để mở
- **ĐỢI** Docker khởi động hoàn toàn (2-3 phút)
- Icon Docker ở system tray (góc phải taskbar) phải màu **XANH** (không phải đỏ/vàng)

**3.2. Kiểm tra Docker:**

Mở PowerShell và chạy:
```powershell
docker info
```

Nếu thấy thông tin Docker (không có lỗi) → OK! Tiếp tục bước 4.

### ☐ Bước 4: Start MongoDB + Qdrant

Chạy script tự động:
```bash
start-databases.bat
```

Script này sẽ:
- ✅ Clean old containers
- ✅ Start MongoDB (port 27017)
- ✅ Start Qdrant (port 6333)
- ✅ Verify connections
- ✅ Test ports

### ☐ Bước 5: Setup API Key

Vào `apps\backend\.env` và thêm:
```env
GEMINI_API_KEY=your_key_here
```

**Get Gemini key (FREE):** https://ai.google.dev/

### ☐ Bước 6: Chạy Backend

```bash
start-backend.bat
```

### ☐ Bước 7: Test

Mở browser: http://localhost:8000/docs

---

## ❌ Nếu Gặp Lỗi

### Docker Desktop không mở được sau restart

**Fix:**
1. Uninstall Docker Desktop
2. Download phiên bản mới: https://www.docker.com/products/docker-desktop/
3. Cài lại
4. Restart máy

### Docker báo "WSL 2 installation is incomplete"

**Fix:**
```bash
# Mở PowerShell as Administrator
wsl --install
wsl --set-default-version 2

# Restart máy
shutdown /r /t 0
```

### MongoDB/Qdrant không start được

**Fix:**
```bash
# Check Docker đang chạy
docker info

# Remove và tạo lại
docker stop mongodb qdrant
docker rm mongodb qdrant
start-databases.bat
```

---

## 📞 Quick Commands

### Check Docker status
```bash
docker info
docker ps
```

### Check containers
```bash
docker ps -a
```

### Check logs
```bash
docker logs mongodb
docker logs qdrant
```

### Stop databases
```bash
docker stop mongodb qdrant
```

### Start databases
```bash
docker start mongodb qdrant
```

### Remove everything và start lại
```bash
docker stop mongodb qdrant
docker rm mongodb qdrant
start-databases.bat
```

---

## 🎯 TÓM TẮT

**HIỆN TẠI:**
1. ✅ WSL đang update (đúng rồi!)
2. ⏳ Đợi update xong
3. 🔄 Restart máy (BẮT BUỘC)
4. 🐳 Mở Docker Desktop
5. ▶️ Chạy `start-databases.bat`
6. 🚀 Chạy `start-backend.bat`

**SAU KHI RESTART, CHẠY:**
```bash
start-databases.bat
```

---

## ⏰ Timeline

- **Bây giờ:** WSL đang update (~5-10 phút)
- **Sau update:** Restart máy (2 phút)
- **Sau restart:** Mở Docker Desktop (2-3 phút)
- **Setup databases:** Chạy `start-databases.bat` (30 giây)
- **Setup API key:** Edit `.env` (1 phút)
- **Start backend:** Chạy `start-backend.bat` (10 giây)
- **DONE!** 🎉

**TỔNG: ~15-20 phút từ bây giờ**

---

**🔴 QUAN TRỌNG: Phải restart máy sau khi WSL update xong!**

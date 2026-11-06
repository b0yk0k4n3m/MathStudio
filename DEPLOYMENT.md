# 🚀 Hướng Dẫn & Các Nguyên Tắc Triển Khai (Deployment) Math Studio

Tài liệu này cung cấp toàn bộ các nguyên tắc kiến trúc, quy chuẩn vận hành và các phương án triển khai (**Deployment**) ứng dụng **Math Studio** (Hệ thống soạn thảo & thẩm định đề toán THPT 2026) từ môi trường cục bộ, mạng nội bộ (LAN) cho đến môi trường Production (Docker, Linux VPS, Windows Server, Cloud PaaS).

---

## 📑 Mục lục

1. [Các Nguyên tắc Cốt lõi khi Deploy](#1-các-nguyên-tắc-cốt-lõi-khi-deploy)
2. [Bảng Cấu hình Biến Môi trường (.env)](#2-bảng-cấu-hình-biến-môi-trường-env)
3. [Phương án 1: Triển khai Cục bộ & Mạng nội bộ (LAN)](#phương-án-1-triển-khai-cục-bộ--mạng-nội-bộ-lan)
4. [Phương án 2: Triển khai bằng Docker & Docker Compose (Khuyến nghị)](#phương-án-2-triển-khai-bằng-docker--docker-compose-khuyến-nghị)
5. [Phương án 3: Triển khai Máy chủ Linux VPS (Ubuntu/Debian) với Nginx & Systemd](#phương-án-3-triển-khai-máy-chủ-linux-vps-ubuntudebian-với-nginx--systemd)
6. [Phương án 4: Triển khai Windows Server dạng Windows Service (NSSM)](#phương-án-4-triển-khai-windows-server-dạng-windows-service-nssm)
7. [Phương án 5: Triển khai Cloud PaaS (Render, Railway, Fly.io)](#phương-án-5-triển-khai-cloud-paas-render-railway-flyio)
8. [Quy trình Sao lưu (Backup) & Phục hồi Dữ liệu](#8-quy-trình-sao-lưu-backup--phục-hồi-dữ-liệu)
9. [Xử lý Sự cố Thường gặp (Troubleshooting)](#9-xử-lý-sự-cố-thường-gặp-troubleshooting)

---

## 1. Các Nguyên tắc Cốt lõi khi Deploy

Trước khi đưa ứng dụng vào vận hành thực tế, đội ngũ kỹ thuật và quản trị viên bắt buộc phải nắm vững các nguyên tắc sau:

### 1.1. Nguyên tắc Xử lý WebSocket & Reverse Proxy
- **Bản chất công nghệ:** Ứng dụng xây dựng trên nền tảng **NiceGUI** (chạy lõi **FastAPI** và máy chủ **Uvicorn**). Giao diện người dùng giao tiếp với server theo cơ chế hai chiều thời gian thực thông qua **WebSocket** (Socket.IO).
- **Yêu cầu Reverse Proxy (Nginx, Caddy, Cloudflare, Traefik):** Bắt buộc phải cấu hình chuyển tiếp header `Upgrade` và `Connection "upgrade"`. Nếu thiếu cấu hình này, giao diện web sẽ liên tục báo lỗi mất kết nối ("Connection lost. Trying to reconnect...").
- **WebSocket Timeout:** Thiết lập thời gian chờ kết nối (`proxy_read_timeout`) từ 3600 giây trở lên để tránh việc ngắt phiên đột ngột khi người dùng đang suy nghĩ hoặc soạn thảo đề.

### 1.2. Nguyên tắc Bền vững Dữ liệu (Stateful Persistence)
- Ứng dụng lưu trữ dữ liệu trực tiếp trong hệ thống tệp tin:
  - `output/*.md`: Các bản đề thi hoàn chỉnh.
  - `output/*.docx`: Các file Word đề thi và đáp án.
  - `output/images/`: Toàn bộ hình ảnh đồ thị và hình học không gian do Matplotlib sinh ra.
  - `output/exams_index.json`: Cơ sở dữ liệu danh mục đề thi.
  - `output/matrix_templates.json`: Kho ma trận mẫu đề thi.
  - `input/`: Các đề nguồn và hình ảnh bản vẽ gốc do người dùng tải lên.
- **Nguyên tắc:** Khi deploy bằng Docker hoặc môi trường Ephemeral (PaaS), **bắt buộc phải gắn Persistent Volume** vào 2 thư mục `/app/input` và `/app/output`. Tuyệt đối không để dữ liệu nằm trong tầng tạm thời của container.

### 1.3. Nguyên tắc Chế độ Chạy Không Đầu (Headless Mode)
- Ở chế độ phát triển trên máy cá nhân, cờ `show=True` sẽ tự động mở trình duyệt web.
- Khi triển khai lên Server / Docker / Service chạy ngầm, **bắt buộc đặt `SHOW_BROWSER=false`** (qua biến môi trường). Nếu không, tiến trình sẽ báo lỗi tìm kiếm DISPLAY hoặc gây treo luồng khởi động.

### 1.4. Nguyên tắc Bộ gõ Công thức Toán Word (MML2OMML)
- Trên hệ điều hành Windows đã cài Microsoft Office, `export_docx.py` tự động nhận diện file `MML2OMML.XSL` trong thư mục Office để chuyển đổi công thức LaTeX sang Equation chuẩn gốc (Native Word OMML).
- Trên hệ điều hành Linux hoặc Docker: Để kích hoạt tính năng Native Equation tương đương, quản trị viên chỉ cần sao chép file `MML2OMML.XSL` vào thư mục gốc của dự án hoặc đặt đường dẫn qua biến môi trường `MML2OMML_PATH=/app/MML2OMML.XSL`. Nếu không có file này, hệ thống sẽ tự động dùng bộ fallback công thức dạng text nghiêng chuẩn thẩm mỹ mà không gây lỗi chương trình.

### 1.5. Giới hạn Tài nguyên Hệ thống (Resource Capacity)
- **CPU:** Tối thiểu 1 vCPU (Khuyến nghị 2 vCPU). Việc vẽ đồ thị (`matplotlib`) và giải nghiệm hình thức (`sympy`) tiêu tốn CPU đột biến trong thời gian ngắn (1 - 3 giây/câu).
- **RAM:** Tối thiểu 1 GB RAM khả dụng (Khuyến nghị 2 GB đến 4 GB nếu phục vụ từ 5 đến 20 giáo viên đồng thời).

---

## 2. Bảng Cấu hình Biến Môi trường (.env)

Hệ thống hỗ trợ nạp cấu hình linh hoạt thông qua biến môi trường của hệ điều hành hoặc file `.env`:

| Tên biến | Kiểu giá trị | Mặc định | Ý nghĩa & Hướng dẫn |
| :--- | :---: | :---: | :--- |
| `HOST` | String | `0.0.0.0` | IP lắng nghe của server (`0.0.0.0` cho phép truy cập từ mọi mạng/LAN/Internet, `127.0.0.1` chỉ cho máy nội bộ). |
| `PORT` | Integer | `8080` | Cổng HTTP lắng nghe của ứng dụng. Có thể đổi sang `80`, `3000`, `5000` tùy hạ tầng. |
| `SHOW_BROWSER` | Boolean | `true` | Tự động mở cửa sổ trình duyệt khi ứng dụng khởi chạy. Đặt `false` trên Server/Docker. |
| `MML2OMML_PATH` | Path | `None` | Đường dẫn tùy chọn tới file `MML2OMML.XSL` chuyển đổi công thức toán trên Linux/Docker. |
| `ENV` | String | `production` | Môi trường triển khai (`development` hoặc `production`). |

---

## Phương án 1: Triển khai Cục bộ & Mạng nội bộ (LAN)

Phù hợp cho: Giáo viên đơn lẻ hoặc tổ chuyên môn chia sẻ một máy tính trạm làm máy chủ dùng chung trong mạng trường học/gia đình.

### Bước 1: Cài đặt Tự Động (One-Click)
1. Cài đặt Python 3.10+ (nếu máy chưa có).
2. Nhấp đúp vào file [install.bat](file:///D:/MathAI/de-toan-ai/install.bat). Script sẽ tự động:
   - Nhận diện Python trên máy hoặc tự cài qua `winget`.
   - Tạo môi trường ảo riêng biệt `venv/` để không xung đột thư viện hệ thống.
   - Nâng cấp `pip` và cài đặt đầy đủ tất cả thư viện trong `requirements.txt`.
   - Tự động tạo thư mục và file cấu hình `.env`.
   - Chạy test kiểm thử toàn vẹn (Sanity Check) đảm bảo không có bất kỳ lỗi nào.

### Bước 2: Thiết lập IP Lắng nghe Mạng LAN
Mở file `.env` (hoặc tạo từ `.env.example`) và đảm bảo:
```env
HOST=0.0.0.0
PORT=8080
SHOW_BROWSER=true
```

### Bước 3: Mở Cổng Tường lửa Windows (Windows Firewall)
Để các máy tính khác trong trường học kết nối được vào máy chủ:
1. Mở PowerShell với quyền **Run as Administrator**.
2. Chạy lệnh mở cổng 8080:
   ```powershell
   New-NetFirewallRule -DisplayName "Math Studio" -Direction Inbound -LocalPort 8080 -Protocol TCP -Action Allow
   ```

### Bước 4: Khởi chạy và Truy cập
- Nhấp đúp vào file `run_app.bat` trên máy chủ.
- Xem địa chỉ IP của máy chủ bằng lệnh `ipconfig` (Ví dụ: `192.168.1.15`).
- Các máy tính khác trong cùng mạng Wi-Fi/LAN truy cập qua:
  ```text
  http://192.168.1.15:8080
  ```

---

## Phương án 2: Triển khai bằng Docker & Docker Compose (Khuyến nghị)

Đây là phương pháp triển khai chuẩn mực, ổn định và dễ bảo trì nhất trên mọi môi trường (Windows Server, Linux Server, MacOS).

### Bước 1: Cấu hình Tập tin Dịch vụ
Dự án đã tích hợp sẵn [Dockerfile](file:///D:/MathAI/de-toan-ai/Dockerfile) và [docker-compose.yml](file:///D:/MathAI/de-toan-ai/docker-compose.yml).

### Bước 2: Khởi động Dịch vụ
Tại thư mục gốc dự án, thực hiện lệnh:
```bash
# Build image và chạy container ở chế độ nền (detached mode)
docker compose up -d --build
```

### Bước 3: Kiểm tra Trạng thái & Nhật ký
```bash
# Kiểm tra container đang chạy và kiểm tra tính năng Healthcheck
docker compose ps

# Xem log trực tiếp của ứng dụng
docker compose logs -f math-studio
```

### Bước 4: Cập nhật Ứng dụng khi có Mã nguồn Mới
```bash
# Lấy code mới và build lại container mà không làm mất dữ liệu output
git pull
docker compose up -d --build
```

### Bước 5: Dừng Dịch vụ
```bash
docker compose down
```

> [!NOTE]
> Nhờ cấu hình `volumes` trong `docker-compose.yml`, toàn bộ thư mục `./input` và `./output` trên máy chủ vật lý được gắn trực tiếp vào container. Khi bạn nâng cấp hoặc xóa container, toàn bộ đề thi, ảnh đồ thị và lịch sử đều được bảo toàn 100%.

---

## Phương án 3: Triển khai Máy chủ Linux VPS (Ubuntu/Debian) với Nginx & Systemd

Phù hợp cho: Triển khai đưa ứng dụng lên tên miền công khai (Public Domain) với chứng chỉ bảo mật HTTPS (SSL Let's Encrypt).

### Bước 1: Cài đặt Gói Nền tảng trên VPS
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx \
    libxml2-dev libxslt1-dev fonts-dejavu-core fonts-liberation
```

### Bước 2: Đưa Mã nguồn Lên Máy Chủ
```bash
sudo mkdir -p /var/www/math-studio
sudo chown -R $USER:$USER /var/www/math-studio
cd /var/www/math-studio

# Clone mã nguồn dự án vào thư mục này
git clone <URL_GIT_REPO> .

# Tạo môi trường ảo và cài đặt thư viện
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Bước 3: Tạo Cấu hình Biến Môi trường Production
Tạo file `/var/www/math-studio/.env`:
```env
HOST=127.0.0.1
PORT=8080
SHOW_BROWSER=false
ENV=production
```

### Bước 4: Thiết lập Dịch vụ Systemd Tự Khởi Động
Tạo file dịch vụ:
```bash
sudo nano /etc/systemd/system/math-studio.service
```
Dán nội dung sau vào:
```ini
[Unit]
Description=Math Studio Service
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/math-studio
EnvironmentFile=/var/www/math-studio/.env
ExecStart=/var/www/math-studio/venv/bin/python app.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```
Phân quyền và kích hoạt dịch vụ:
```bash
sudo chown -R www-data:www-data /var/www/math-studio
sudo systemctl daemon-reload
sudo systemctl enable math-studio
sudo systemctl start math-studio
sudo systemctl status math-studio
```

### Bước 5: Cấu hình Nginx Reverse Proxy (Có WebSocket)
Tạo file cấu hình máy chủ ảo:
```bash
sudo nano /etc/nginx/sites-available/math-studio
```
Nội dung cấu hình chuẩn:
```nginx
server {
    listen 80;
    server_name math.yourdomain.com; # Thay bằng tên miền hoặc IP của bạn

    client_max_body_size 50M; # Cho phép upload file đề và ảnh lớn

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;

        # Cấu hình bắt buộc cho WebSocket NiceGUI
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Thiết lập Header chuyển tiếp client
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Giữ kết nối WebSocket liên tục, không bị ngắt quãng
        proxy_read_timeout 86400s;
        proxy_send_timeout 86400s;
    }
}
```
Kích hoạt trang và tải lại Nginx:
```bash
sudo ln -s /etc/nginx/sites-available/math-studio /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Bước 6: Cài đặt Chứng chỉ SSL Miễn phí (HTTPS)
```bash
sudo certbot --nginx -d math.yourdomain.com
```
Lệnh này sẽ tự động gia hạn chứng chỉ SSL và cấu hình chuyển hướng HTTP sang HTTPS an toàn.

---

## Phương án 4: Triển khai Windows Server dạng Windows Service (NSSM)

Nếu bạn có máy chủ Windows Server và muốn ứng dụng chạy ngầm liên tục, tự động bật lại khi máy chủ khởi động lại mà không cần người dùng đăng nhập Desktop:

### Bước 1: Tải NSSM
1. Tải công cụ **NSSM (Non-Sucking Service Manager)** từ [nssm.cc](https://nssm.cc/download).
2. Giải nén và đặt file `nssm.exe` vào thư mục hệ thống (ví dụ `C:\Windows\System32` hoặc `D:\MathAI\nssm.exe`).

### Bước 2: Đăng ký Service
Mở Command Prompt với quyền Administrator và chạy lệnh:
```cmd
nssm install MathStudioService
```
Một giao diện đồ họa sẽ xuất hiện:
- **Application Path:** Trỏ đến file python trong môi trường của bạn (Ví dụ: `C:\Program Files\Python313\python.exe` hoặc `D:\MathAI\de-toan-ai\venv\Scripts\python.exe`).
- **Startup directory:** `D:\MathAI\de-toan-ai`
- **Arguments:** `app.py`
- **Tab Environment:**
  ```text
  HOST=0.0.0.0
  PORT=8080
  SHOW_BROWSER=false
  ```
Nhấp **Install service**.

### Bước 3: Khởi động Dịch vụ
```cmd
nssm start MathStudioService
```
Từ lúc này, ứng dụng sẽ chạy vĩnh viễn như một dịch vụ Windows chuẩn (`services.msc`).

---

## Phương án 5: Triển khai Cloud PaaS (Render, Railway, Fly.io)

### Triển khai trên Render.com
1. Đăng ký tài khoản tại [render.com](https://render.com) và kết nối kho GitHub của bạn.
2. Tạo một **Web Service** mới, chọn môi trường **Docker**.
3. Trong phần cấu hình:
   - **Environment Variables:**
     - `PORT`: `8080`
     - `SHOW_BROWSER`: `false`
     - `HOST`: `0.0.0.0`
4. **Gắn Persistent Disk (Rất quan trọng):**
   - Vào mục **Disks** $\rightarrow$ **Add Disk**.
   - Tên disk: `math-storage`.
   - Mount path: `/app/output`.
   - Size: `5 GB` trở lên.
5. Nhấp **Deploy Web Service**.

---

## 8. Quy trình Sao lưu (Backup) & Phục hồi Dữ liệu

Dữ liệu của Antigravity Math Studio tập trung hoàn toàn trong thư mục `output/`. Để đảm bảo an toàn dữ liệu:

### 8.1. Script Tự Động Sao Lưu Hàng Ngày (Crontab Linux)
Tạo script sao lưu `/var/www/math-studio/backup.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/math-studio"
DATE=$(date +'%Y%m%d_%H%M%S')
mkdir -p "$BACKUP_DIR"

tar -czf "$BACKUP_DIR/math_output_$DATE.tar.gz" -C /var/www/math-studio output
# Giữ lại các bản sao lưu trong vòng 30 ngày gần nhất
find "$BACKUP_DIR" -type f -name "*.tar.gz" -mtime +30 -delete
```
Cấp quyền và đưa vào crontab chạy lúc 2:00 sáng mỗi ngày:
```bash
chmod +x /var/www/math-studio/backup.sh
(crontab -l 2>/dev/null; echo "0 2 * * * /var/www/math-studio/backup.sh") | crontab -
```

### 8.2. Phục hồi Dữ liệu (Restore)
Khi cần khôi phục lại dữ liệu trên server mới:
```bash
# Giải nén đè lại thư mục output
tar -xzf /var/backups/math-studio/math_output_YYYYMMDD_HHMMSS.tar.gz -C /var/www/math-studio/
```

---

## 9. Xử lý Sự cố Thường gặp (Troubleshooting)

### 9.1. Giao diện báo "Connection lost. Trying to reconnect..."
- **Nguyên nhân:** Reverse proxy (Nginx / Cloudflare / Apache) chưa bật cấu hình hỗ trợ WebSocket hoặc timeout kết nối quá ngắn.
- **Cách khắc phục:**
  1. Kiểm tra khối Nginx location đã có đủ `proxy_set_header Upgrade $http_upgrade;` và `proxy_set_header Connection "upgrade";`.
  2. Nâng `proxy_read_timeout 86400s;`.
  3. Nếu dùng Cloudflare, hãy bật mục **WebSockets** trong tab *Network* của bảng điều khiển Cloudflare.

### 9.2. Báo lỗi `[Errno 98] Address already in use` hoặc `Port 8080 is in use`
- **Nguyên nhân:** Cổng 8080 đang có tiến trình khác chiếm dụng hoặc phiên bản app cũ chưa tắt hẳn.
- **Cách khắc phục:**
  - **Trên Windows:**
    ```powershell
    netstat -ano | findstr :8080
    taskkill /PID <PID_TIM_THAY> /F
    ```
  - **Trên Linux:**
    ```bash
    sudo fuser -k 8080/tcp
    ```
  - Hoặc đổi cổng khác trong file `.env`: `PORT=8088`.

### 9.3. Xuất file Word (.docx) công thức không biến thành Equation Word chuẩn
- **Nguyên nhân:** Trên hệ thống thiếu file stylesheet `MML2OMML.XSL` (thường xảy ra khi chạy trên Linux hoặc Docker không có cài Microsoft Office).
- **Cách khắc phục:**
  1. Lấy file `MML2OMML.XSL` từ một máy Windows (nằm tại `C:\Program Files\Microsoft Office\root\Office16\MML2OMML.XSL`).
  2. Đặt file này ngay vào thư mục gốc của dự án `de-toan-ai/MML2OMML.XSL`.
  3. `export_docx.py` sẽ tự động phát hiện và kích hoạt bộ biên dịch OMML Native ngay tức thì.

### 9.4. Báo lỗi `[WinError 10054] An existing connection was forcibly closed by the remote host`
- **Giải thích:** Đây là hành vi bình thường của cơ chế kết nối Proactor Event Loop trên hệ điều hành Windows khi người dùng bấm phím F5 (Refresh) hoặc đóng tab trình duyệt đột ngột khiến socket bị đứt.
- **Xử lý:** Ứng dụng trong `app.py` đã tích hợp sẵn đoạn vá lỗi ngắt êm dịu (`_silent_call_conn_lost`), không ảnh hưởng đến độ ổn định và tiến trình nền của server.

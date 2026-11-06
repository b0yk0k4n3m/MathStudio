# 🛠️ Hướng Dẫn Cài Đặt Công Cụ & Môi Trường Chạy Math Studio

Tài liệu này cung cấp **đầy đủ link tải trực tiếp** và hướng dẫn từng bước cài đặt các công cụ cần thiết để chạy hệ thống **Math Studio**. Hướng dẫn được biên soạn theo phong cách trực quan, gần gũi, giúp các Thầy/Cô giáo dù không chuyên về công nghệ thông tin vẫn có thể dễ dàng cài đặt và sử dụng thành công trong 5 phút.

---

## 🌟 HƯỚNG DẪN 3 BƯỚC NHANH CHO THẦY CÔ GIÁO

Nếu Thầy/Cô không rành về kỹ thuật hay dòng lệnh, chỉ cần làm đúng 3 bước đơn giản sau:

### 🟢 Bước 1: Tải bộ cài đặt Python về máy tính
👉 **[Nhấp vào đây để tải trực tiếp Python 3.11 (Bản chuẩn 64-bit cho Windows)](https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe)**

*(Nếu máy tính của Thầy/Cô dùng hệ điều hành khác hoặc cần bản 32-bit: xem tại [Trang chủ Python Windows](https://www.python.org/downloads/windows/))*.

---

### 🟢 Bước 2: Cài đặt Python và TÍCH CHỌN ô "Add to PATH"
1. Mở file cài đặt vừa tải về (`python-3.11.9-amd64.exe`).
2. **LƯU Ý CỰC KỲ QUAN TRỌNG:** Ở ngay màn hình đầu tiên xuất hiện, Thầy/Cô hãy nhìn xuống dưới cùng cửa sổ và **bấm chuột tích vào ô vuông**:
   > `☑ Add python.exe to PATH`

```text
┌────────────────────────────────────────────────────────────────────────┐
│  Python 3.11.9 (64-bit) Setup                                          │
│                                                                        │
│   ➡️  Install Now                                                      │
│       C:\Users\ThayCo\AppData\Local\Programs\Python\Python311          │
│       (Bấm vào đây SAU KHI đã tích ô ở dưới)                           │
│                                                                        │
│   ⚙️  Customize installation                                           │
│                                                                        │
│   [ ] Use admin privileges when installing py.exe                      │
│   [X] Add python.exe to PATH   <=== ⚠️ THẦY CÔ BẮT BUỘC TÍCH Ô NÀY!   │
└────────────────────────────────────────────────────────────────────────┘
```

3. Sau khi đã tích ô `☑ Add python.exe to PATH`, Thầy/Cô bấm vào dòng chữ lớn **`Install Now`** ở phía trên.
4. Đợi khoảng 1 phút cho thanh chạy hoàn tất, bấm **Close** để đóng cửa sổ.

> [!TIP]
> **Nếu Thầy/Cô lỡ quên không tích ô này thì sao?**
> Thầy/Cô **hoàn toàn yên tâm**! Bộ cài tự động `install.bat` và `run_app.bat` của Math Studio đã được tích hợp thuật toán thông minh **tự động dò tìm Python** trong mọi thư mục mặc định của Windows. Kể cả khi quên tích ô này, hệ thống vẫn tự nhận diện và khởi động bình thường!

---

### 🟢 Bước 3: Khởi động Math Studio (1-Click)
1. Trong thư mục dự án `MathStudio`, Thầy/Cô **nhấp đúp chuột vào file `install.bat`** (Hệ thống sẽ tự động tải các gói tính toán, vẽ hình, tạo đề trong 1-2 phút).
2. Sau khi cài xong, Thầy/Cô **nhấp đúp chuột vào file `run_app.bat`**.
3. Trình duyệt web sẽ tự động mở ra giao diện soạn đề Math Studio tại:
   👉 **`http://localhost:8080`**

---

## 📋 Danh Mục Link Tải Các Công Cụ Cần Thiết

Dưới đây là bảng tổng hợp link tải trực tiếp các phần mềm phục vụ toàn bộ chu trình hoạt động của Math Studio:

| Công Cụ | Link Tải Trực Tiếp (1-Click) | Mục Đích Sử Dụng | Mức Độ |
| :--- | :--- | :--- | :--- |
| **Python 3.11.9** | 📥 [**Tải Python 3.11 Windows 64-bit (.exe)**](https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe) | Máy chủ Web, tính toán SymPy, vẽ đồ thị & xuất Word | **Bắt buộc** |
| **Google Antigravity** | 🤖 [**Trang chủ Google Antigravity (CLI / IDE)**](https://antigravity.google) | Autonomous AI Agent tự động soạn đề, thẩm định nghiệm | **Khuyến nghị cao** |
| **Git for Windows** | 📥 [**Tải Git 64-bit Windows (.exe)**](https://github.com/git-for-windows/git/releases/download/v2.47.1.windows.1/Git-2.47.1-64-bit.exe) | Đồng bộ mã nguồn và cập nhật tính năng từ GitHub | **Khuyến nghị** |
| **Microsoft Word** | 💼 [**Trang chủ Microsoft Office / 365**](https://www.office.com/) | Mở & in ấn đề thi chứa công thức Native Equation (OMML) | **Khuyến nghị** |
| **LibreOffice** | 📥 [**Tải LibreOffice Tiếng Việt (Miễn phí 100%)**](https://www.libreoffice.org/download/download/) | Phần mềm mở file Word miễn phí nếu máy chưa có Office | **Thay thế Word** |
| **Trình duyệt Web** | 🌐 [**Tải Google Chrome**](https://www.google.com/chrome/) \| [**Microsoft Edge**](https://www.microsoft.com/edge) | Xem và tương tác giao diện biên soạn trực quan | **Bắt buộc** |

---

## 🤖 Hướng Dẫn Cài Đặt & Sử Dụng Google Antigravity (CLI / IDE)

### 1. Google Antigravity là gì?
**Google Antigravity** (AGY) là môi trường Agentic AI Coding thế hệ mới từ Google DeepMind được cài đặt và vận hành trực tiếp trên máy tính của bạn (dưới dạng **Antigravity CLI** `agy` hoặc **Antigravity IDE**). Trong Math Studio, Antigravity đóng vai trò như một **Trợ lý Khảo thí Toán học chuyên nghiệp**:
- Đọc hiểu sâu sắc **Công văn 7991/BGDĐT-GDTrH** và cấu trúc **Tốt nghiệp THPT 2026**.
- Tự động lập trình và chạy các thuật toán đại số độc lập bằng **SymPy** để giải nghiệm, tính đạo hàm, tích phân, tọa độ vector và thẩm định tính đúng/sai của từng mệnh đề.
- Tự động vẽ đồ thị hàm số và hình học không gian đạt chuẩn nét vẽ SGK bằng thư viện `math_draw.py`.
- Tự động sửa số liệu nếu phát hiện nghiệm xấu hoặc trùng phương án.

### 2. Cài đặt & Đăng nhập Antigravity (Không cần tạo API Key thủ công)
- Truy cập trang chủ chính thức: 👉 **[antigravity.google](https://antigravity.google)** để tải và cài đặt **Antigravity CLI** hoặc **Antigravity IDE**.
- **Xác thực tài khoản (Authentication):** Khi khởi chạy lần đầu tiên, Antigravity sẽ tự động mở trình duyệt để bạn đăng nhập trực tiếp bằng tài khoản Google của mình. **Bạn hoàn toàn không cần phải đi lấy API Key thủ công hay cấu hình phức tạp.**

### 3. Ra lệnh tạo đề tự động với Slash Command `/tao-de`
1. Mở Terminal / PowerShell tại thư mục dự án `MathStudio`, gõ lệnh:
   ```bash
   agy
   ```
   *(Hoặc mở thư mục dự án trực tiếp bằng Antigravity IDE).*
2. Trong khung chat của Antigravity, Thầy/Cô chỉ cần gõ yêu cầu kèm lệnh `/tao-de`:
   > `/tao-de Soạn cho tôi 01 đề kiểm tra cuối học kỳ 2 Toán 11 theo đúng chuẩn Công văn 7991, có đầy đủ Ma trận (Phụ lục 1), Bản đặc tả (Phụ lục 2) và lời giải chi tiết.`

Agent sẽ tự động kích hoạt workflow 6 bước, viết code kiểm định nghiệm SymPy, vẽ đồ thị hàm số và xuất kết quả ra file Word/Markdown trong thư mục `output/`. Thầy/Cô chỉ cần mở giao diện Web App lên để xem và tải về!

---

## 💻 Hướng Dẫn Dành Cho Người Thích Dùng Dòng Lệnh (CLI)

Nếu bạn quen dùng dòng lệnh Terminal/PowerShell:

```bash
# 1. Tải mã nguồn về máy
git clone https://github.com/b0yk0k4n3m/MathStudio.git
cd MathStudio

# 2. Tạo và kích hoạt môi trường ảo Python
python -m venv venv
# Trên Windows:
venv\Scripts\activate
# Trên Linux/macOS:
source venv/bin/activate

# 3. Nâng cấp pip và cài đặt toàn bộ thư viện
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Khởi chạy máy chủ Web
python app.py
```
Mở trình duyệt truy cập: `http://localhost:8080`

---

## ❓ Câu Hỏi & Xử Lý Sự Cố Thường Gặp

### Q1: Tôi mở `run_app.bat` nhưng cửa sổ hiện lên rồi tắt ngay?
- **Nguyên nhân:** Máy tính của bạn chưa từng chạy file `install.bat` để tạo môi trường.
- **Khắc phục:** Hãy nhấp đúp vào file `install.bat`, đợi chạy xong xuất hiện thông báo `[HOAN TAT]` rồi hãy chạy `run_app.bat`.

### Q2: Ứng dụng báo lỗi `Port 8080 is already in use`?
- **Nguyên nhân:** Ứng dụng đang chạy ngầm ở một cửa sổ khác.
- **Khắc phục:** Nhấp đúp vào file [`stop_app.bat`](stop_app.bat) để tắt sạch các tiến trình cũ, sau đó mở lại `run_app.bat`.

### Q3: Mở file Word đề thi thấy công thức toán hiển thị bình thường không?
- **Trả lời:** **Có, cực kỳ chuẩn đẹp!** Toàn bộ đề thi xuất từ Math Studio đều ở chuẩn **Native Word Equation (OMML)** bản địa của Microsoft Word. Thầy/Cô mở bằng Word 2016, 2019, 2021 hoặc Microsoft 365 có thể nhấp đúp trực tiếp vào từng công thức để sửa số mà không cần cài đặt thêm MathType.

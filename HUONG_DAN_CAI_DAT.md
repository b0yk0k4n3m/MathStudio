# 🛠️ Hướng Dẫn Cài Đặt Công Cụ & Môi Trường Chạy Math Studio

Tài liệu này hướng dẫn chi tiết từng bước chuẩn bị các công cụ phần mềm cần thiết để khởi chạy và khai thác toàn bộ sức mạnh của hệ thống **Math Studio**, bao gồm môi trường chạy Python, nền tảng Trí tuệ Nhân tạo **Google Antigravity**, công cụ kiểm soát mã nguồn Git và các phần mềm văn phòng hỗ trợ.

---

## 📋 Danh Mục Công Cụ Cần Thiết

| Công Cụ | Phiên Bản Khuyến Nghị | Mục Đích Sử Dụng | Mức Độ |
| :--- | :--- | :--- | :--- |
| **Python** | `3.10` – `3.12` | Chạy máy chủ Web App, xử lý giải nghiệm đại số SymPy, vẽ đồ thị & xuất file Word | **Bắt buộc** |
| **Google Antigravity** | Antigravity CLI / IDE | Trợ lý Agentic AI tự động biên soạn câu hỏi, thẩm định lời giải, vẽ hình & đảo đề | **Khuyến nghị cao** |
| **Git** | `2.40+` | Tải mã nguồn dự án, đồng bộ cập nhật từ GitHub repository | **Khuyến nghị** |
| **Microsoft Word / Office** | `2016` trở lên hoặc 365 | Mở, in ấn và tinh chỉnh trực tiếp đề thi Word chứa công thức Native Equation (OMML) | **Khuyến nghị** |
| **Trình Duyệt Web** | Chrome, Edge, Brave, Firefox | Truy cập giao diện biên tập tương tác thời gian thực tại `http://localhost:8080` | **Bắt buộc** |

---

## 1. 🐍 Hướng Dẫn Cài Đặt Python (Bắt Buộc)

Python là môi trường nền tảng để chạy giao diện Web tương tác (NiceGUI), thư viện tính toán hình thức (SymPy), vẽ đồ thị (Matplotlib) và chuyển đổi công thức toán sang định dạng Word (python-docx + OMML).

### Bước 1: Tải bộ cài đặt Python
- Truy cập trang chủ chính thức: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Tải bản cài đặt mới nhất cho hệ điều hành của bạn (Khuyến nghị **Python 3.10**, **3.11** hoặc **3.12**; không dùng Python 3.9 trở xuống do chưa hỗ trợ cú pháp kiểu dữ liệu mới).

### Bước 2: Cài đặt trên Windows (Lưu Ý Cực Kỳ Quan Trọng)
1. Nhấp đúp vào file `.exe` vừa tải về (ví dụ: `python-3.11.x-amd64.exe`).
2. ⚠️ **BẮT BUỘC TICK VÀO Ô:**
   > `☑ Add python.exe to PATH` (nằm ở ngay góc dưới màn hình cài đặt đầu tiên).
   > *(Nếu quên tích ô này, máy tính sẽ báo lỗi `'python' is not recognized as an internal or external command` khi chạy script).*
3. Nhấp chọn **Install Now** và đợi quá trình cài đặt hoàn tất.
4. Ở màn hình cuối cùng, nếu thấy nút **Disable path length limit**, hãy nhấn vào đó để tránh lỗi đường dẫn dài trên Windows.

### Bước 3: Kiểm tra cài đặt thành công
Mở **Command Prompt (CMD)** hoặc **PowerShell** và gõ 2 lệnh sau:
```bash
python --version
# Kết quả hiển thị dạng: Python 3.11.x (hoặc 3.10.x, 3.12.x)

pip --version
# Kết quả hiển thị dạng: pip 24.x from ...
```

---

## 2. 🤖 Hướng Dẫn Cài Đặt & Cấu Hình Google Antigravity

### 2.1. Google Antigravity là gì?
**Google Antigravity** (AGY) là môi trường Agentic AI Coding tiên tiến được phát triển bởi Google DeepMind. Khác với các mô hình Chat thông thường chỉ trả về văn bản, Antigravity là một **Autonomous Agent** có thể:
- 📖 Đọc và hiểu toàn bộ cấu trúc dự án, ma trận khảo thí và các file hướng dẫn chuẩn của Bộ GD&ĐT.
- ⚡ Tự động lập trình và chạy các script Python `verify_math.py` sử dụng thư viện SymPy để giải nghiệm đại số, thẩm định tính đúng/sai của câu hỏi.
- 📊 Gọi module `math_draw.py` để tự động tính toán tọa độ và vẽ hình đồ thị / hình không gian.
- 🔄 Tự động chỉnh sửa lại tham số toán học nếu phát hiện nghiệm xấu hoặc trùng đáp án.

### 2.2. Cách cài đặt Antigravity
Tùy thuộc vào phương thức bạn tiếp cận Antigravity:
1. **Sử dụng Antigravity CLI (`agy`):**
   - Đảm bảo máy đã cài đặt Node.js hoặc gói cài đặt Antigravity từ Google.
   - Kiểm tra lệnh trong Terminal:
     ```bash
     agy --version
     ```
2. **Sử dụng Antigravity IDE / Extension:**
   - Mở dự án `MathStudio` trực tiếp trong môi trường Antigravity IDE.

### 2.3. Cấu hình API Key
- Antigravity kết nối với các mô hình suy luận mạnh mẽ của Google (Gemini 2.5 Pro / Flash).
- Đảm bảo bạn đã cấu hình API Key:
  - Trên Windows (PowerShell):
    ```powershell
    [System.Environment]::SetEnvironmentVariable('GEMINI_API_KEY', 'your-api-key-here', 'User')
    ```
  - Hoặc tạo file `.env` trong thư mục gốc của dự án:
    ```env
    GEMINI_API_KEY=your-api-key-here
    ```

### 2.4. Cách Dự Án Math Studio Tích Hợp Sẵn Với Antigravity
Dự án đã được cấu hình sẵn cấu trúc Agent tiêu chuẩn trong thư mục `.agent/`:
- **`📁 .agent/skills/tao-de/SKILL.md`**: Kỹ năng chuyên biệt để tạo đề thi chuẩn THPT 2026 hoặc Đề kiểm tra định kỳ Công văn 7991.
- **`📁 .agent/rules/math-standard.md`**: Hệ thống luật sư phạm nghiêm ngặt (chuẩn ký hiệu toán học Việt Nam, quy tắc kiểm định nghiệm, bảng điểm lũy tiến Đúng/Sai).
- **`📁 .agent/workflows/tao-de.md`**: Quy trình tự động 6 bước khép kín từ nhận yêu cầu $\rightarrow$ soạn đề $\rightarrow$ kiểm định SymPy $\rightarrow$ vẽ hình $\rightarrow$ xuất bản.

### 2.5. Cách ra lệnh cho Antigravity tạo đề tự động:
Khi mở dự án trong Antigravity, bạn chỉ cần gõ yêu cầu vào khung chat, ví dụ:
```text
/tao-de Soạn cho tôi một đề kiểm tra giữa học kỳ 2 Toán 12 theo đúng chuẩn Công văn 7991/BGDĐT-GDTrH, chủ đề Nguyên hàm - Tích phân và Hình học Oxyz.
```
Agent Antigravity sẽ:
1. Nạp tri thức từ Công văn 7991 và Ma trận chuẩn.
2. Soạn thảo đủ 4 phần (Trắc nghiệm nhiều lựa chọn, Đúng/Sai, Trả lời ngắn, Tự luận).
3. Tự viết mã giải nghiệm độc lập để đảm bảo 100% đáp án chính xác.
4. Xuất file kết quả vào thư mục `output/`. Bạn chỉ cần mở Web App lên để xem và tải file Word!

---

## 3. 📦 Cài Đặt Mã Nguồn & Thư Viện Dự Án

### Bước 1: Tải mã nguồn về máy
Nếu bạn đã cài Git:
```bash
git clone git@github.com:b0yk0k4n3m/MathStudio.git
cd MathStudio
```
*(Hoặc tải file `.zip` từ GitHub rồi giải nén vào thư mục bạn muốn).*

### Bước 2: Cài đặt thư viện phụ thuộc (Dependencies)
Dự án cung cấp sẵn file cài đặt 1-click cho người dùng Windows:
- **Cách 1 (Nhanh nhất trên Windows):** Nhấp đúp chuột vào file [`install.bat`](install.bat). File này sẽ tự động tạo môi trường ảo `venv` và cài đặt đầy đủ các gói: `nicegui`, `sympy`, `matplotlib`, `python-docx`, `latex2mathml`, `jinja2`, `uvicorn`...
- **Cách 2 (Thủ công qua dòng lệnh):**
  ```bash
  # 1. Tạo môi trường ảo
  python -m venv venv

  # 2. Kích hoạt môi trường ảo:
  # Trên Windows:
  venv\Scripts\activate
  # Trên macOS / Linux:
  source venv/bin/activate

  # 3. Nâng cấp pip và cài đặt thư viện
  python -m pip install --upgrade pip
  pip install -r requirements.txt
  ```

---

## 4. 🚀 Khởi Chạy Ứng Dụng Math Studio

Sau khi cài đặt xong, bạn có thể khởi chạy ứng dụng bất cứ lúc nào:
1. **Trên Windows (1-Click):**
   - Nhấp đúp vào [`run_app.bat`](run_app.bat).
   - Cửa sổ dòng lệnh sẽ khởi động máy chủ và tự động mở trình duyệt tại địa chỉ:
     👉 **`http://localhost:8080`**
2. **Dừng ứng dụng:**
   - Khi không sử dụng nữa, bạn nhấp đúp vào [`stop_app.bat`](stop_app.bat) để tắt tiến trình nền và giải phóng cổng mạng `8080`.

---

## 5. ❓ Xử Lý Lỗi Thường Gặp (Troubleshooting)

### Lỗi 1: `'python' is not recognized as an internal or external command`
- **Nguyên nhân:** Khi cài đặt Python, bạn chưa tích chọn `Add python.exe to PATH`.
- **Cách khắc phục:** 
  1. Chạy lại bộ cài đặt Python `.exe`.
  2. Chọn **Modify** hoặc cài đặt lại, nhớ tích chọn `☑ Add python.exe to PATH`.
  3. Đóng tất cả cửa sổ Terminal / PowerShell hiện tại và mở lại.

### Lỗi 2: Lỗi cổng mạng `Port 8080 is already in use`
- **Nguyên nhân:** Một phiên bản cũ của ứng dụng hoặc một phần mềm khác đang chiếm cổng `8080`.
- **Cách khắc phục:**
  - Nhấp đúp vào [`stop_app.bat`](stop_app.bat) để tắt tiến trình cũ.
  - Hoặc mở file [`app.py`](app.py), kéo xuống dòng cuối cùng và đổi `port=8080` thành cổng khác (ví dụ: `port=8088`).

### Lỗi 3: Công thức toán trong Word bị hiển thị dạng chữ thô thay vì công thức đẹp
- **Nguyên nhân:** Mở file `.docx` bằng các phần mềm soạn thảo không hỗ trợ chuẩn Office Math Markup Language (OMML).
- **Cách khắc phục:**
  - Hãy mở bằng **Microsoft Word 2016, 2019, 2021 hoặc Microsoft 365**.
  - Toàn bộ công thức toán trong Math Studio được xuất bản dưới dạng **Native Equation**, cho phép bạn nhấp đúp vào công thức để chỉnh sửa trực tiếp mà không cần cài thêm MathType.

### Lỗi 4: Khi dùng Git báo lỗi `Permission denied (publickey)`
- **Cách khắc phục:**
  - Nếu bạn chưa cấu hình SSH Key trên GitHub, hãy dùng đường dẫn HTTPS để clone:
    ```bash
    git clone https://github.com/b0yk0k4n3m/MathStudio.git
    ```

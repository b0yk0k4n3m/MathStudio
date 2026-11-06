<div align="center">

# 📐 Math Studio

### Hệ Thống Biên Soạn, Thẩm Định Toán Học & Xuất Bản Đề Thi THPT 2026

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-informational.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Program](https://img.shields.io/badge/Chương_trình-GDPT_2018-success.svg?style=for-the-badge)](https://moet.gov.vn/)
[![Format](https://img.shields.io/badge/Cấu_trúc-THPT_2026-orange.svg?style=for-the-badge)](https://moet.gov.vn/)
[![UI](https://img.shields.io/badge/Giao_diện-NiceGUI_Web-purple.svg?style=for-the-badge)](https://nicegui.io/)

<p align="center">
  <b>Giải pháp tự động hóa toàn diện quy trình thiết kế ma trận, biên soạn câu hỏi, kiểm định nghiệm chính xác tuyệt đối và xuất bản đề thi Microsoft Word (.docx) bản địa.</b>
</p>

[✨ Tính Năng Nổi Bật](#-tính-năng-nổi-bật) •
[🚀 Khởi Chạy Nhanh](#-khởi-chạy-nhanh) •
[📂 Cấu Trúc Dự Án](#-cấu-trúc-dự-án) •
[📖 Tài Liệu Chi Tiết](#-tài-liệu-hướng-dẫn-chi-tiết) •
[👨‍💻 Tác Giả](#-tác-giả--liên-hệ) •
[📄 Giấy Phép](#-giấy-phép-bản-quyền-license)

---

</div>

## 🌟 Giới Thiệu Chung

**Math Studio** là nền tảng công nghệ giáo dục chuyên sâu (EdTech) phục vụ công tác khảo thí, ra đề thi và ôn luyện môn Toán bậc THPT. Ứng dụng bám sát 100% định hướng đổi mới của **Chương trình Giáo dục Phổ thông 2018** và cấu trúc kỳ thi **Tốt nghiệp THPT từ năm 2025 – 2026** ban hành bởi Bộ Giáo dục & Đào tạo.

Hệ thống giải quyết triệt để các thách thức lớn nhất của giáo viên khi ra đề:
- ⏳ **Tiết kiệm hàng chục giờ soạn thảo:** Tự động tạo câu hỏi theo đúng ma trận nhận thức 4 mức độ.
- 🎯 **Triệt tiêu lỗi sai đề:** Giải nghiệm hình thức tự động, chống nhầm lẫn, trùng đáp án hoặc số liệu vô lý.
- 📐 **Chuẩn mực vẽ hình sư phạm:** Tự động vẽ đồ thị hàm số và hình học không gian chuẩn nét SGK.
- 📝 **Công thức Word chuẩn bản địa:** Xuất file `.docx` chứa công thức toán dạng Equation gốc (OMML), có thể nhấp đúp chỉnh sửa trực tiếp không qua ảnh chụp.

---

## ✨ Tính Năng Nổi Bật

### 1. 🎯 Chuẩn Cấu Trúc Đề Thi Tốt Nghiệp THPT 2026
Tự động phân bổ cấu trúc đề chuẩn gồm **22 câu hỏi – 90 phút – 10.00 điểm**:
- **PHẦN I (12 câu - 3.0 điểm):** Trắc nghiệm 4 phương án (A, B, C, D) chọn 1 đáp án đúng (0.25đ/câu), đánh giá năng lực *Nhận biết* và *Thông hiểu*.
- **PHẦN II (4 câu - 4.0 điểm):** Trắc nghiệm Đúng/Sai dạng bài toán tự luận tích hợp 4 mệnh đề $a), b), c), d)$ theo thang tư duy (NB $\rightarrow$ TH $\rightarrow$ VD $\rightarrow$ VDC). Áp dụng quy tắc điểm lũy tiến: Đúng 1 ý = 0.1đ; Đúng 2 ý = 0.25đ; Đúng 3 ý = 0.5đ; Đúng 4 ý = 1.0đ.
- **PHẦN III (6 câu - 3.0 điểm):** Trắc nghiệm trả lời ngắn (0.5đ/câu), đánh giá năng lực *Vận dụng* giải quyết tình huống thực tế, kết quả số gọn gàng.

### 2. 📐 Thẩm Định Toán Học Độc Lập
- Tự động thiết lập mã kiểm định giải nghiệm đại số, đạo hàm, tích phân, tọa độ $Oxyz$ và hình học không gian.
- Kiểm tra tính đúng/sai của từng mệnh đề trong Phần II và xác thực đáp số Phần III trước khi xuất bản.
- Tích hợp cửa sổ **Kiểm định Toán** cho phép giáo viên theo dõi và chạy thử nghiệm thuật toán tính toán.

### 3. 📊 Tự Động Dựng Đồ Thị & Hình Học Không Gian
- Đồ thị hàm số bậc ba, hàm phân thức bậc nhất/bậc nhất, hàm bậc hai/bậc nhất có tiệm cận xiên.
- Hình học không gian: Khối chóp, lăng trụ, hình nón, hình trụ tuân thủ nghiêm ngặt quy chuẩn nét thấy (`solid`), nét khuất (`dashed`), ký hiệu góc vuông và nhãn đỉnh.
- Tự động sinh file ảnh độ nét cao và liên kết trực tiếp vào đề thi Markdown / Word.

### 4. 📝 Xuất Bản Microsoft Word (.docx) Chuẩn OMML & Trộn Mã Đề
- Chuyển đổi công thức LaTeX trực tiếp thành **Native Word Equation (OMML)**.
- Người dùng có thể nhấp đúp vào công thức trong Word để chỉnh sửa dễ dàng, không bị vỡ nét như công thức chèn dạng ảnh.
- Tự động tạo nhiều mã đề đảo (101, 102, 103, 104...) kèm bảng đáp án chi tiết và ma trận đặc tả.

### 5. ⚡ Tinh Chỉnh Câu Hỏi Linh Hoạt
- **🎲 Đổi số mới (1-Click):** Tự động sinh bộ tham số khác có nghiệm đẹp, giữ nguyên dạng toán và tạo lại lời giải chi tiết mới.
- **🤖 Tinh chỉnh thông minh:** Gắn bài toán vào bối cảnh thực tế, chuyển dạng đồ thị/hình vẽ hoặc nâng/hạ mức độ tư duy.
- **✏️ Sửa tay trực tiếp:** Trình biên soạn Markdown/LaTeX thời gian thực với công nghệ xem trước MathJax/KaTeX.

---

## 🚀 Khởi Chạy Nhanh

### Cách 1: Khởi Động 1-Click trên Windows (Khuyến nghị)
1. **Cài đặt tự động:** Nhấp đúp vào file [`install.bat`](install.bat) (tự động tạo môi trường ảo `venv` và cài đặt gói phụ thuộc).
2. **Khởi chạy ứng dụng:** Nhấp đúp vào file [`run_app.bat`](run_app.bat) để mở giao diện tại `http://localhost:8080`.
3. **Dừng máy chủ:** Nhấp đúp vào file [`stop_app.bat`](stop_app.bat) khi muốn tắt ứng dụng và giải phóng cổng kết nối.

### Cách 2: Cài Đặt Thủ Công qua Dòng Lệnh
```bash
# 1. Tạo môi trường ảo
python -m venv venv

# 2. Kích hoạt môi trường:
# Trên Windows:
venv\Scripts\activate
# Trên Linux/macOS:
source venv/bin/activate

# 3. Cài đặt các thư viện
pip install -r requirements.txt

# 4. Khởi chạy máy chủ
python app.py
```
Mở trình duyệt web và truy cập địa chỉ: **`http://localhost:8080`**

---

## 📂 Cấu Trúc Dự Án

```text
de-toan-ai/
├── app.py                  # Giao diện Web Application (NiceGUI)
├── export_docx.py          # Module xuất đề thi Word (.docx) chuẩn Native Equation (OMML)
├── math_draw.py            # Thư viện tự động vẽ đồ thị hàm số & hình không gian
├── verify_math.py          # Mã nguồn kiểm định toán học toàn bộ đề
├── verify_single.py        # Mã nguồn kiểm định toán học từng câu đơn lẻ
├── CURRENT_TASK.md         # File cấu hình yêu cầu đề thi đang soạn thảo
├── requirements.txt        # Danh mục thư viện Python phụ thuộc
├── install.bat             # Cài đặt tự động môi trường 1-click (Windows)
├── run_app.bat             # Khởi chạy ứng dụng 1-click (Windows)
├── stop_app.bat            # Tắt ứng dụng & giải phóng cổng kết nối (Windows)
├── Dockerfile              # Cấu hình container hóa Docker
├── docker-compose.yml      # Cấu hình triển khai dịch vụ Docker Compose
├── LICENSE                 # Giấy phép bản quyền mã nguồn mở (MIT)
├── GUIDELINES.md           # Hướng dẫn sử dụng & quy chuẩn đề thi chi tiết
├── DEPLOYMENT.md           # Hướng dẫn triển khai Production (VPS, LAN, Docker, Cloud)
├── input/                  # Chứa file đề mẫu, ảnh đề bài đầu vào
│   └── blueprint_images/   # Ảnh ma trận đề hoặc đề gốc tải lên
└── output/                 # Lưu trữ thành phẩm đề thi
    ├── images/             # Ảnh đồ thị & hình không gian tự động sinh
    ├── history/            # Lịch sử các phiên bản sửa đổi đề thi
    ├── scripts/            # Script kiểm định tương ứng từng đề
    ├── exams_index.json    # Cơ sở dữ liệu danh mục đề thi
    └── matrix_templates.json # Kho mẫu ma trận đề thi
```

---

## 📖 Tài Liệu Hướng Dẫn Chi Tiết

Hệ thống có đầy đủ tài liệu hướng dẫn kỹ thuật chuyên sâu được phân tách rõ ràng:

- 📋 [**GUIDELINES.md**](GUIDELINES.md): Hướng dẫn sử dụng chi tiết từng chức năng trên giao diện Web, quy cách cấu trúc đề 2026, quy chuẩn công thức LaTeX và quy tắc kiểm định toán học.
- 🚀 [**DEPLOYMENT.md**](DEPLOYMENT.md): Hướng dẫn triển khai hệ thống toàn diện: Mạng nội bộ trường học (LAN), Docker / Docker Compose, Linux VPS (Nginx + Systemd + SSL), Windows Server (Windows Service NSSM) và Cloud PaaS (Render, Railway, Fly.io).

---

## 👨‍💻 Tác Giả & Liên Hệ

- **Tác giả phát triển:** Nguyễn Minh Trung
- **Email:** [minhtrung.mis@gmail.com](mailto:minhtrung.mis@gmail.com)
- **Lĩnh vực nghiên cứu:** Công nghệ Giáo dục (EdTech), Tự động hóa Khảo thí & Đo lường Đề thi Toán THPT.
- **Định hướng phát triển:** Nghiên cứu và ứng dụng Trí tuệ Nhân tạo hỗ trợ giáo viên và học sinh đổi mới phương pháp dạy học, nâng cao chất lượng đề thi theo Chương trình GDPT 2018.

---

## 📄 Giấy Phép Bản Quyền (License)

Dự án được phân phối dưới giấy phép mã nguồn mở **[MIT License](LICENSE)**. Bạn được toàn quyền sử dụng, sao chép, chỉnh sửa, sáp nhập, xuất bản và phân phối lại cho mục đích giáo dục, nghiên cứu hoặc thương mại theo các điều khoản của giấy phép MIT.

Copyright (c) 2026 **Nguyen Minh Trung**.

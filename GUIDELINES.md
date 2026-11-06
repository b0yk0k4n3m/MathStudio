# 📖 Hướng Dẫn Sử Dụng & Quy Chuẩn Biên Soạn Đề Toán THPT (Chuẩn THPT 2026 & Công Văn 7991/BGDĐT-GDTrH)

Tài liệu này cung cấp hướng dẫn vận hành chi tiết và các nguyên tắc chuẩn mực sư phạm để biên soạn, kiểm định và xuất bản đề thi môn Toán chuẩn Chương trình GDPT 2018 theo hai định dạng trọng tâm nhất của Bộ Giáo dục & Đào tạo:
1. **Đề thi Tốt nghiệp THPT từ năm 2025 – 2026** (Cấu trúc 100% trắc nghiệm khách quan).
2. **Đề kiểm tra Định kỳ (Giữa kỳ, Cuối kỳ) theo Công văn số 7991/BGDĐT-GDTrH ngày 17/12/2024** (Kết hợp 70% Trắc nghiệm + 30% Tự luận, kèm Khung Ma trận Phụ lục 1 & Bản đặc tả Phụ lục 2, áp dụng từ Học kỳ II năm học 2024 – 2025).

---

## 📑 Mục lục
1. [Khởi chạy & Cài đặt Ứng dụng](#1-khởi-chạy--cài-đặt-ứng-dụng)
2. [Cấu trúc Đề Kiểm tra Định kỳ theo Công văn 7991/BGDĐT-GDTrH](#2-cấu-trúc-đề-kiểm-tra-định-kỳ-theo-công-văn-7991bgdđt-gdtrh)
3. [Cấu trúc Đề thi Chuẩn Tốt nghiệp THPT 2026](#3-cấu-trúc-đề-thi-chuẩn-tốt-nghiệp-thpt-2026)
4. [Quy trình Thao tác trên Giao diện Web](#4-quy-trình-thao-tác-trên-giao-diện-web)
5. [Quy chuẩn Định dạng Công thức & Hình vẽ](#5-quy-chuẩn-định-dạng-công-thức--hình-vẽ)
6. [Quy trình Kiểm định Tính Đúng đắn Toán học](#6-quy-trình-kiểm-định-tính-đúng-đắn-toán-học)
7. [Xuất bản Microsoft Word (.docx) & Trộn Mã Đề Đảo](#7-xuất-bản-microsoft-word-docx--trộn-mã-đề-đảo)

---

## 1. Khởi chạy & Cài đặt Ứng dụng

### Cách 1: Khởi động Nhanh 1-Click trên Windows (Khuyến nghị)
- **Bước 1 - Cài đặt tự động:** Nhấp đúp vào file `install.bat`. Script sẽ tự động:
  - Kiểm tra môi trường Python 3.10+.
  - Khởi tạo môi trường ảo `venv`.
  - Cài đặt đầy đủ các gói phụ thuộc từ `requirements.txt`.
  - Tạo các thư mục làm việc cần thiết (`input/`, `output/history/`, `output/images/`...).
- **Bước 2 - Khởi chạy:** Nhấp đúp vào file `run_app.bat`. Giao diện Web sẽ tự động mở tại: `http://localhost:8080`.
- **Bước 3 - Dừng hệ thống:** Khi kết thúc phiên làm việc, nhấp đúp vào `stop_app.bat` để đóng tiến trình an toàn và giải phóng cổng kết nối.

### Cách 2: Khởi chạy Thủ công qua Dòng lệnh (Windows / macOS / Linux)
```bash
# 1. Tạo môi trường ảo
python -m venv venv

# 2. Kích hoạt môi trường ảo:
# Trên Windows:
venv\Scripts\activate
# Trên Linux/macOS:
source venv/bin/activate

# 3. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 4. Khởi chạy ứng dụng
python app.py
```

---

## 2. Cấu trúc Đề Kiểm tra Định kỳ theo Công văn 7991/BGDĐT-GDTrH

**Công văn số 7991/BGDĐT-GDTrH** do Bộ GD&ĐT ban hành ngày **17/12/2024** hướng dẫn thực hiện kiểm tra, đánh giá định kỳ đối với cấp THCS và THPT theo Thông tư số 22/2021/TT-BGDĐT, chính thức áp dụng từ **Học kỳ II năm học 2024 – 2025**.

### 2.1. Bộ Hồ sơ Khảo thí Bắt buộc
Mỗi đề kiểm tra định kỳ (Giữa kỳ, Cuối kỳ) môn Toán phải bảo đảm sự khớp đúng 100% giữa 4 thành phần:
1. **Phụ lục 1: Khung Ma trận đề kiểm tra định kì**
2. **Phụ lục 2: Bản đặc tả đề kiểm tra định kì**
3. **Đề kiểm tra định kì**
4. **Hướng dẫn chấm và biểu điểm chi tiết**

### 2.2. Bảng Phân Bổ Cấu Trúc Đề Môn Toán (70% Trắc nghiệm + 30% Tự luận)
- **Thời gian làm bài:** 90 phút (hoặc 60 phút tùy cấp độ giữa kỳ).
- **Tổng điểm:** 10,00 điểm.

| Phần | Dạng thức câu hỏi | Số câu / bài | Điểm tối đa | Quy cách & Thang điểm |
| :--- | :--- | :---: | :---: | :--- |
| **PHẦN I** | Trắc nghiệm Nhiều lựa chọn | 12 câu | **3.00 đ** | Chọn 1 phương án đúng trong 4 phương án (A, B, C, D). **0.25 đ / câu**. Tập trung mức độ *Biết* và *Hiểu*. |
| **PHẦN II** | Trắc nghiệm Đúng / Sai | 2 câu | **2.00 đ** | Mỗi câu là bài toán hoàn chỉnh tích hợp 4 mệnh đề $a), b), c), d)$ theo thang bậc tư duy. Điểm lũy tiến: Đúng 1 ý = **0.10 đ**; Đúng 2 ý = **0.25 đ**; Đúng 3 ý = **0.50 đ**; Đúng 4 ý = **1.00 đ**. |
| **PHẦN III** | Trắc nghiệm Trả lời ngắn | 4 câu | **2.00 đ** | Thí sinh tự tính toán và điền đáp số dạng số. **0.50 đ / câu**. Tập trung mức độ *Hiểu* và *Vận dụng*. |
| **PHẦN IV** | Tự luận | 2 bài | **3.00 đ** | Trình bày các bước biến đổi chi tiết, lập luận logic, mô hình hóa toán học và giải quyết tình huống thực tế. Mỗi bài **1.50 đ** (hoặc 1.0 đ + 2.0 đ). |

### 2.3. Tỉ lệ Phân Bổ Mức Độ Nhận Thức Chuẩn
- **Biết (Nhận biết):** Khoảng 40% (4.0 điểm).
- **Hiểu (Thông hiểu):** Khoảng 30% (3.0 điểm).
- **Vận dụng:** Khoảng 30% (3.0 điểm) (bao gồm cả Vận dụng và Vận dụng phát triển năng lực).

---

## 3. Cấu trúc Đề thi Chuẩn Tốt nghiệp THPT 2026

Đề thi môn Toán Tốt nghiệp THPT theo định hướng GDPT 2018 được chuẩn hóa **100% trắc nghiệm khách quan**, gồm **22 câu hỏi**, thời gian làm bài **90 phút**, tổng điểm **10.00 điểm**:

| Phần | Dạng thức câu hỏi | Số câu | Điểm tối đa | Quy cách & Thang điểm |
| :--- | :--- | :---: | :---: | :--- |
| **PHẦN I** | Trắc nghiệm 4 lựa chọn (A, B, C, D) | 12 câu | **3.00 đ** | Chọn 1 phương án đúng duy nhất. **0.25 đ / câu**. Đánh giá mức độ *Nhận biết* và *Thông hiểu*. |
| **PHẦN II** | Trắc nghiệm Đúng / Sai | 4 câu | **4.00 đ** | 4 câu lớn $\times$ 4 mệnh đề = 16 lệnh hỏi. Điểm lũy tiến: Đúng 1 ý = **0.10 đ**; Đúng 2 ý = **0.25 đ**; Đúng 3 ý = **0.50 đ**; Đúng cả 4 ý = **1.00 đ**. Phân hóa năng lực giải toán toàn diện. |
| **PHẦN III** | Trắc nghiệm Trả lời ngắn | 6 câu | **3.00 đ** | Thí sinh tự tính toán và điền đáp số vào phiếu trả lời. **0.50 đ / câu**. Yêu cầu kết quả là số nguyên hoặc thập phân tối đa 4 ký tự số. |

---

## 4. Quy trình Thao tác trên Giao diện Web

### 4.1. Thiết lập Ma trận & Sinh đề Tự động
1. Tại cột trái **Thiết lập Ma trận & Đề thi**, xem tổng quan ma trận hiện thời (số câu, số điểm, phân bố theo từng chuyên đề).
2. Nhấn **📋 Quản lý Danh sách Ma trận Đề thi** để chọn:
   - Các mẫu **Chuẩn Công văn 7991/BGDĐT-GDTrH** (Giữa kỳ II, Cuối kỳ II gồm 70% TN + 30% TL).
   - Hoặc mẫu **Chuẩn Tốt nghiệp THPT 2026** (100% Trắc nghiệm).
3. Nhấn **🚀 Tạo Đề Theo Ma Trận Này & Kiểm Định**. Hệ thống sẽ tự động tổng hợp bài toán, kiểm tra tính đúng đắn và hiển thị ngay trên không gian làm việc.

### 4.2. Nhân bản Câu hỏi từ Ảnh mẫu
1. Chọn tab **📸 Từ Ảnh mẫu** ở cột trái.
2. Tải ảnh chụp câu hỏi toán học (định dạng `.png`, `.jpg`, `.jpeg`).
3. Chọn số lượng câu tương tự cần nhân bản (từ 1 đến 15 câu) và kiểu biến đổi (Thay số liệu nghiệm đẹp, Đổi hàm số tương đương, Nâng lên Vận dụng cao).
4. Bấm **🚀 Nhân bản & Kiểm Định**.

### 4.3. Tinh chỉnh Câu hỏi Trực tiếp
Trên mỗi thẻ câu hỏi hiển thị tại không gian làm việc, bạn có các công cụ can thiệp linh hoạt:
- **🎲 Đổi số mới (1-Click):** Tự động sinh bộ số liệu mới cho riêng câu hỏi đó, bảo đảm nghiệm đẹp và tính lại lời giải chi tiết.
- **🤖 AI Sửa câu này:** Mở bảng tùy chọn nâng cao để gắn bài toán thực tế, chuyển thành nhận dạng đồ thị/hình vẽ, sửa phương án nhiễu hoặc nhập yêu cầu tự do.
- **✏️ Sửa tay (Live Preview):** Mở trình soạn thảo Markdown/LaTeX hai cột song song để giáo viên chỉnh sửa trực tiếp từng ký tự và xem trước công thức toán học thời gian thực.
- **📘 Xem/Ẩn lời giải:** Xem đáp án và các bước biến đổi chi tiết đã được thẩm định.

---

## 5. Quy chuẩn Định dạng Công thức & Hình vẽ

### 5.1. Quy chuẩn Công thức Toán học LaTeX
- Tất cả biến số, biểu thức, phương trình, hệ số phải đặt trong cặp dấu đô la `$...$`.
  - ✅ Chuẩn: `Hàm số $y = x^3 - 3x + 2$ đồng biến trên khoảng nào?`
  - ❌ Không chuẩn: `Hàm số y = x^3 - 3x + 2 đồng biến trên khoảng nào?`
- Đối với công thức đặt riêng dòng, sử dụng cặp dấu `$$...$$`.
- Ký hiệu góc, vectơ, tích phân, ma trận cần sử dụng lệnh LaTeX chuẩn: `\vec{u}`, `\int_{0}^{1}`, `\widehat{ABC}`.

### 5.2. Quy chuẩn Hình vẽ Sư phạm
- Khi câu hỏi yêu cầu đồ thị hàm số hoặc hình học không gian, hệ thống tự động gọi thư viện `math_draw.py` để tạo ảnh chất lượng cao vào thư mục `output/images/ten_hinh.png`.
- Quy chuẩn đồ thị:
  - Hiển thị rõ các trục tọa độ $Ox$, $Oy$, gốc $O$, các điểm cực trị, giao điểm và tiệm cận.
- Quy chuẩn hình không gian:
  - Nét thấy vẽ bằng nét liền (`solid`), nét khuất vẽ bằng nét đứt (`dashed`).
  - Gắn nhãn đỉnh rõ ràng, ký hiệu góc vuông và đường cao chuẩn xác.
- Nhúng vào đề thi thông qua cú pháp Markdown:
  ```markdown
  ![Đồ thị hàm số bậc ba](output/images/do_thi_cau_1.png)
  ```

---

## 6. Quy trình Kiểm định Tính Đúng đắn Toán học

Nhằm đảm bảo **100% đề thi không có lỗi sai sót**, hệ thống tích hợp quy trình thẩm định hình thức độc lập:
1. Mỗi khi câu hỏi được tạo hoặc sửa đổi, một mã kiểm tra (`verify_single.py` hoặc `verify_math.py`) được thiết lập để giải bài toán bằng thuật toán đại số máy tính.
2. Quy trình kiểm tra bao gồm:
   - Tính nghiệm chính xác và kiểm tra tính duy nhất của đáp án đúng.
   - Thẩm định độc lập tính đúng/sai của cả 4 mệnh đề trong Phần II.
   - Kiểm tra các phương án nhiễu (distractors) để tránh trùng lặp đáp án.
   - Xác thực số liệu bài toán thực tế không rơi vào trường hợp phi thực tế.
3. Giáo viên có thể bấm nút **📐 Kiểm định Toán** trên thanh tiêu đề để mở trình biên tập mã kiểm tra và chạy thẩm định thủ công bất cứ lúc nào.

---

## 7. Xuất bản Microsoft Word (.docx) & Trộn Mã Đề Đảo

Khi bấm nút **📄 Xuất file Word (.docx)** tại thanh công cụ đề thi:
1. **Chuẩn công thức Native Word Equation (OMML):**
   - Công thức toán học không bị chuyển đổi thành ảnh mờ, mà chuyển thẳng thành đối tượng Equation gốc của Microsoft Word (`OMML`).
   - Giáo viên có thể nhấp đúp vào công thức trên Microsoft Word để chỉnh sửa dễ dàng.
2. **Trộn đề tự động:**
   - Hệ thống tự động sinh nhiều mã đề đảo (101, 102, 103, 104...) theo nguyên tắc hoán vị ngẫu nhiên phương án và thứ tự câu hỏi nhưng bảo đảm độ khó tương đương.
3. **Bảng đáp án & Ma trận:**
   - Đi kèm mỗi đề xuất bản là phiếu soi đáp án nhanh cho toàn bộ các mã đề và bảng ma trận đặc tả chi tiết.

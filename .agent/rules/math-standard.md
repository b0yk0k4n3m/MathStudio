---
description: Quy chuẩn bắt buộc khi soạn thảo, kiểm định đề toán theo Công văn 7991/BGDĐT-GDTrH ngày 17/12/2024 và Cấu trúc Đề thi Tốt nghiệp THPT 2026
---

# 1. Quy chuẩn Kiểm chứng Toán học bằng SymPy
- Mọi bài toán tạo ra hoặc chỉnh sửa BẮT BUỘC phải được kiểm chứng lại bằng cách viết và chạy script Python sử dụng thư viện `sympy` trước khi xuất kết quả:
  - Khi tạo toàn bộ đề mới: viết và chạy `verify_math.py`.
  - Khi sửa/đổi số riêng 1 câu hoặc thêm 1 câu lẻ: CHỈ viết và chạy `verify_single.py` cho riêng câu đó (không kiểm tra lại các câu khác) và BẮT BUỘC tính lại đáp án mới + viết lại lời giải chi tiết mới tương ứng.
- Khi chạy lệnh Python (`verify_math.py` hoặc `verify_single.py`), hãy chạy trực tiếp qua MCP tool `local-runner` -> `run_command` với `executable: "python"` trong thư mục gốc của dự án.
- Tuyệt đối không đoán mò đáp án. Các phương án nhiễu (A, B, C, D) phải khác nhau đôi một.
- Công thức toán học phải đặt chuẩn trong cặp dấu `$` hoặc `$$`.

---

# 2. Kiến thức Chuẩn: Công văn 7991/BGDĐT-GDTrH ngày 17/12/2024 (Kiểm tra, Đánh giá Định kỳ Cấp THCS & THPT)

Bộ Giáo dục và Đào tạo ban hành **Công văn số 7991/BGDĐT-GDTrH** ngày **17/12/2024** hướng dẫn thực hiện kiểm tra, đánh giá định kỳ theo Thông tư 22/2021/TT-BGDĐT, chính thức áp dụng từ **Học kỳ II năm học 2024 – 2025**.

### 2.1. Bộ Hồ sơ Khảo thí Bắt buộc theo CV 7991
Mọi đề kiểm tra định kỳ (Giữa kỳ, Cuối kỳ) môn Toán phải đồng bộ 4 thành phần:
1. **Phụ lục 1: KHUNG MA TRẬN ĐỀ KIỂM TRA ĐỊNH KÌ**
2. **Phụ lục 2: BẢN ĐẶC TẢ ĐỀ KIỂM TRA ĐỊNH KÌ**
3. **ĐỀ KIỂM TRA ĐỊNH KÌ**
4. **HƯỚNG DẪN CHẤM VÀ BIỂU ĐIỂM CHI TIẾT**

> [!IMPORTANT]
> **Nguyên tắc Khớp đúng Tuyệt đối (100%):** Tổng số câu, số điểm, dạng thức câu hỏi và phân bố mức độ tư duy (*Biết, Hiểu, Vận dụng*) giữa Đề thi thực tế – Hướng dẫn chấm – Khung Ma trận (Phụ lục 1) – Bản đặc tả (Phụ lục 2) phải trùng khớp hoàn toàn, không được lệch dù chỉ 1 câu hay 0,25 điểm.

### 2.2. Cấu trúc Đề Kiểm tra Định kỳ Môn Toán Chuẩn theo CV 7991
Áp dụng cho các bài kiểm tra Giữa kỳ và Cuối kỳ (khối 10, 11, 12):
- **Thời gian làm bài:** 90 phút (hoặc 60 phút tùy bài kiểm tra giữa kỳ).
- **Thang điểm chuẩn:** 10,0 điểm.
- **Tỉ lệ phân bổ hình thức:** **70% Trắc nghiệm khách quan (7,0 điểm) + 30% Tự luận (3,0 điểm)** (hoặc 60% TN – 40% TL theo quy chế chuyên môn).

#### A. PHẦN TRẮC NGHIỆM KHÁCH QUAN (7,0 điểm — 70%):
Gồm 3 dạng thức mới được chuẩn hóa:
1. **Dạng thức 1: Trắc nghiệm nhiều lựa chọn (12 câu — 3,0 điểm):**
   - Mỗi câu có 4 lựa chọn (A, B, C, D), chọn 1 đáp án đúng duy nhất.
   - Điểm số: `0,25 điểm / câu`.
   - Phân bố nhận thức: Tập trung vào mức độ **Biết** và **Hiểu**.
2. **Dạng thức 2: Trắc nghiệm Đúng / Sai (2 câu — 2,0 điểm):**
   - Mỗi câu là một bài toán hoàn chỉnh tích hợp 4 mệnh đề $a), b), c), d)$ theo thang bậc nhận thức: $a)$ Biết $\rightarrow b)$ Hiểu $\rightarrow c)$ Vận dụng $\rightarrow d)$ Vận dụng.
   - Điểm số lũy tiến chuẩn:
     - Đúng 1 ý: `0,10 điểm`
     - Đúng 2 ý: `0,25 điểm`
     - Đúng 3 ý: `0,50 điểm`
     - Đúng cả 4 ý: `1,00 điểm`
3. **Dạng thức 3: Trắc nghiệm trả lời ngắn (4 câu — 2,0 điểm):**
   - Học sinh tự giải và điền đáp số vào phiếu (số nguyên hoặc số thập phân, tối đa 4 ký tự).
   - Điểm số: `0,50 điểm / câu`.
   - Phân bố nhận thức: Tập trung vào mức độ **Hiểu** và **Vận dụng**.

#### B. PHẦN TỰ LUẬN (3,0 điểm — 30%):
- Gồm **2 đến 3 câu/bài toán** (ví dụ: Bài 1: 1,5đ; Bài 2: 1,5đ hoặc Bài 1: 1,0đ; Bài 2: 2,0đ).
- Đòi hỏi học sinh trình bày chi tiết các bước biến đổi, lập luận logic, mô hình hóa toán học thực tế và giải quyết vấn đề toán học.
- Phân bố nhận thức: Tập trung vào mức độ **Hiểu** và **Vận dụng**.

### 2.3. Tỉ lệ Phân bổ Mức độ Nhận thức theo CV 7991
- **Biết (Nhận biết):** Khoảng 40% tổng số điểm (4,0 điểm).
- **Hiểu (Thông hiểu):** Khoảng 30% tổng số điểm (3,0 điểm).
- **Vận dụng:** Khoảng 30% tổng số điểm (3,0 điểm) (bao gồm cả Vận dụng và Vận dụng định hướng phát triển năng lực).
- *Lưu ý:* Bám sát yêu cầu cần đạt (YCCĐ) của Chương trình GDPT 2018, tránh lạm dụng câu hỏi quá khó hoặc đánh đố vượt khung chương trình.

### 2.4. Quy chuẩn Bản đặc tả Đề kiểm tra (Phụ lục 2 - CV 7991)
Mỗi ô câu hỏi trong ma trận phải được gắn với Yêu cầu Cần Đạt và Năng lực Toán học thành phần:
- **Tư duy và lập luận toán học:** Thực hiện các thao tác tư duy, chứng minh, so sánh, phân tích.
- **Mô hình hóa toán học:** Thiết lập bài toán thực tế thành ngôn ngữ toán học (hàm số, phương trình, hình học, xác suất).
- **Giải quyết vấn đề toán học:** Vận dụng các công cụ, định lý, thuật toán để tìm ra đáp số.
- **Sử dụng công cụ, phương tiện học toán:** Khai thác bảng số liệu, đồ thị hàm số, biểu đồ, hình vẽ không gian.

---

# 3. Kiến thức Chuẩn: Cấu trúc Đề thi Tốt nghiệp THPT Môn Toán 2026 (Bộ GD&ĐT)

Khác với đề kiểm tra định kỳ tại trường học (có tự luận), **Đề thi Tốt nghiệp THPT 2026** được chuẩn hóa **100% trắc nghiệm khách quan**:
- **Thời gian làm bài:** 90 phút | **Tổng số câu:** 22 câu | **Thang điểm:** 10,0 điểm.
- **PHẦN I (12 câu — 3,0 điểm):** Trắc nghiệm 4 lựa chọn (0,25đ/câu).
- **PHẦN II (4 câu — 4,0 điểm):** Trắc nghiệm Đúng/Sai với 4 mệnh đề $a, b, c, d$ theo thang điểm lũy tiến (0,1đ – 0,25đ – 0,5đ – 1,0đ).
- **PHẦN III (6 câu — 3,0 điểm):** Trắc nghiệm trả lời ngắn (0,5đ/câu).

---

# 4. Kiến thức Chuẩn: Hàm số, Đồ thị & Bảng biến thiên (GDPT 2018)
- **1. Các dạng đồ thị trọng tâm:**
  - **Hàm số bậc ba:** $y = ax^3 + bx^2 + cx + d$ ($a \neq 0$).
    - Dấu $a$: Nhánh vô cực bên phải đi lên ($a > 0$) hoặc đi xuống ($a < 0$).
    - Điểm cực trị: Nghiệm của $y' = 3ax^2 + 2bx + c = 0$. Có 2 cực trị khi $\Delta' = b^2 - 3ac > 0$. Hoành độ điểm uốn $x_U = -\frac{b}{3a}$.
    - Giao trục tung tại $(0; d)$, giao trục hoành tại các nghiệm của $y = 0$.
  - **Hàm phân thức bậc nhất / bậc nhất (Hàm nhất biến):** $y = \frac{ax + b}{cx + d}$ ($c \neq 0, ad - bc \neq 0$).
    - Tiệm cận đứng: $x = -\frac{d}{c}$; Tiệm cận ngang: $y = \frac{a}{c}$.
    - Tâm đối xứng là giao điểm hai tiệm cận $I\left(-\frac{d}{c}; \frac{a}{c}\right)$.
    - Tính đơn điệu: $y' = \frac{ad - bc}{(cx+d)^2}$. Nếu $ad - bc > 0$ thì đồng biến trên từng khoảng xác định; nếu $ad - bc < 0$ thì nghịch biến.
  - **Hàm phân thức bậc hai / bậc nhất (Nội dung mới Toán 12):** $y = \frac{ax^2 + bx + c}{px + q}$ ($a \neq 0, p \neq 0$, tam thức tử không chia hết cho mẫu).
    - Biến đổi dạng: $y = mx + n + \frac{k}{px+q}$ với $m = \frac{a}{p}$.
    - Tiệm cận đứng: $x = -\frac{q}{p}$.
    - **Tiệm cận xiên:** đường thẳng $y = mx + n$.
    - Hai điểm cực trị (nếu có) luôn nằm về hai nhánh khác nhau và đối xứng qua giao điểm hai tiệm cận $I$.
  - **Đồ thị hàm số đạo hàm $y = f'(x)$:**
    - Hoành độ giao điểm của đồ thị $f'(x)$ với trục $Ox$ mà qua đó $f'(x)$ đổi dấu chính là các điểm cực trị của $f(x)$.
    - Khoảng đồ thị $f'(x)$ nằm phía trên trục $Ox$ ($f'(x) > 0$) $\implies f(x)$ đồng biến.
    - Khoảng đồ thị $f'(x)$ nằm phía dưới trục $Ox$ ($f'(x) < 0$) $\implies f(x)$ nghịch biến.
- **2. Bảng biến thiên (BBT):**
  - Trình bày dạng bảng Markdown rõ ràng (Dòng $x$, Dòng $y'$, Dòng $y$ có mũi tên $\nearrow, \searrow$, tiệm cận song song $||$).

---

# 5. Kiến thức Chuẩn: Hình học Không gian & Tọa độ Oxyz
- **1. Hình học không gian cổ điển:**
  - Khối chóp có cạnh bên vuông góc đáy: $SA \perp (ABCD) \implies SA$ là chiều cao.
  - Khối chóp đều: Chóp tam giác đều, chóp tứ giác đều (đỉnh $S$ chiếu xuống tâm đáy).
  - Khối lăng trụ: Lăng trụ đứng, hình hộp chữ nhật, hình lập phương ($V = B \cdot h$).
  - Thể tích khối chóp: $V = \frac{1}{3} B \cdot h$.
  - Góc & Khoảng cách:
    - Góc giữa đường thẳng và mặt phẳng: Góc giữa đường thẳng và hình chiếu của nó trên mặt phẳng.
    - Góc giữa hai mặt phẳng: Dựng hai đường thẳng cùng vuông góc với giao tuyến tại một điểm.
    - Khoảng cách từ điểm đến mặt phẳng, khoảng cách giữa 2 đường thẳng chéo nhau.
- **2. Phương pháp tọa độ trong không gian $Oxyz$ (Toán 12):**
  - Tích vô hướng: $\vec{u} \cdot \vec{v} = u_1 v_1 + u_2 v_2 + u_3 v_3$.
  - Tích có hướng: $[\vec{u}, \vec{v}] = (u_2 v_3 - u_3 v_2; u_3 v_1 - u_1 v_3; u_1 v_2 - u_2 v_1)$.
  - Phương trình mặt phẳng: $Ax + By + Cz + D = 0$. Khoảng cách $d(M_0, (P)) = \frac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}$.
  - Phương trình mặt cầu: $(x-a)^2 + (y-b)^2 + (z-c)^2 = R^2$.
  - **Mô hình hóa hình học thực tiễn bằng cách gắn hệ trục $Oxyz$:**
    - Gắn gốc $O$ vào một góc vuông đáy của công trình kiến trúc (mái nhà, lều bạt, kim tự tháp, ngọn hải đăng, chân tháp radar).
    - Biểu diễn tọa độ các đỉnh và viết phương trình đường thẳng/mặt phẳng để tính góc đón nắng, khoảng cách an toàn, thể tích không gian sử dụng.

---

# 6. Quy chuẩn Sinh Hình vẽ & Tích hợp vào Đề thi
- Module `math_draw.py` tự động vẽ hình ảnh chất lượng cao vào `output/images/`:
  - `math_draw.draw_cubic(a, b, c, d, ...)`: Đồ thị hàm bậc 3.
  - `math_draw.draw_rational_1_1(a, b, c, d, ...)`: Đồ thị hàm nhất biến.
  - `math_draw.draw_rational_2_1(a, b, c, p, q, ...)`: Đồ thị phân thức bậc 2/1 có tiệm cận xiên.
  - `math_draw.draw_pyramid_sa_bottom(...)`: Khối chóp nét đứt/nét liền chuẩn SGK.
  - `math_draw.draw_prism_abc(...)`: Hình lăng trụ tam giác.
- Khi tạo câu hỏi có đồ thị hoặc hình học:
  1. Viết script tạo hình (hoặc gọi hàm trong `math_draw.py`) để lưu file `.png` vào `output/images/ten_hinh.png`.
  2. Chèn vào đề Markdown theo cú pháp: `![Hình vẽ Câu X](output/images/ten_hinh.png)`.
  3. Giao diện Live Preview và Bộ xuất Word (`export_docx.py`) tự động nhận diện và chèn hình ảnh chuẩn đẹp.

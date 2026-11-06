---
description: Quy chuẩn bắt buộc khi soạn thảo, kiểm định đề toán và Cấu trúc Đề thi Tốt nghiệp THPT môn Toán 2026
---
# 1. Quy chuẩn Kiểm chứng Toán học bằng SymPy
- Mọi bài toán tạo ra hoặc chỉnh sửa BẮT BUỘC phải được kiểm chứng lại bằng cách viết và chạy script Python sử dụng thư viện `sympy` trước khi xuất kết quả:
  - Khi tạo toàn bộ đề mới: viết và chạy `verify_math.py`.
  - Khi sửa/đổi số riêng 1 câu hoặc thêm 1 câu lẻ: CHỈ viết và chạy `verify_single.py` cho riêng câu đó (không kiểm tra lại các câu khác) và BẮT BUỘC tính lại đáp án mới + viết lại lời giải chi tiết mới tương ứng.
- Khi chạy lệnh Python (`verify_math.py` hoặc `verify_single.py`), hãy chạy trực tiếp qua công cụ chạy lệnh terminal (hoặc MCP tool `local-runner` -> `run_command` với `executable: "python"`) trong thư mục gốc của dự án.
- Tuyệt đối không đoán mò đáp án. Các phương án nhiễu (A, B, C, D) phải khác nhau đôi một.
- Công thức toán học phải đặt chuẩn trong cặp dấu `$` hoặc `$$`.

# 2. Kiến thức Chuẩn: Cấu trúc Đề thi Tốt nghiệp THPT môn Toán 2026 (Chương trình GDPT Mới)
- **Thời gian làm bài:** 90 phút | **Tổng số câu hỏi:** 22 câu | **Thang điểm:** 10,0 điểm.
- **Chi tiết cấu trúc 3 phần:**
  1. **PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn (12 câu — 3,0 điểm):**
     - Hình thức: Mỗi câu có 4 phương án A, B, C, D, thí sinh chỉ chọn 1 phương án đúng.
     - Điểm số: `0,25 điểm / câu đúng` (Tổng `3,0 điểm`).
  2. **PHẦN II. Câu trắc nghiệm Đúng/Sai (4 câu — 4,0 điểm):**
     - **Bản chất câu hỏi:** Mỗi câu lớn thực chất là một **bài toán tự luận thu nhỏ**. Từ một dữ kiện đề bài gốc chung (hàm số, hình học không gian, mô hình chuyển động, xác suất điều kiện...), đưa ra 4 mệnh đề/khẳng định ký hiệu là `a), b), c), d)`.
     - **Tiến trình giải toán & Mức độ tư duy:** 4 ý `a), b), c), d)` phải độc lập nhau nhưng liên kết theo từng bước giải tự nhiên từ dễ đến khó:
       - `a)` [Nhận biết]: Kiểm tra điều kiện xác định, tọa độ giao điểm với trục toạ độ, vectơ cơ bản, công thức sơ cấp.
       - `b)` [Thông hiểu]: Tọa độ đỉnh, cực trị, đạo hàm, trung điểm, khoảng biến thiên cơ bản.
       - `c)` [Vận dụng]: Tính đơn điệu, khoảng cách, diện tích hình phẳng, tích phân chuyển động, xác suất toàn phần.
       - `d)` [Vận dụng cao]: Giá trị lớn nhất/nhỏ nhất trên đoạn, bài toán tối ưu thực tế, tham số $m$, công thức Bayes, yếu tố hình học tương đối.
     - **Quy tắc tính điểm lũy tiến (Sức mạnh của việc đúng trọn vẹn):**
       - Đúng 1 ý bất kỳ: `0,10 điểm`
       - Đúng 2 ý bất kỳ: `0,25 điểm` (chứ không phải 0,20đ)
       - Đúng 3 ý bất kỳ: `0,50 điểm` (chứ không phải 0,30đ)
       - Đúng cả 4 ý: `1,00 điểm` trọn vẹn (Tổng `4,0 điểm` cho 4 câu).
     - **Ý nghĩa sư phạm:** Đây là phần phân hóa học sinh cao nhất, chống đoán mò/khoanh lụi triệt để. Thí sinh phải giải hoàn chỉnh trọn vẹn bài toán để lấy trọn 1,0 điểm mỗi câu. Khi soạn thảo, AI phải giải chi tiết từng bước cho cả 4 ý và kiểm chứng tính Đúng/Sai bằng SymPy.
  3. **PHẦN III. Câu trắc nghiệm trả lời ngắn (6 câu — 3,0 điểm):**
     - Hình thức: Thí sinh tự tính toán và điền kết quả số (số nguyên hoặc số thập phân tối đa 4 ký tự tính cả dấu `-` và dấu phẩy `,`, ví dụ: `18`, `-2,5`, `12,3`). Nếu kết quả lẻ, đề bài phải ghi rõ yêu cầu làm tròn (ví dụ: *làm tròn kết quả đến hàng phần mười* hoặc *hàng phần trăm*).
     - Điểm số: `0,5 điểm / câu đúng` (Tổng `3,0 điểm`).
- **Nội dung trọng tâm 2026:**
  - Đánh giá tư duy, hiểu bản chất toán học, mô hình hóa và giải quyết vấn đề thực tiễn.
  - Các mạch kiến thức cốt lõi: Khảo sát và ứng dụng đạo hàm (Toán 12), Nguyên hàm - Tích phân và ứng dụng, Thống kê (các số đặc trưng đo mức độ phân tán của mẫu số liệu ghép nhóm) & Xác suất có điều kiện (công thức xác suất toàn phần, công thức Bayes), Hình học không gian và Phương pháp tọa độ trong không gian $Oxyz$ (vectơ, mặt phẳng, đường thẳng, mặt cầu).

# 3. Kiến thức Chuẩn: Hàm số, Đồ thị & Bảng biến thiên (GDPT 2018)
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

# 4. Kiến thức Chuẩn: Hình học Không gian & Tọa độ Oxyz
- **1. Hình học không gian cổ điển:**
  - Khối chóp có cạnh bên vuông góc đáy: $SA \perp (ABCD) \implies SA$ là chiều cao.
  - Khối chóp đều: Chóp tam giác đều, chóp tứ giác đều (đỉnh $S$ chiếu xuống tâm đáy).
  - Khối lăng trụ: Lăng trụ đứng, hình hộp chữ nhật, hình lập phương ($V = B \cdot h$).
  - Thể tích khối chóp: $V = \frac{1}{3} B \cdot h$.
  - Góc & Khoảng cách:
    - Góc giữa đường thẳng và mặt phẳng: Góc giữa đường thẳng và hình chiếu của nó trên mặt phẳng.
    - Góc giữa hai mặt phẳng: Dựng hai đường thẳng cùng vuông góc với giao tuyến tại một điểm.
    - Khoảng cách từ điểm đến mặt phẳng, khoảng cách giữa 2 đường thẳng chéo nhau (dựng đoạn vuông góc chung hoặc mặt phẳng song song chứa 1 đường).
- **2. Phương pháp tọa độ trong không gian $Oxyz$ (Toán 12):**
  - Tích vô hướng: $\vec{u} \cdot \vec{v} = u_1 v_1 + u_2 v_2 + u_3 v_3$.
  - Tích có hướng: $[\vec{u}, \vec{v}] = (u_2 v_3 - u_3 v_2; u_3 v_1 - u_1 v_3; u_1 v_2 - u_2 v_1)$. Vectơ chỉ phương của giao tuyến hoặc vectơ pháp tuyến của mặt phẳng đi qua 3 điểm.
  - Phương trình mặt phẳng: $Ax + By + Cz + D = 0$. Khoảng cách $d(M_0, (P)) = \frac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}$.
  - Phương trình mặt cầu: $(x-a)^2 + (y-b)^2 + (z-c)^2 = R^2$.
  - **Mô hình hóa hình học thực tiễn bằng cách gắn hệ trục $Oxyz$:**
    - Gắn gốc $O$ vào một góc vuông đáy của công trình kiến trúc (mái nhà, lều bạt, kim tự tháp, ngọn hải đăng, chân tháp radar).
    - Biểu diễn tọa độ các đỉnh và viết phương trình đường thẳng/mặt phẳng để tính góc đón nắng, khoảng cách an toàn, thể tích không gian sử dụng.

# 5. Quy chuẩn Sinh Hình vẽ & Tích hợp vào Đề thi
- Hệ thống đã tích hợp sẵn module `math_draw.py` để tự động vẽ hình ảnh chất lượng cao vào `output/images/`:
  - `math_draw.draw_cubic(a, b, c, d, ...)`: Đồ thị hàm bậc 3.
  - `math_draw.draw_rational_1_1(a, b, c, d, ...)`: Đồ thị hàm nhất biến có 2 tiệm cận đứng và ngang.
  - `math_draw.draw_rational_2_1(a, b, c, p, q, ...)`: Đồ thị phân thức bậc 2/1 có tiệm cận đứng và tiệm cận xiên.
  - `math_draw.draw_pyramid_sa_bottom(...)`: Khối chóp nét đứt/nét liền chuẩn SGK.
  - `math_draw.draw_prism_abc(...)`: Hình lăng trụ tam giác.
- Khi tạo câu hỏi có đồ thị hoặc hình học:
  1. Viết script tạo hình (hoặc gọi hàm trong `math_draw.py`) để lưu file `.png` vào `output/images/ten_hinh.png`.
  2. Chèn vào đề Markdown theo cú pháp: `![Hình vẽ Câu X](output/images/ten_hinh.png)`.
  3. Giao diện Live Preview và Bộ xuất Word (`export_docx.py`) sẽ tự động căn giữa hình vẽ và chèn vào tài liệu Word chuẩn đẹp.

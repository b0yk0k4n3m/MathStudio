---
name: tao-de
description: Tự động đọc yêu cầu từ CURRENT_TASK.md, tạo đề toán chuẩn cấu trúc THPT 2026 hoặc Đề kiểm tra định kỳ chuẩn Công văn 7991/BGDĐT-GDTrH (kèm Ma trận & Bản đặc tả), chạy SymPy kiểm tra và xuất file vào output/.
---

# Quy trình Tạo & Kiểm định Đề Toán (`/tao-de`)

1. **Đọc yêu cầu:** Đọc nội dung yêu cầu chi tiết trong file `CURRENT_TASK.md` (và file ảnh trong `input/` nếu có). Xác định rõ định dạng đề:
   - **Định dạng A: Đề thi Tốt nghiệp THPT 2026 (Bộ GD&ĐT)**: 100% Trắc nghiệm khách quan (22 câu, 10.0đ, 90 phút).
   - **Định dạng B: Đề kiểm tra Định kỳ theo Công văn 7991/BGDĐT-GDTrH (17/12/2024)**: Kết hợp **70% Trắc nghiệm (7,0đ) + 30% Tự luận (3,0đ)**.

2. **Soạn thảo câu hỏi theo đúng cấu trúc chuẩn:**
   - **Phần I (Trắc nghiệm 4 lựa chọn):** 0,25 điểm/câu (12 câu = 3,0đ), tập trung mức độ Biết và Hiểu.
   - **Phần II (Trắc nghiệm Đúng/Sai):** Mỗi câu gồm 4 mệnh đề `a), b), c), d)` theo nấc thang tư duy (Biết $\rightarrow$ Hiểu $\rightarrow$ Vận dụng $\rightarrow$ Vận dụng). Điểm lũy tiến chuẩn: Đúng 1 ý = 0,1đ; Đúng 2 ý = 0,25đ; Đúng 3 ý = 0,5đ; Đúng cả 4 ý = 1,0đ. Bắt buộc kiểm chứng SymPy độc lập cả 4 ý.
     - Đề Tốt nghiệp THPT 2026: 4 câu (4,0đ).
     - Đề Kiểm tra Định kỳ CV 7991: 2 câu (2,0đ).
   - **Phần III (Trắc nghiệm trả lời ngắn):** 0,5 điểm/câu, đáp số là một con số rõ ràng (tối đa 4 ký tự khi tô phiếu).
     - Đề Tốt nghiệp THPT 2026: 6 câu (3,0đ).
     - Đề Kiểm tra Định kỳ CV 7991: 4 câu (2,0đ).
   - **Phần IV (Tự luận - Đề CV 7991):** 2 đến 3 bài toán (3,0đ), giải chi tiết các bước biến đổi, lập luận logic và mô hình hóa thực tế (mức độ Hiểu và Vận dụng).
   - Mỗi câu bắt đầu bằng tiêu đề `### Câu 1.`, `### Câu 2.`, ... và ngay bên dưới mỗi câu có dòng `**Lời giải:**`.

3. **Xử lý Đồ thị hàm số & Hình học không gian:**
   - Sử dụng thư viện `math_draw.py` (hoặc script Python Matplotlib) để tự động sinh file ảnh `.png` chất lượng cao vào `output/images/ten_hinh.png`.
   - Các dạng hình vẽ hỗ trợ: Đồ thị bậc ba (`draw_cubic`), hàm nhất biến (`draw_rational_1_1`), hàm phân thức bậc 2/1 có tiệm cận xiên (`draw_rational_2_1`), hình chóp vuông góc đáy (`draw_pyramid_sa_bottom`), lăng trụ tam giác (`draw_prism_abc`).
   - Nhúng hình ảnh trực tiếp vào đề bài: `![Đồ thị hàm số](output/images/ten_hinh.png)`.

4. **Kiểm chứng toán học bằng SymPy:**
   - Tạo file `verify_math.py` (hoặc `verify_single.py` nếu sửa 1 câu), sử dụng `sympy` để giải nghiệm chính xác và đối chiếu đáp án qua MCP tool `local-runner` -> `run_command` (`executable: "python"`).
   - Đảm bảo 100% không có câu nào bị trùng đáp án, nghiệm xấu hoặc sai số làm tròn khi chưa được quy định.

5. **Xuất bản đề thi hoàn chỉnh:**
   - Ghi nội dung đề kèm đáp án và lời giải chi tiết (chuẩn LaTeX `$...$`) ra file được chỉ định trong `output/`.
   - Đối với đề kiểm tra theo Công văn 7991, đảm bảo đồng bộ hoàn hảo với Khung Ma trận (Phụ lục 1) và Bản đặc tả (Phụ lục 2).

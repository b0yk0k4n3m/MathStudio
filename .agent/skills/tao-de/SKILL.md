---
name: tao-de
description: Tự động đọc yêu cầu từ CURRENT_TASK.md, tạo đề toán chuẩn cấu trúc THPT 2026 (hoặc theo ma trận), chạy SymPy kiểm tra và xuất file vào output/.
---

# Quy trình Tạo & Kiểm định Đề Toán (`/tao-de`)

1. Đọc nội dung yêu cầu chi tiết trong file `CURRENT_TASK.md` (và file ảnh trong `input/` nếu có).
2. Soạn thảo các câu hỏi toán học theo đúng cấu trúc yêu cầu và chuẩn chương trình THPT 2026:
   - **Phần I (Trắc nghiệm 4 lựa chọn):** 0,25 điểm/câu.
   - **Phần II (Trắc nghiệm Đúng/Sai):** Mỗi câu là một bài toán tự luận thu nhỏ gồm 4 mệnh đề `a), b), c), d)` sắp xếp theo nấc thang tư duy (Nhận biết -> Thông hiểu -> Vận dụng -> Vận dụng cao). Điểm lũy tiến đặc biệt: Đúng 1 ý = 0,1đ; Đúng 2 ý = 0,25đ; Đúng 3 ý = 0,5đ; Đúng cả 4 ý = 1,0đ trọn vẹn. Bắt buộc kiểm chứng SymPy độc lập cả 4 ý.
   - **Phần III (Trắc nghiệm trả lời ngắn):** 0,5 điểm/câu, đáp số là một con số rõ ràng (tối đa 4 ký tự khi tô phiếu; nếu cần làm tròn phải nêu rõ quy tắc làm tròn trong đề).
   - Mỗi câu bắt đầu bằng tiêu đề `### Câu 1.`, `### Câu 2.`, ... và ngay bên dưới mỗi câu có dòng `**Lời giải:**`.
3. Khi đề bài có câu hỏi về **Đồ thị hàm số** hoặc **Hình học không gian**:
   - Sử dụng thư viện `math_draw.py` (hoặc viết script Python với Matplotlib) để tự động sinh file ảnh `.png` chất lượng cao vào `output/images/ten_hinh.png`.
   - Các dạng hình vẽ hỗ trợ: Đồ thị bậc ba (`draw_cubic`), hàm nhất biến (`draw_rational_1_1`), hàm phân thức bậc 2/1 có tiệm cận xiên (`draw_rational_2_1`), hình chóp vuông góc đáy (`draw_pyramid_sa_bottom`), lăng trụ tam giác (`draw_prism_abc`).
   - Nhúng hình ảnh trực tiếp vào đề bài: `![Đồ thị hàm số](output/images/ten_hinh.png)`. Cả giao diện web NiceGUI và tính năng Xuất Word (.docx) sẽ tự động nhận diện và hiển thị hình ảnh chuẩn đẹp.
4. Tạo file `verify_math.py` (hoặc `verify_single.py` nếu chỉ sửa 1 câu) sử dụng `sympy` để giải kiểm chứng từng câu, gọi MCP `local-runner` -> `run_command` (`executable="python"`) để đối chiếu đáp án.
5. Nếu phát hiện câu nào nghiệm xấu hoặc trùng đáp án, tự động chỉnh sửa lại hệ số và chạy lại script SymPy.
6. Xuất đề thi hoàn chỉnh kèm lời giải chi tiết (dùng chuẩn LaTeX `$...$`) ra file được chỉ định.

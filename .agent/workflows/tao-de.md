---
description: Tự động đọc yêu cầu từ CURRENT_TASK.md, tạo đề toán chuẩn THPT 2026, chạy SymPy kiểm tra và xuất file
---
1. Đọc nội dung yêu cầu chi tiết trong file `CURRENT_TASK.md` (và file ảnh trong `input/` nếu có).
2. Soạn thảo các câu hỏi toán học theo đúng cấu trúc THPT 2026 (Phần I: 4 lựa chọn - 0,25đ/câu; Phần II: Đúng/Sai 4 ý a,b,c,d - lũy tiến 0,1/0,25/0,5/1,0đ; Phần III: Trả lời ngắn - 0,5đ/câu).
3. Nếu câu hỏi có Đồ thị hàm số hoặc Hình học không gian: Sử dụng `math_draw.py` để tự động vẽ hình `.png` vào `output/images/` và nhúng `![Hình minh họa](output/images/...)` vào đề thi.
4. Tạo file `verify_math.py` sử dụng `sympy` để giải từng câu và chạy `python verify_math.py` để đối chiếu đáp án.
5. Nếu phát hiện câu nào nghiệm xấu hoặc trùng đáp án, tự động chỉnh sửa lại hệ số và chạy lại `verify_math.py`.
6. Xuất đề thi hoàn chỉnh kèm lời giải chi tiết ra file được chỉ định trong `output/`.

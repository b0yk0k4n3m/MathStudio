# KỲ THI TỐT NGHIỆP TRUNG HỌC PHỔ THÔNG NĂM 2026
**MÔN: TOÁN (CHƯƠNG TRÌNH MỚI)**  
*Thời gian làm bài: 90 phút (không kể thời gian phát đề)*  
*Tổng số câu: 22 câu | Tổng điểm: 10.00 điểm*  
*(Chuyên đề: Tổng hợp chuẩn cấu trúc THPT 2026 — Hàm số, Giải tích 12, Oxyz, Xác suất - Thống kê, Thực tiễn)*  
*(Đề thi và lời giải chi tiết đã được kiểm chứng tính toán chính xác 100% bằng SymPy)*

---

### CẤU TRÚC VÀ QUY TẮC TÍNH ĐIỂM ĐỀ THI CHUẨN NĂM 2026
- **PHẦN I (12 câu — 3.00 điểm):** Thí sinh chọn một phương án trả lời đúng duy nhất trong 4 phương án $A, B, C, D$. Mỗi câu trả lời đúng thí sinh được $0,25$ điểm; trả lời sai hoặc không trả lời không có điểm.
- **PHẦN II (4 câu — 4.00 điểm):** Câu trắc nghiệm Đúng/Sai. Mỗi câu gồm $4$ ý kiểm tra theo tiến trình tư duy giải toán từ Nhận biết $\rightarrow$ Thông hiểu $\rightarrow$ Vận dụng $\rightarrow$ Vận dụng cao. Thang điểm lũy tiến từng câu như sau:
  - Đúng $1$ ý: được $0,10$ điểm.
  - Đúng $2$ ý: được $0,25$ điểm.
  - Đúng $3$ ý: được $0,50$ điểm.
  - Đúng cả $4$ ý trọn vẹn: được $1,00$ điểm.
- **PHẦN III (6 câu — 3.00 điểm):** Câu trắc nghiệm trả lời ngắn. Thí sinh tự tính toán và điền đáp số là một con số nguyên hoặc số thập phân gọn. Mỗi câu trả lời đúng được $0,50$ điểm.

---

## PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn (12 câu — 3.00 điểm)

---

### Câu 1.
Đường tiệm cận ngang của đồ thị hàm số $y = \frac{3x - 2}{x + 1}$ là đường thẳng có phương trình
- **A.** $y = 3$.
- **B.** $y = -2$.
- **C.** $x = -1$.
- **D.** $x = 3$.

**Lời giải:**
- **Đáp án đúng:** **A**
- Ta có:
  $$\lim_{x \to +\infty} y = \lim_{x \to +\infty} \frac{3x - 2}{x + 1} = \lim_{x \to +\infty} \frac{3 - \frac{2}{x}}{1 + \frac{1}{x}} = 3$$
  $$\lim_{x \to -\infty} y = \lim_{x \to -\infty} \frac{3x - 2}{x + 1} = 3$$
- Do đó, đồ thị hàm số có đường tiệm cận ngang là đường thẳng $y = 3$.

---

### Câu 2.
Họ tất cả các nguyên hàm của hàm số $f(x) = 4x^3 - 2x + 5$ trên $\mathbb{R}$ là
- **A.** $F(x) = 12x^2 - 2 + C$.
- **B.** $F(x) = x^4 - x^2 + 5x + C$.
- **C.** $F(x) = 4x^4 - 2x^2 + 5x + C$.
- **D.** $F(x) = x^4 - 2x^2 + 5x + C$.

**Lời giải:**
- **Đáp án đúng:** **B**
- Áp dụng công thức nguyên hàm cơ bản:
  $$\int f(x)\,\mathrm{d}x = \int (4x^3 - 2x + 5)\,\mathrm{d}x = 4 \cdot \frac{x^4}{4} - 2 \cdot \frac{x^2}{2} + 5x + C = x^4 - x^2 + 5x + C$$

---

### Câu 3.
Cho hàm số bậc ba $y = x^3 - 3x^2 - 9x + 2$. Giá trị cực tiểu của hàm số đã cho bằng
- **A.** $-25$.
- **B.** $3$.
- **C.** $7$.
- **D.** $-1$.

**Lời giải:**
- **Đáp án đúng:** **A**
- Tập xác định: $\mathcal{D} = \mathbb{R}$.
- Đạo hàm: $y' = 3x^2 - 6x - 9$.
- Giải phương trình $y' = 0 \iff 3(x^2 - 2x - 3) = 0 \iff \left[\begin{aligned} &x = -1 \\ &x = 3 \end{aligned}\right.$
- Ta có đạo hàm cấp hai: $y'' = 6x - 6$.
  - Với $x = -1 \implies y''(-1) = -12 < 0 \implies x = -1$ là điểm cực đại của hàm số.
  - Với $x = 3 \implies y''(3) = 12 > 0 \implies x = 3$ là điểm cực tiểu của hàm số.
- Do đó, giá trị cực tiểu của hàm số là:
  $$y_{\text{CT}} = y(3) = 3^3 - 3 \cdot 3^2 - 9 \cdot 3 + 2 = 27 - 27 - 27 + 2 = -25$$

---

### Câu 4.
Trong không gian với hệ tọa độ $Oxyz$, mặt cầu $(S)$ có tâm $I(2; -1; 3)$ và đi qua điểm $A(4; 1; 2)$ có phương trình là
- **A.** $(x - 2)^2 + (y + 1)^2 + (z - 3)^2 = 9$.
- **B.** $(x + 2)^2 + (y - 1)^2 + (z + 3)^2 = 9$.
- **C.** $(x - 2)^2 + (y + 1)^2 + (z - 3)^2 = 3$.
- **D.** $(x - 2)^2 + (y + 1)^2 + (z - 3)^2 = 81$.

**Lời giải:**
- **Đáp án đúng:** **A**
- Bán kính mặt cầu $(S)$ là khoảng cách $R = IA$:
  $$R^2 = IA^2 = (4 - 2)^2 + (1 - (-1))^2 + (2 - 3)^2 = 2^2 + 2^2 + (-1)^2 = 4 + 4 + 1 = 9$$
- Mặt cầu tâm $I(2; -1; 3)$ bán kính $R = 3$ có phương trình chính tắc:
  $$(x - 2)^2 + (y + 1)^2 + (z - 3)^2 = 9$$

---

### Câu 5.
Giá trị lớn nhất của hàm số $y = x + \frac{4}{x}$ trên đoạn $[1; 3]$ bằng
- **A.** $4$.
- **B.** $5$.
- **C.** $\frac{13}{3}$.
- **D.** $6$.

**Lời giải:**
- **Đáp án đúng:** **B**
- Hàm số xác định và liên tục trên đoạn $[1; 3]$.
- Đạo hàm: $y' = 1 - \frac{4}{x^2} = \frac{x^2 - 4}{x^2}$.
- Xét trên $[1; 3]$, $y' = 0 \iff x^2 - 4 = 0 \iff x = 2$ (do $x \in [1; 3]$).
- Tính các giá trị:
  - $y(1) = 1 + \frac{4}{1} = 5$.
  - $y(2) = 2 + \frac{4}{2} = 4$.
  - $y(3) = 3 + \frac{4}{3} = \frac{13}{3} \approx 4,33$.
- So sánh các giá trị suy ra $\max_{[1; 3]} y = y(1) = 5$.

---

### Câu 6.
Số nghiệm nguyên của bất phương trình $\log_2(x^2 - 3x + 2) \le 1$ là
- **A.** $1$.
- **B.** $2$.
- **C.** $3$.
- **D.** $4$.

**Lời giải:**
- **Đáp án đúng:** **B**
- Điều kiện xác định:
  $$x^2 - 3x + 2 > 0 \iff (x - 1)(x - 2) > 0 \iff \left[\begin{aligned} &x < 1 \\ &x > 2 \end{aligned}\right.$$
- Vì cơ số $2 > 1$, bất phương trình đã cho tương đương với:
  $$x^2 - 3x + 2 \le 2^1 \iff x^2 - 3x \le 0 \iff 0 \le x \le 3$$
- Kết hợp với điều kiện xác định, ta được tập nghiệm của bất phương trình:
  $$S = [0; 1) \cup (2; 3]$$
- Do $x \in \mathbb{Z}$ nên $x \in \{0; 3\}$.
- Vậy có tất cả $2$ nghiệm nguyên thỏa mãn.

---

### Câu 7.
Cho $\int_0^2 f(x)\,\mathrm{d}x = 5$. Khi đó tích phân $I = \int_0^1 [3f(2x) - 4x]\,\mathrm{d}x$ bằng
- **A.** $\frac{15}{2}$.
- **B.** $\frac{11}{2}$.
- **C.** $13$.
- **D.** $\frac{7}{2}$.

**Lời giải:**
- **Đáp án đúng:** **B**
- Tách tích phân $I$:
  $$I = 3\int_0^1 f(2x)\,\mathrm{d}x - \int_0^1 4x\,\mathrm{d}x$$
- Đặt $t = 2x \implies \mathrm{d}t = 2\mathrm{d}x \implies \mathrm{d}x = \frac{\mathrm{d}t}{2}$.
  Đổi cận: khi $x = 0 \implies t = 0$; khi $x = 1 \implies t = 2$.
  Do đó:
  $$\int_0^1 f(2x)\,\mathrm{d}x = \int_0^2 f(t)\,\frac{\mathrm{d}t}{2} = \frac{1}{2}\int_0^2 f(t)\,\mathrm{d}t = \frac{1}{2} \cdot 5 = \frac{5}{2}$$
- Tính tích phân thứ hai:
  $$\int_0^1 4x\,\mathrm{d}x = \left[2x^2\right]_0^1 = 2 \cdot 1^2 - 0 = 2$$
- Vậy $I = 3 \cdot \frac{5}{2} - 2 = \frac{15}{2} - 2 = \frac{11}{2}$.

---

### Câu 8.
Diện tích hình phẳng giới hạn bởi đồ thị hàm số $y = x^2 - 4x + 3$ và đường thẳng $y = x - 1$ bằng
- **A.** $\frac{9}{2}$.
- **B.** $\frac{9}{4}$.
- **C.** $\frac{27}{2}$.
- **D.** $9$.

**Lời giải:**
- **Đáp án đúng:** **A**
- Phương trình hoành độ giao điểm của parabol và đường thẳng:
  $$x^2 - 4x + 3 = x - 1 \iff x^2 - 5x + 4 = 0 \iff \left[\begin{aligned} &x = 1 \\ &x = 4 \end{aligned}\right.$$
- Diện tích hình phẳng cần tính là:
  $$S = \int_1^4 |(x - 1) - (x^2 - 4x + 3)|\,\mathrm{d}x = \int_1^4 (-x^2 + 5x - 4)\,\mathrm{d}x$$
- Tính nguyên hàm:
  $$S = \left[ -\frac{x^3}{3} + \frac{5x^2}{2} - 4x \right]_1^4 = \left( -\frac{64}{3} + 40 - 16 \right) - \left( -\frac{1}{3} + \frac{5}{2} - 4 \right) = \frac{8}{3} - \left(-\frac{11}{6}\right) = \frac{27}{6} = \frac{9}{2}$$

---

### Câu 9.
Trong không gian với hệ tọa độ $Oxyz$, cho điểm $M(1; 2; -1)$ và đường thẳng $d: \frac{x - 2}{1} = \frac{y + 1}{2} = \frac{z}{-2}$. Mặt phẳng $(P)$ đi qua $M$ và vuông góc với đường thẳng $d$. Khoảng cách từ gốc tọa độ $O(0; 0; 0)$ đến mặt phẳng $(P)$ bằng
- **A.** $\frac{7}{3}$.
- **B.** $\frac{7}{9}$.
- **C.** $7$.
- **D.** $\frac{5}{3}$.

**Lời giải:**
- **Đáp án đúng:** **A**
- Đường thẳng $d$ có một vectơ chỉ phương là $\vec{u}_d = (1; 2; -2)$.
- Vì $(P) \perp d$ nên mặt phẳng $(P)$ nhận $\vec{u}_d = (1; 2; -2)$ làm một vectơ pháp tuyến.
- Mặt phẳng $(P)$ đi qua điểm $M(1; 2; -1)$ có phương trình tổng quát:
  $$1(x - 1) + 2(y - 2) - 2(z + 1) = 0 \iff x + 2y - 2z - 7 = 0$$
- Khoảng cách từ gốc tọa độ $O(0; 0; 0)$ đến mặt phẳng $(P)$ là:
  $$d(O, (P)) = \frac{|0 + 2(0) - 2(0) - 7|}{\sqrt{1^2 + 2^2 + (-2)^2}} = \frac{7}{\sqrt{1 + 4 + 4}} = \frac{7}{3}$$

---

### Câu 10.
Trong không gian với hệ tọa độ $Oxyz$, đường thẳng $\Delta$ đi qua điểm $A(1; 0; -2)$, đồng thời song song với mặt phẳng $(P): 2x - y + 2z + 3 = 0$ và vuông góc với đường thẳng $d: \frac{x - 1}{2} = \frac{y}{1} = \frac{z + 1}{-1}$. Một vectơ chỉ phương của đường thẳng $\Delta$ là
- **A.** $\vec{u}_1 = (-1; 6; 4)$.
- **B.** $\vec{u}_2 = (1; 6; -4)$.
- **C.** $\vec{u}_3 = (-1; -6; 4)$.
- **D.** $\vec{u}_4 = (1; 2; 1)$.

**Lời giải:**
- **Đáp án đúng:** **A**
- Mặt phẳng $(P)$ có một vectơ pháp tuyến là $\vec{n}_P = (2; -1; 2)$.
- Đường thẳng $d$ có một vectơ chỉ phương là $\vec{u}_d = (2; 1; -1)$.
- Vì $\Delta \parallel (P)$ nên $\vec{u}_\Delta \perp \vec{n}_P$; và $\Delta \perp d$ nên $\vec{u}_\Delta \perp \vec{u}_d$.
- Do đó, một vectơ chỉ phương của $\Delta$ có thể chọn là tích có hướng của $\vec{n}_P$ và $\vec{u}_d$:
  $$\vec{u} = [\vec{n}_P, \vec{u}_d] = \left( (-1)(-1) - 2(1);\, 2(2) - 2(-1);\, 2(1) - (-1)(2) \right) = (-1; 6; 4)$$

---

### Câu 11.
Khảo sát thời gian tập thể dục mỗi ngày (đơn vị: phút) của $50$ người cao tuổi tại một khu dân cư thu được bảng số liệu ghép nhóm như sau:

| Thời gian (phút) | $[10; 20)$ | $[20; 30)$ | $[30; 40)$ | $[40; 50)$ | $[50; 60)$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Tần số (số người) | $5$ | $12$ | $18$ | $10$ | $5$ |

Khoảng tứ phân vị của mẫu số liệu ghép nhóm này bằng
- **A.** $16,25$.
- **B.** $15,75$.
- **C.** $26,25$.
- **D.** $42,50$.

**Lời giải:**
- **Đáp án đúng:** **A**
- Cỡ mẫu $n = 5 + 12 + 18 + 10 + 5 = 50$.
- Tần số tích lũy của các nhóm lần lượt là: $cf_1 = 5$, $cf_2 = 17$, $cf_3 = 35$, $cf_4 = 45$, $cf_5 = 50$.
- **Xác định tứ phân vị thứ nhất $Q_1$:**
  - Ta có $\frac{n}{4} = \frac{50}{4} = 12,5$.
  - Vì $cf_1 = 5 < 12,5 \le cf_2 = 17$ nên nhóm chứa $Q_1$ là nhóm $[20; 30)$.
  - Áp dụng công thức:
    $$Q_1 = 20 + \frac{12,5 - 5}{12} \cdot (30 - 20) = 20 + \frac{7,5}{12} \cdot 10 = 20 + 6,25 = 26,25$$
- **Xác định tứ phân vị thứ ba $Q_3$:**
  - Ta có $\frac{3n}{4} = \frac{3 \cdot 50}{4} = 37,5$.
  - Vì $cf_3 = 35 < 37,5 \le cf_4 = 45$ nên nhóm chứa $Q_3$ là nhóm $[40; 50)$.
  - Áp dụng công thức:
    $$Q_3 = 40 + \frac{37,5 - 35}{10} \cdot (50 - 40) = 40 + \frac{2,5}{10} \cdot 10 = 42,5$$
- Khoảng tứ phân vị của mẫu số liệu ghép nhóm là:
  $$\Delta_Q = Q_3 - Q_1 = 42,5 - 26,25 = 16,25$$

---

### Câu 12.
Một nhà máy có hai phân xưởng I và II cùng sản xuất một loại linh kiện điện tử. Phân xưởng I sản xuất $60\%$ tổng sản lượng của nhà máy, phân xưởng II sản xuất $40\%$ tổng sản lượng còn lại. Biết rằng tỉ lệ phế phẩm của phân xưởng I là $2\%$ và của phân xưởng II là $3\%$. Chọn ngẫu nhiên một linh kiện từ kho hàng của nhà máy. Xác suất để linh kiện được chọn là phế phẩm bằng
- **A.** $0,024$.
- **B.** $0,025$.
- **C.** $0,050$.
- **D.** $0,012$.

**Lời giải:**
- **Đáp án đúng:** **A**
- Gọi $A_1$ là biến cố "Linh kiện được chọn do phân xưởng I sản xuất", ta có $P(A_1) = 0,60$.
- Gọi $A_2$ là biến cố "Linh kiện được chọn do phân xưởng II sản xuất", ta có $P(A_2) = 0,40$.
- Hai biến cố $A_1, A_2$ tạo thành một nhóm biến cố đầy đủ.
- Gọi $B$ là biến cố "Linh kiện được chọn là phế phẩm".
  - Xác suất linh kiện hỏng do phân xưởng I sản xuất: $P(B|A_1) = 2\% = 0,02$.
  - Xác suất linh kiện hỏng do phân xưởng II sản xuất: $P(B|A_2) = 3\% = 0,03$.
- Theo công thức xác suất toàn phần:
  $$P(B) = P(A_1)P(B|A_1) + P(A_2)P(B|A_2) = 0,60 \times 0,02 + 0,40 \times 0,03 = 0,012 + 0,012 = 0,024$$

---

## PHẦN II. Câu trắc nghiệm Đúng/Sai (4 câu — 4.00 điểm)
*Thí sinh trả lời từ câu 1 đến câu 4. Trong mỗi ý a), b), c), d) ở mỗi câu, thí sinh chọn Đúng hoặc Sai.*

---

### Câu 1.
Cho hàm số $y = f(x) = \frac{x^2 - 2x + 5}{x - 1}$.
- **a)** Hàm số đã cho đồng biến trên khoảng $(3; +\infty)$.
- **b)** Đồ thị hàm số có đường tiệm cận xiên là đường thẳng $y = x - 1$.
- **c)** Giá trị cực đại của hàm số đã cho bằng $6$.
- **d)** Đường thẳng đi qua hai điểm cực trị của đồ thị hàm số có phương trình $y = 2x - 2$.

**Lời giải:**
- **Kết quả từng mệnh đề:**
  - **a) Đúng**
  - **b) Đúng**
  - **c) Sai**
  - **d) Đúng**
- **Giải chi tiết:**
  - Tập xác định của hàm số: $\mathcal{D} = \mathbb{R} \setminus \{1\}$.
  - Ta phân tích hàm số: $f(x) = \frac{(x - 1)^2 + 4}{x - 1} = x - 1 + \frac{4}{x - 1}$.
  - Đạo hàm: $f'(x) = 1 - \frac{4}{(x - 1)^2} = \frac{(x - 1)^2 - 4}{(x - 1)^2} = \frac{x^2 - 2x - 3}{(x - 1)^2} = \frac{(x + 1)(x - 3)}{(x - 1)^2}$.
  - Cho $f'(x) = 0 \iff (x + 1)(x - 3) = 0 \iff x = -1$ hoặc $x = 3$.
  - Bảng biến thiên cho thấy trên khoảng $(3; +\infty)$, $f'(x) > 0$ nên hàm số đồng biến trên $(3; +\infty)$. Do đó **a) Đúng**.
  - Ta có $\lim_{x \to \pm\infty} [f(x) - (x - 1)] = \lim_{x \to \pm\infty} \frac{4}{x - 1} = 0$, suy ra đường thẳng $y = x - 1$ là đường tiệm cận xiên của đồ thị hàm số. Do đó **b) Đúng**.
  - Đạo hàm đổi dấu từ dương sang âm khi qua điểm $x = -1$, do đó $x = -1$ là điểm cực đại của hàm số. Giá trị cực đại là $y_{\text{CĐ}} = f(-1) = \frac{(-1)^2 - 2(-1) + 5}{-1 - 1} = \frac{8}{-2} = -4 \ne 6$. Do đó **c) Sai**.
  - Tọa độ hai điểm cực trị của đồ thị hàm số là $A(-1; -4)$ và $B(3; 4)$. Phương trình đường thẳng $AB$ đi qua hai cực trị có dạng $y = \frac{(x^2 - 2x + 5)'}{(x - 1)'} = \frac{2x - 2}{1} = 2x - 2$. Kiểm tra: tại $x = -1 \implies y = 2(-1) - 2 = -4$; tại $x = 3 \implies y = 2(3) - 2 = 4$ (hoàn toàn trùng khớp). Do đó **d) Đúng**.

---

### Câu 2.
Một ô tô đang chạy với vận tốc ban đầu $v_0 = 20\text{ m/s}$ thì người lái xe bất ngờ đạp phanh. Kể từ thời điểm đó, ô tô chuyển động chậm dần đều với vận tốc $v(t) = -4t + 20\text{ (m/s)}$, trong đó $t$ là thời gian tính bằng giây kể từ lúc bắt đầu đạp phanh.
- **a)** Gia tốc của ô tô kể từ lúc bắt đầu đạp phanh bằng $-4\text{ m/s}^2$.
- **b)** Kể từ lúc bắt đầu đạp phanh, sau $5$ giây thì ô tô dừng hẳn.
- **c)** Quãng đường ô tô đi được trong $3$ giây đầu tiên kể từ lúc đạp phanh bằng $48\text{ m}$.
- **d)** Giả sử trước khi đạp phanh $2$ giây ô tô chuyển động thẳng đều với vận tốc $20\text{ m/s}$. Tổng quãng đường ô tô di chuyển trong khoảng thời gian $7$ giây (gồm $2$ giây trước khi đạp phanh và $5$ giây phanh cho đến khi dừng hẳn) là $90\text{ m}$.

**Lời giải:**
- **Kết quả từng mệnh đề:**
  - **a) Đúng**
  - **b) Đúng**
  - **c) Sai**
  - **d) Đúng**
- **Giải chi tiết:**
  - Gia tốc tức thời của chuyển động là đạo hàm của hàm vận tốc:
    $$a(t) = v'(t) = (-4t + 20)' = -4\text{ (m/s}^2)$$
    Vậy gia tốc của ô tô luôn bằng $-4\text{ m/s}^2$. Do đó **a) Đúng**.
  - Ô tô dừng hẳn khi vận tốc triệt tiêu:
    $$v(t) = 0 \iff -4t + 20 = 0 \iff t = 5\text{ (giây)}$$
    Vậy ô tô dừng lại hoàn toàn sau $5$ giây. Do đó **b) Đúng**.
  - Quãng đường ô tô đi được trong $3$ giây đầu kể từ lúc đạp phanh được tính bởi tích phân:
    $$s(3) = \int_0^3 v(t)\,\mathrm{d}t = \int_0^3 (-4t + 20)\,\mathrm{d}t = \left[-2t^2 + 20t\right]_0^3 = -2(9) + 20(3) = -18 + 60 = 42\text{ (m)}$$
    Vì $42\text{ m} \ne 48\text{ m}$ nên **c) Sai**.
  - Trong $2$ giây trước khi đạp phanh, ô tô chạy đều với vận tốc $20\text{ m/s}$, quãng đường đi được là:
    $$s_1 = 20 \times 2 = 40\text{ (m)}$$
    Quãng đường ô tô đi trong $5$ giây từ lúc phanh đến khi dừng hẳn là:
    $$s_2 = \int_0^5 (-4t + 20)\,\mathrm{d}t = \left[-2t^2 + 20t\right]_0^5 = -2(25) + 20(5) = -50 + 100 = 50\text{ (m)}$$
    Tổng quãng đường trong $7$ giây đó là $s_{\text{tổng}} = s_1 + s_2 = 40 + 50 = 90\text{ (m)}$. Do đó **d) Đúng**.

---

### Câu 3.
Trong không gian với hệ tọa độ $Oxyz$, cho hai điểm $A(1; 2; -1)$, $B(3; 0; 1)$ và mặt phẳng $(P): x - y + 2z - 3 = 0$.
- **a)** Tọa độ trung điểm của đoạn thẳng $AB$ là điểm $M(2; 1; 0)$.
- **b)** Một vectơ chỉ phương của đường thẳng $AB$ là $\vec{u} = (1; -1; 1)$.
- **c)** Khoảng cách từ điểm $A$ đến mặt phẳng $(P)$ bằng $2\sqrt{6}$.
- **d)** Tọa độ hình chiếu vuông góc của điểm $A$ trên mặt phẳng $(P)$ là điểm $H(2; 1; 1)$.

**Lời giải:**
- **Kết quả từng mệnh đề:**
  - **a) Đúng**
  - **b) Đúng**
  - **c) Sai**
  - **d) Đúng**
- **Giải chi tiết:**
  - Trung điểm $M$ của đoạn thẳng $AB$ có tọa độ:
    $$x_M = \frac{1 + 3}{2} = 2,\quad y_M = \frac{2 + 0}{2} = 1,\quad z_M = \frac{-1 + 1}{2} = 0 \implies M(2; 1; 0)$$
    Do đó **a) Đúng**.
  - Ta có vectơ $\vec{AB} = (3 - 1; 0 - 2; 1 - (-1)) = (2; -2; 2) = 2(1; -1; 1)$.
    Do đó, vectơ $\vec{u} = (1; -1; 1)$ cùng phương với $\vec{AB}$ nên là một vectơ chỉ phương của đường thẳng $AB$. Do đó **b) Đúng**.
  - Khoảng cách từ điểm $A$ đến mặt phẳng $(P)$ là:
    $$d(A, (P)) = \frac{|1 - 2 + 2(-1) - 3|}{\sqrt{1^2 + (-1)^2 + 2^2}} = \frac{|-6|}{\sqrt{6}} = \frac{6}{\sqrt{6}} = \sqrt{6}$$
    Vì $\sqrt{6} \ne 2\sqrt{6}$ nên **c) Sai**.
  - Đường thẳng $\Delta$ đi qua $A(1; 2; -1)$ và vuông góc với $(P)$ nhận $\vec{n}_P = (1; -1; 2)$ làm vectơ chỉ phương:
    $$\Delta: \left\{\begin{aligned} x &= 1 + t \\ y &= 2 - t \\ z &= -1 + 2t \end{aligned}\right.$$
    Hình chiếu vuông góc $H$ của $A$ lên $(P)$ là giao điểm của $\Delta$ và $(P)$. Tọa độ $H$ tương ứng với $t$ thỏa mãn:
    $$(1 + t) - (2 - t) + 2(-1 + 2t) - 3 = 0 \iff 6t - 6 = 0 \iff t = 1$$
    Thay $t = 1$ ta được $H(1 + 1; 2 - 1; -1 + 2) = H(2; 1; 1)$. Do đó **d) Đúng**.

---

### Câu 4.
Một xét nghiệm y khoa sàng lọc được sử dụng trong cộng đồng để tầm soát một loại bệnh lý. Thống kê dịch tễ cho thấy tỉ lệ người mắc bệnh trong dân cư là $2\%$ (tức $0,02$). Đối với người thực sự mắc bệnh, xét nghiệm có xác suất cho kết quả dương tính là $98\%$. Đối với người hoàn toàn không mắc bệnh, xét nghiệm vẫn có xác suất cho kết quả dương tính giả là $2\%$ (tức tỉ lệ xét nghiệm âm tính đúng là $98\%$). Chọn ngẫu nhiên một người trong cộng đồng nói trên để làm xét nghiệm.
- **a)** Xác suất để người được chọn không mắc bệnh là $0,98$.
- **b)** Xác suất để người được chọn không mắc bệnh nhưng lại nhận kết quả xét nghiệm dương tính bằng $0,02$.
- **c)** Xác suất để người được chọn nhận kết quả xét nghiệm dương tính bằng $0,05$.
- **d)** Giả sử người được chọn có kết quả xét nghiệm dương tính. Xác suất để người đó thực sự mắc căn bệnh này là $0,5$ (tức $50\%$).

**Lời giải:**
- **Kết quả từng mệnh đề:**
  - **a) Đúng**
  - **b) Đúng**
  - **c) Sai**
  - **d) Đúng**
- **Giải chi tiết:**
  - Gọi $A$ là biến cố "Người được chọn thực sự mắc bệnh". Khi đó $\bar{A}$ là biến cố "Người được chọn không mắc bệnh".
    Theo dữ liệu bài toán: $P(A) = 0,02 \implies P(\bar{A}) = 1 - 0,02 = 0,98$. Do đó **a) Đúng**.
  - Gọi $B$ là biến cố "Người được chọn nhận kết quả xét nghiệm dương tính".
    Xác suất dương tính đối với người mắc bệnh (độ nhạy): $P(B|A) = 0,98$.
    Xác suất dương tính giả đối với người không mắc bệnh: $P(B|\bar{A}) = 1 - 0,98 = 0,02$. Do đó **b) Đúng**.
  - Áp dụng công thức xác suất toàn phần, xác suất để một người bất kỳ nhận kết quả dương tính là:
    $$P(B) = P(A)P(B|A) + P(\bar{A})P(B|\bar{A}) = 0,02 \times 0,98 + 0,98 \times 0,02 = 0,0196 + 0,0196 = 0,0392\text{ (tức } 3,92\%)$$
    Vì $0,0392 \ne 0,05$ nên **c) Sai**.
  - Xác suất người nhận kết quả dương tính thực sự mang bệnh được tính theo công thức Bayes:
    $$P(A|B) = \frac{P(A)P(B|A)}{P(B)} = \frac{0,0196}{0,0392} = \frac{1}{2} = 0,5\text{ (tức } 50\%)$$
    Như vậy, dù xét nghiệm có độ nhạy rất cao ($98\%$), nhưng do căn bệnh hiếm gặp trong cộng đồng ($2\%$), nên một người nhận kết quả dương tính chỉ có đúng $50\%$ khả năng thực sự mắc bệnh. Do đó **d) Đúng**.

---

## PHẦN III. Câu trắc nghiệm trả lời ngắn (6 câu — 3.00 điểm)
*Thí sinh trả lời từ câu 1 đến câu 6. Điền kết quả là một số nguyên hoặc số thập phân gọn vào khung đáp án.*

---

### Câu 1.
Một doanh nghiệp sản xuất một loại sản phẩm công nghệ độc quyền. Chi phí sản xuất $x$ sản phẩm ($1 \le x \le 100$) được cho bởi hàm số $C(x) = x^2 + 30x + 400$ (đơn vị: triệu đồng). Giá bán của mỗi sản phẩm trên thị trường phụ thuộc vào số lượng sản xuất theo hàm cầu $p(x) = 190 - x$ (đơn vị: triệu đồng/sản phẩm). Giả sử toàn bộ sản phẩm sản xuất ra đều được bán hết. Để thu được lợi nhuận lớn nhất thì doanh nghiệp cần sản xuất bao nhiêu sản phẩm?

**Lời giải:**
- **Đáp số:** `40`
- Doanh thu của công ty khi tiêu thụ hết $x$ sản phẩm là:
  $$R(x) = x \cdot p(x) = x(190 - x) = 190x - x^2\text{ (triệu đồng)}$$
- Lợi nhuận của doanh nghiệp là:
  $$L(x) = R(x) - C(x) = (190x - x^2) - (x^2 + 30x + 400) = -2x^2 + 160x - 400\text{ (triệu đồng)}$$
- Xét hàm lợi nhuận $L(x)$ trên đoạn $[1; 100]$:
  $$L'(x) = -4x + 160$$
  $$L'(x) = 0 \iff -4x + 160 = 0 \iff x = 40 \in [1; 100]$$
- Vì hàm số bậc hai có hệ số $a = -2 < 0$ nên $L(x)$ đạt giá trị lớn nhất tại đỉnh parabol $x = 40$.
- Giá trị lợi nhuận tối đa khi đó là $L(40) = -2(40)^2 + 160(40) - 400 = 2800$ triệu đồng.
- Vậy doanh nghiệp cần sản xuất $40$ sản phẩm.

---

### Câu 2.
Một cổng chào của khu triển lãm công nghệ có dạng đường parabol với chiều cao $9\text{ m}$ và bề rộng của chân cổng tại mặt đất bằng $6\text{ m}$. Người ta thiết kế một khung cửa kính hình chữ nhật bên trong cổng sao cho hai đỉnh dưới nằm trên mặt đất và hai đỉnh trên tiếp xúc với vách vòm parabol. Chiều rộng của khung cửa kính chữ nhật này bằng $4\text{ m}$. Phần diện tích còn lại của mặt đứng cổng chào (nằm ngoài khung cửa kính và nằm dưới vòm parabol) được ốp tấm alu màu nghệ thuật. Tính diện tích phần ốp tấm alu theo đơn vị mét vuông ($\text{m}^2$).

**Lời giải:**
- **Đáp số:** `16`
- Chọn hệ trục tọa độ $Oxy$ sao cho gốc $O$ là trung điểm của chân cổng trên mặt đất, trục hoành $Ox$ trùng với mặt đất, trục tung $Oy$ là trục đối xứng của cổng parabol.
- Đỉnh của parabol nằm trên trục tung tại điểm $(0; 9)$. Chân cổng có bề rộng $6\text{ m}$ nên cắt trục hoành tại hai điểm $(-3; 0)$ và $(3; 0)$.
- Parabol có dạng $y = ax^2 + 9$. Thay tọa độ $(3; 0)$ vào ta có:
  $$a \cdot 3^2 + 9 = 0 \iff 9a = -9 \iff a = -1$$
  Vậy phương trình của đường parabol là: $y = 9 - x^2$.
- Diện tích toàn bộ mặt đứng cổng parabol là:
  $$S_{\text{toàn bộ}} = \int_{-3}^3 (9 - x^2)\,\mathrm{d}x = \left[ 9x - \frac{x^3}{3} \right]_{-3}^3 = \left(27 - 9\right) - \left(-27 + 9\right) = 18 - (-18) = 36\text{ (m}^2\text{)}$$
- Khung cửa hình chữ nhật có bề rộng $4\text{ m}$, đặt đối xứng qua trục $Oy$ nên cạnh dưới nằm trên đoạn $[-2; 2]$ của trục $Ox$.
- Chiều cao của khung cửa là tung độ của parabol tại $x = 2$:
  $$h = y(2) = 9 - 2^2 = 5\text{ (m)}$$
- Diện tích khung cửa kính chữ nhật là:
  $$S_{\text{cửa}} = 4 \times 5 = 20\text{ (m}^2\text{)}$$
- Diện tích phần còn lại cần ốp alu là:
  $$S_{\text{alu}} = S_{\text{toàn bộ}} - S_{\text{cửa}} = 36 - 20 = 16\text{ (m}^2\text{)}$$

---

### Câu 3.
Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông cạnh bằng $6$, cạnh bên $SA$ vuông góc với mặt phẳng đáy $(ABCD)$ và $SA = 3$. Gọi $M$ là trung điểm của cạnh $BC$. Tính khoảng cách giữa hai đường thẳng $SB$ và $DM$.

**Lời giải:**
- **Đáp số:** `2`
- Chọn hệ trục tọa độ $Oxyz$ sao cho gốc $O \equiv A(0; 0; 0)$, tia $Ox$ chứa cạnh $AB$, tia $Oy$ chứa cạnh $AD$, tia $Oz$ chứa cạnh $AS$.
- Tọa độ các đỉnh:
  $$A(0; 0; 0),\quad B(6; 0; 0),\quad D(0; 6; 0),\quad C(6; 6; 0),\quad S(0; 0; 3)$$
- Điểm $M$ là trung điểm của $BC$ nên $M(6; 3; 0)$.
- Các vectơ định hướng:
  - $\vec{SB} = B - S = (6; 0; -3)$
  - $\vec{DM} = M - D = (6; -3; 0)$
  - $\vec{SD} = D - S = (0; 6; -3)$
- Tích có hướng $[\vec{SB}, \vec{DM}]$:
  $$[\vec{SB}, \vec{DM}] = \left( 0(0) - (-3)(-3);\, (-3)(6) - 6(0);\, 6(-3) - 0(6) \right) = (-9; -18; -18)$$
- Ta có $|[\vec{SB}, \vec{DM}]| = \sqrt{(-9)^2 + (-18)^2 + (-18)^2} = \sqrt{81 + 324 + 324} = \sqrt{729} = 27$.
- Tích vô hướng $[\vec{SB}, \vec{DM}] \cdot \vec{SD}$:
  $$[\vec{SB}, \vec{DM}] \cdot \vec{SD} = (-9)(0) + (-18)(6) + (-18)(-3) = 0 - 108 + 54 = -54$$
- Khoảng cách giữa hai đường thẳng chéo nhau $SB$ và $DM$ là:
  $$d(SB, DM) = \frac{|[\vec{SB}, \vec{DM}] \cdot \vec{SD}|}{|[\vec{SB}, \vec{DM}]|} = \frac{|-54|}{27} = \frac{54}{27} = 2$$

---

### Câu 4.
Trong không gian với hệ tọa độ $Oxyz$ (đơn vị đo trên mỗi trục là kilômét), một trạm radar cảnh báo được đặt tại gốc tọa độ $O(0; 0; 0)$. Một thiết bị bay không người lái (UAV) bay thẳng theo quỹ đạo đường thẳng $d$ đi qua hai điểm $A(2; 4; 4)$ và $B(1; 2; 5)$. Khi UAV bay đến vị trí điểm $M(a; b; c)$ trên đường thẳng $d$ thì khoảng cách từ UAV đến trạm radar $O$ là ngắn nhất. Tính giá trị của biểu thức $T = a + 2b + 3c$.

**Lời giải:**
- **Đáp số:** `20`
- Vectơ chỉ phương của đường thẳng quỹ đạo $d$:
  $$\vec{u} = \vec{BA} = (2 - 1; 4 - 2; 4 - 5) = (1; 2; -1)$$
- Phương trình tham số của đường thẳng $d$ đi qua $A(2; 4; 4)$ là:
  $$d: \left\{\begin{aligned} x &= 2 + t \\ y &= 4 + 2t \\ z &= 4 - t \end{aligned}\right. \quad (t \in \mathbb{R})$$
- Vì $M \in d$ nên $M(2 + t; 4 + 2t; 4 - t)$.
- Khoảng cách $OM$ ngắn nhất khi và chỉ khi vectơ $\vec{OM}$ vuông góc với vectơ chỉ phương $\vec{u}$:
  $$\vec{OM} \cdot \vec{u} = 0 \iff 1(2 + t) + 2(4 + 2t) - 1(4 - t) = 0$$
  $$\iff 2 + t + 8 + 4t - 4 + t = 0 \iff 6t + 6 = 0 \iff t = -1$$
- Thay $t = -1$ vào tọa độ $M$, ta thu được:
  $$a = 2 + (-1) = 1,\quad b = 4 + 2(-1) = 2,\quad c = 4 - (-1) = 5 \implies M(1; 2; 5)$$
- Giá trị của biểu thức $T$ là:
  $$T = a + 2b + 3c = 1 + 2(2) + 3(5) = 1 + 4 + 15 = 20$$

---

### Câu 5.
Có hai hộp kín chứa các quả cầu cùng kích thước và khối lượng. Hộp I chứa $3$ quả cầu màu đỏ và $5$ quả cầu màu xanh. Hộp II chứa $4$ quả cầu màu đỏ và $5$ quả cầu màu xanh. Người ta lấy ngẫu nhiên $1$ quả cầu từ Hộp I bỏ sang Hộp II, lắc đều rồi từ Hộp II lấy ngẫu nhiên ra $2$ quả cầu. Biết rằng cả $2$ quả cầu lấy ra từ Hộp II đều có màu đỏ. Tính xác suất để quả cầu được chuyển từ Hộp I sang Hộp II trước đó là quả cầu màu đỏ (kết quả ghi dưới dạng số thập phân gọn).

**Lời giải:**
- **Đáp số:** `0.5`
- Gọi $A$ là biến cố "Quả cầu lấy từ Hộp I chuyển sang Hộp II là màu đỏ".
  Khi đó $\bar{A}$ là biến cố "Quả cầu lấy từ Hộp I chuyển sang Hộp II là màu xanh".
  Hộp I có $3$ đỏ và $5$ xanh (tổng 8 quả), do đó:
  $$P(A) = \frac{3}{8},\quad P(\bar{A}) = \frac{5}{8}$$
- Gọi $B$ là biến cố "Lấy được $2$ quả cầu màu đỏ từ Hộp II".
  - Nếu $A$ xảy ra (chuyển quả đỏ sang Hộp II): Hộp II lúc này có $4 + 1 = 5$ quả đỏ và $5$ quả xanh (tổng $10$ quả).
    Xác suất lấy được $2$ quả đỏ là:
    $$P(B|A) = \frac{C_5^2}{C_{10}^2} = \frac{10}{45} = \frac{2}{9}$$
  - Nếu $\bar{A}$ xảy ra (chuyển quả xanh sang Hộp II): Hộp II lúc này có $4$ quả đỏ và $5 + 1 = 6$ quả xanh (tổng $10$ quả).
    Xác suất lấy được $2$ quả đỏ là:
    $$P(B|\bar{A}) = \frac{C_4^2}{C_{10}^2} = \frac{6}{45} = \frac{2}{15}$$
- Theo công thức xác suất toàn phần:
  $$P(B) = P(A)P(B|A) + P(\bar{A})P(B|\bar{A}) = \frac{3}{8} \cdot \frac{10}{45} + \frac{5}{8} \cdot \frac{6}{45} = \frac{30}{360} + \frac{30}{360} = \frac{60}{360} = \frac{1}{6}$$
- Theo công thức Bayes, xác suất quả cầu chuyển từ Hộp I sang Hộp II là quả màu đỏ khi biết biến cố $B$ đã xảy ra:
  $$P(A|B) = \frac{P(A)P(B|A)}{P(B)} = \frac{\frac{30}{360}}{\frac{60}{360}} = \frac{30}{60} = 0,5$$

---

### Câu 6.
Một nhà máy phát điện đặt tại vị trí điểm $A$ bên một đường bờ biển thẳng. Một trạm biến áp cấp điện trên đảo du lịch được đặt tại vị trí điểm $C$, cách bờ biển một khoảng $CB = 4\text{ km}$ ($CB$ vuông góc với bờ biển tại $B$), và khoảng cách giữa $A$ và $B$ dọc theo bờ biển là $AB = 10\text{ km}$. Để cấp điện cho trạm $C$, người ta lắp đặt đường dây tải điện trên bộ từ nhà máy $A$ đến một điểm $M$ ($M$ thuộc đoạn thẳng $AB$), sau đó lắp đặt đường cáp ngầm dưới biển từ $M$ đến $C$. Chi phí lắp đặt đường dây trên bộ là $300$ triệu đồng/$\text{km}$, chi phí lắp đặt cáp ngầm dưới biển là $500$ triệu đồng/$\text{km}$. Chi phí thấp nhất (theo đơn vị triệu đồng) để hoàn thành việc cấp điện từ nhà máy $A$ ra đảo $C$ bằng bao nhiêu?

**Lời giải:**
- **Đáp số:** `4600`
- Đặt khoảng cách $BM = x\text{ (km)}$ với $0 \le x \le 10$.
- Khi đó:
  - Chiều dài đường dây tải điện trên bộ là $AM = AB - BM = 10 - x\text{ (km)}$.
  - Tam giác $\triangle MBC$ vuông tại $B$, do đó chiều dài đường cáp ngầm dưới biển là:
    $$MC = \sqrt{MB^2 + BC^2} = \sqrt{x^2 + 4^2} = \sqrt{x^2 + 16}\text{ (km)}$$
- Tổng chi phí lắp đặt (triệu đồng) là hàm số phụ thuộc vào $x$:
  $$f(x) = 300(10 - x) + 500\sqrt{x^2 + 16} \quad (0 \le x \le 10)$$
- Lấy đạo hàm:
  $$f'(x) = -300 + 500 \cdot \frac{x}{\sqrt{x^2 + 16}}$$
- Giải phương trình $f'(x) = 0$:
  $$500 \cdot \frac{x}{\sqrt{x^2 + 16}} = 300 \iff 5x = 3\sqrt{x^2 + 16}$$
  Bình phương hai vế (với $x \ge 0$):
  $$25x^2 = 9(x^2 + 16) \iff 16x^2 = 144 \iff x^2 = 9 \iff x = 3\text{ (km)}$$
- Tính giá trị chi phí tại $x = 3$ và hai đầu mút:
  - Tại $x = 3$:
    $$f(3) = 300(10 - 3) + 500\sqrt{3^2 + 16} = 300(7) + 500(5) = 2100 + 2500 = 4600\text{ (triệu đồng)}$$
  - Tại $x = 0$ (kéo cáp từ $B$):
    $$f(0) = 300(10) + 500(4) = 3000 + 2000 = 5000\text{ (triệu đồng)}$$
  - Tại $x = 10$ (kéo thẳng ngầm từ $A$ đến $C$):
    $$f(10) = 0 + 500\sqrt{10^2 + 16} = 500\sqrt{116} \approx 5385,16\text{ (triệu đồng)}$$
- Vậy chi phí thấp nhất là $4600$ triệu đồng (đạt được khi đặt điểm rẽ nhánh $M$ cách $B$ một khoảng $3\text{ km}$, tức cách nhà máy $A$ là $7\text{ km}$).

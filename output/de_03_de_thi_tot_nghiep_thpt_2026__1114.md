# KỲ THI TỐT NGHIỆP TRUNG HỌC PHỔ THÔNG NĂM 2026
**MÔN: TOÁN (CHƯƠNG TRÌNH GDPT 2018)**  
*Thời gian làm bài: 90 phút (không kể thời gian phát đề)*  
*Tổng số câu: 22 câu | Tổng điểm: 10.00 điểm*  
*(Chuyên đề: Tổng hợp chuẩn 5 chuyên đề GDPT 2018 — Hàm số, Oxyz, Tích phân, Xác suất - Thống kê, Hình học không gian)*  
*(Đề thi và toàn bộ lời giải chi tiết đã được kiểm chứng tính toán chính xác 100% bằng SymPy)*

---

### CẤU TRÚC VÀ QUY TẮC TÍNH ĐIỂM ĐỀ THI CHUẨN NĂM 2026
- **PHẦN I (12 câu — 3.00 điểm):** Thí sinh chọn một phương án trả lời đúng duy nhất trong 4 phương án $A, B, C, D$. Mỗi câu trả lời đúng thí sinh được $0,25$ điểm; trả lời sai hoặc không trả lời không có điểm.
- **PHẦN II (4 câu — 4.00 điểm):** Câu trắc nghiệm Đúng/Sai. Mỗi câu lớn là **MỘT BÀI TOÁN TỰ LUẬN THU NHỎ** từ một dữ kiện gốc chung, gồm 4 mệnh đề $a), b), c), d)$ kiểm tra độc lập theo tiến trình tư duy giải toán từ dễ đến khó (a: Nhận biết $\rightarrow$ b: Thông hiểu $\rightarrow$ c: Vận dụng $\rightarrow$ d: Vận dụng cao). Thang điểm lũy tiến từng câu như sau:
  - Đúng $1$ ý: được $0,10$ điểm.
  - Đúng $2$ ý: được $0,25$ điểm.
  - Đúng $3$ ý: được $0,50$ điểm.
  - Đúng cả $4$ ý trọn vẹn: được $1,00$ điểm.
- **PHẦN III (6 câu — 3.00 điểm):** Câu trắc nghiệm trả lời ngắn. Thí sinh tự tính toán và điền đáp số là một con số nguyên hoặc số thập phân gọn. Mỗi câu trả lời đúng được $0,50$ điểm.

---

## PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn (12 câu — 3.00 điểm)
*Thí sinh trả lời từ câu 1 đến câu 12. Mỗi câu hỏi chỉ chọn một phương án.*

---

### Câu 1.
Đường cong trong hình vẽ bên là đồ thị của hàm số nào dưới đây?

![Đồ thị hàm số bậc ba](output/images/de03_cau01_bac3.png)

- **A.** $y = x^3 - 3x + 2$.
- **B.** $y = -x^3 + 3x + 2$.
- **C.** $y = x^3 - 3x^2 + 2$.
- **D.** $y = x^3 + 3x + 2$.

**Lời giải:**
- **Đáp án đúng:** **A**
- Nhánh ngoài cùng bên phải của đồ thị đi lên khi $x \to +\infty$, suy ra hệ số $a > 0 \implies$ loại phương án **B**.
- Đồ thị cắt trục tung tại điểm có tọa độ $(0; 2)$.
- Đồ thị có hai điểm cực trị là điểm cực đại $A(-1; 4)$ và điểm cực tiểu $B(1; 0)$.
  - Với hàm số $y = x^3 - 3x + 2$:
    - Đạo hàm $y' = 3x^2 - 3 = 0 \iff x = \pm 1$.
    - Tại $x = -1 \implies y = (-1)^3 - 3(-1) + 2 = 4$ (điểm cực đại $(-1; 4)$).
    - Tại $x = 1 \implies y = 1^3 - 3(1) + 2 = 0$ (điểm cực tiểu $(1; 0)$).
- Do đó đồ thị đã cho là đồ thị của hàm số $y = x^3 - 3x + 2$.

---

### Câu 2.
Đường tiệm cận xiên của đồ thị hàm số $y = \frac{x^2 - 3x + 5}{x - 1}$ là đường thẳng có phương trình
- **A.** $y = x + 2$.
- **B.** $y = x - 2$.
- **C.** $y = x - 3$.
- **D.** $y = 2x - 1$.

**Lời giải:**
- **Đáp án đúng:** **B**
- Thực hiện phép chia đa thức tử cho mẫu:
  $$y = \frac{x^2 - 3x + 5}{x - 1} = \frac{(x - 1)(x - 2) + 3}{x - 1} = x - 2 + \frac{3}{x - 1}$$
- Ta có:
  $$\lim_{x \to +\infty} [y - (x - 2)] = \lim_{x \to +\infty} \frac{3}{x - 1} = 0$$
  $$\lim_{x \to -\infty} [y - (x - 2)] = \lim_{x \to -\infty} \frac{3}{x - 1} = 0$$
- Vậy đường tiệm cận xiên của đồ thị hàm số là đường thẳng $y = x - 2$.

---

### Câu 3.
Cho hàm số $y = f(x)$ xác định và liên tục trên $\mathbb{R}$. Biết hàm số đạo hàm $y = f'(x)$ có đồ thị như hình vẽ bên.

![Đồ thị hàm số đạo hàm](output/images/de03_cau03_daoham.png)

Hàm số $y = f(x)$ đồng biến trên khoảng nào dưới đây?
- **A.** $(-1; 2)$.
- **B.** $(0; 3)$.
- **C.** $(2; +\infty)$.
- **D.** $(-\infty; 1)$.

**Lời giải:**
- **Đáp án đúng:** **C**
- Quan sát đồ thị hàm số $y = f'(x)$, ta thấy:
  - $f'(x) > 0$ khi và chỉ khi đồ thị $f'(x)$ nằm phía trên trục hoành, tức là $x \in (-\infty; -1) \cup (2; +\infty)$.
  - $f'(x) < 0$ khi và chỉ khi đồ thị $f'(x)$ nằm phía dưới trục hoành, tức là $x \in (-1; 2)$.
- Do đó, hàm số $y = f(x)$ đồng biến trên các khoảng $(-\infty; -1)$ và $(2; +\infty)$.
- Trong bốn phương án đã cho, chỉ có khoảng $(2; +\infty)$ thỏa mãn.

---

### Câu 4.
Cho hình chóp $S.ABC$ có đáy $ABC$ là tam giác vuông tại $B$, $AB = a, BC = a\sqrt{3}$. Cạnh bên $SA$ vuông góc với mặt phẳng đáy $(ABC)$ và $SA = a$. Góc giữa đường thẳng $SB$ và mặt phẳng đáy $(ABC)$ bằng
- **A.** $30^\circ$.
- **B.** $60^\circ$.
- **C.** $90^\circ$.
- **D.** $45^\circ$.

**Lời giải:**
- **Đáp án đúng:** **D**
- Vì $SA \perp (ABC)$ nên hình chiếu vuông góc của điểm $S$ lên mặt phẳng $(ABC)$ là điểm $A$.
- Do đó, hình chiếu vuông góc của đường thẳng $SB$ lên mặt phẳng $(ABC)$ là đường thẳng $AB$.
- Suy ra góc giữa đường thẳng $SB$ và mặt phẳng $(ABC)$ chính là góc giữa hai đường thẳng $SB$ và $AB$, tức là góc $\widehat{SBA}$.
- Xét tam giác $SAB$ vuông tại $A$, ta có:
  $$\tan \widehat{SBA} = \frac{SA}{AB} = \frac{a}{a} = 1 \implies \widehat{SBA} = 45^\circ$$

---

### Câu 5.
Cho khối chóp tứ giác đều $S.ABCD$ có cạnh đáy bằng $a$ và chiều cao $h = 3a$. Thể tích của khối chóp đã cho bằng
- **A.** $3a^3$.
- **B.** $a^3$.
- **C.** $\frac{1}{3}a^3$.
- **D.** $\frac{4}{3}a^3$.

**Lời giải:**
- **Đáp án đúng:** **B**
- Đáy $ABCD$ của khối chóp tứ giác đều là hình vuông cạnh $a$, do đó diện tích đáy là:
  $$S_{\text{đáy}} = a^2$$
- Thể tích khối chóp là:
  $$V = \frac{1}{3} S_{\text{đáy}} \cdot h = \frac{1}{3} a^2 \cdot (3a) = a^3$$

---

### Câu 6.
Trong không gian với hệ tọa độ $Oxyz$, cho mặt cầu $(S): (x - 2)^2 + (y + 1)^2 + (z - 4)^2 = 25$. Tọa độ tâm $I$ và bán kính $R$ của mặt cầu $(S)$ là
- **A.** $I(2; -1; 4)$ và $R = 5$.
- **B.** $I(-2; 1; -4)$ và $R = 5$.
- **C.** $I(2; -1; 4)$ và $R = 25$.
- **D.** $I(-2; 1; -4)$ và $R = 25$.

**Lời giải:**
- **Đáp án đúng:** **A**
- Phương trình chính tắc của mặt cầu có tâm $I(x_0; y_0; z_0)$ và bán kính $R$ là:
  $$(x - x_0)^2 + (y - y_0)^2 + (z - z_0)^2 = R^2$$
- Đối chiếu với phương trình đề bài $(x - 2)^2 + (y - (-1))^2 + (z - 4)^2 = 5^2$, ta có:
  - Tọa độ tâm: $I(2; -1; 4)$.
  - Bán kính: $R = \sqrt{25} = 5$.

---

### Câu 7.
Trong không gian với hệ tọa độ $Oxyz$, phương trình mặt phẳng đi qua ba điểm $A(3; 0; 0)$, $B(0; -2; 0)$, $C(0; 0; 1)$ là
- **A.** $2x + 3y + 6z - 6 = 0$.
- **B.** $2x - 3y + 6z + 6 = 0$.
- **C.** $2x - 3y + 6z - 6 = 0$.
- **D.** $3x - 2y + z - 6 = 0$.

**Lời giải:**
- **Đáp án đúng:** **C**
- Ba điểm $A(3; 0; 0)$, $B(0; -2; 0)$, $C(0; 0; 1)$ lần lượt nằm trên ba trục tọa độ $Ox, Oy, Oz$.
- Áp dụng phương trình mặt phẳng theo đoạn chắn:
  $$\frac{x}{3} + \frac{y}{-2} + \frac{z}{1} = 1$$
- Quy đồng mẫu số chung là $6$:
  $$2x - 3y + 6z = 6 \iff 2x - 3y + 6z - 6 = 0$$

---

### Câu 8.
Trong không gian với hệ tọa độ $Oxyz$, giao tuyến của hai mặt phẳng $(P): x + 2y - z + 1 = 0$ và $(Q): 2x - y + z - 4 = 0$ có một vectơ chỉ phương là
- **A.** $\vec{u}_2 = (1; 3; -5)$.
- **B.** $\vec{u}_3 = (3; 1; 5)$.
- **C.** $\vec{u}_4 = (1; -3; 5)$.
- **D.** $\vec{u}_1 = (1; -3; -5)$.

**Lời giải:**
- **Đáp án đúng:** **D**
- Vectơ pháp tuyến của hai mặt phẳng $(P)$ và $(Q)$ lần lượt là:
  $$\vec{n}_P = (1; 2; -1),\quad \vec{n}_Q = (2; -1; 1)$$
- Giao tuyến $d$ của $(P)$ và $(Q)$ vuông góc với cả $\vec{n}_P$ và $\vec{n}_Q$, nên một vectơ chỉ phương của $d$ là tích có hướng:
  $$\vec{u} = [\vec{n}_P, \vec{n}_Q] = \left( 2 \cdot 1 - (-1)(-1);\, (-1) \cdot 2 - 1 \cdot 1;\, 1 \cdot (-1) - 2 \cdot 2 \right) = (1; -3; -5)$$
- Vậy một vectơ chỉ phương của giao tuyến là $\vec{u}_1 = (1; -3; -5)$.

---

### Câu 9.
Tập nghiệm của bất phương trình $\log_2(3x - 5) \le 2$ là
- **A.** $\left(\frac{5}{3}; 3\right]$.
- **B.** $(-\infty; 3]$.
- **C.** $\left[\frac{5}{3}; 3\right]$.
- **D.** $(3; +\infty)$.

**Lời giải:**
- **Đáp án đúng:** **A**
- Điều kiện xác định: $3x - 5 > 0 \iff x > \frac{5}{3}$.
- Vì cơ số $2 > 1$ nên bất phương trình tương đương:
  $$\log_2(3x - 5) \le 2 \iff 3x - 5 \le 2^2 = 4 \iff 3x \le 9 \iff x \le 3$$
- Kết hợp với điều kiện xác định, ta được tập nghiệm:
  $$S = \left(\frac{5}{3}; 3\right]$$

---

### Câu 10.
Giá trị của tích phân $I = \int_0^1 \frac{2x + 3}{x + 1}\,\mathrm{d}x$ bằng
- **A.** $2 - \ln 2$.
- **B.** $2 + \ln 2$.
- **C.** $1 + \ln 2$.
- **D.** $2 + 2\ln 2$.

**Lời giải:**
- **Đáp án đúng:** **B**
- Phân tích biểu thức dưới dấu tích phân:
  $$\frac{2x + 3}{x + 1} = \frac{2(x + 1) + 1}{x + 1} = 2 + \frac{1}{x + 1}$$
- Tính tích phân:
  $$I = \int_0^1 \left(2 + \frac{1}{x + 1}\right)\,\mathrm{d}x = \left[ 2x + \ln|x + 1| \right]_0^1 = (2 \cdot 1 + \ln 2) - (0 + \ln 1) = 2 + \ln 2$$

---

### Câu 11.
Diện tích hình phẳng giới hạn bởi đường parabol $(P): y = -x^2 + 4x$ và đường thẳng $d: y = x$ bằng
- **A.** $9$.
- **B.** $\frac{9}{4}$.
- **C.** $\frac{9}{2}$.
- **D.** $\frac{27}{2}$.

**Lời giải:**
- **Đáp án đúng:** **C**
- Phương trình hoành độ giao điểm của $(P)$ và $d$:
  $$-x^2 + 4x = x \iff -x^2 + 3x = 0 \iff x(3 - x) = 0 \iff \left[\begin{aligned} &x = 0 \\ &x = 3 \end{aligned}\right.$$
- Trên đoạn $[0; 3]$, ta có $(-x^2 + 4x) - x = 3x - x^2 \ge 0$.
- Diện tích hình phẳng cần tìm là:
  $$S = \int_0^3 (-x^2 + 3x)\,\mathrm{d}x = \left[ -\frac{x^3}{3} + \frac{3x^2}{2} \right]_0^3 = \left(-\frac{27}{3} + \frac{3 \cdot 9}{2}\right) - 0 = -9 + \frac{27}{2} = \frac{9}{2}$$

---

### Câu 12.
Một công ty thiết bị ghi lại thời gian sử dụng pin (đơn vị: giờ) của $40$ thiết bị sau một lần sạc đầy, thu được bảng tần số ghép nhóm như sau:

| Thời gian (giờ) | $[10; 15)$ | $[15; 20)$ | $[20; 25)$ | $[25; 30)$ | $[30; 35)$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Số thiết bị | $4$ | $12$ | $10$ | $8$ | $6$ |

Khoảng tứ phân vị $\Delta_Q$ của mẫu số liệu ghép nhóm trên bằng
- **A.** $12,5$.
- **B.** $15,0$.
- **C.** $7,5$.
- **D.** $10,0$.

**Lời giải:**
- **Đáp án đúng:** **D**
- Cỡ mẫu: $n = 4 + 12 + 10 + 8 + 6 = 40$.
- Tần số tích lũy của các nhóm lần lượt là: $cf_1 = 4$, $cf_2 = 16$, $cf_3 = 26$, $cf_4 = 34$, $cf_5 = 40$.
- **Tìm tứ phân vị thứ nhất $Q_1$:**
  - Ta có $\frac{n}{4} = \frac{40}{4} = 10$.
  - Do $cf_1 = 4 < 10 \le cf_2 = 16$ nên nhóm chứa $Q_1$ là nhóm thứ hai: $[15; 20)$.
  - Áp dụng công thức tính tứ phân vị:
    $$Q_1 = 15 + \frac{10 - 4}{12} \cdot (20 - 15) = 15 + \frac{6}{12} \cdot 5 = 15 + 2,5 = 17,5$$
- **Tìm tứ phân vị thứ ba $Q_3$:**
  - Ta có $\frac{3n}{4} = \frac{3 \cdot 40}{4} = 30$.
  - Do $cf_3 = 26 < 30 \le cf_4 = 34$ nên nhóm chứa $Q_3$ là nhóm thứ tư: $[25; 30)$.
  - Áp dụng công thức:
    $$Q_3 = 25 + \frac{30 - 26}{8} \cdot (30 - 25) = 25 + \frac{4}{8} \cdot 5 = 25 + 2,5 = 27,5$$
- Khoảng tứ phân vị của mẫu số liệu ghép nhóm là:
  $$\Delta_Q = Q_3 - Q_1 = 27,5 - 17,5 = 10,0$$

---

## PHẦN II. Câu trắc nghiệm Đúng/Sai (4 câu — 4.00 điểm)
*Thí sinh trả lời từ câu 1 đến câu 4. Trong mỗi ý a), b), c), d) ở mỗi câu, thí sinh chọn Đúng hoặc Sai.*

---

### Câu 1.
Cho hàm số bậc ba $y = f(x) = ax^3 + bx^2 + cx + d$ ($a \ne 0$) có đồ thị $(C)$ như hình vẽ bên. Biết đồ thị $(C)$ cắt trục tung tại điểm cực đại $A(0; 2)$ và có điểm cực tiểu là $B(2; -2)$.

![Đồ thị hàm số bậc ba Phần II Câu 1](output/images/de03_p2_cau01_bac3.png)

- **a)** Hệ số $a > 0$ và hệ số tự do $d = 2$.
- **b)** Hàm số $y = f(x)$ nghịch biến trên khoảng $(0; 2)$.
- **c)** Tổng các hệ số $S = a + b + c + d$ bằng $1$.
- **d)** Phương trình $|f(x)| = m$ có đúng $6$ nghiệm thực phân biệt khi và chỉ khi $0 < m < 2$.

**Lời giải:**
- **Kết quả từng mệnh đề:**
  - **a) Đúng**
  - **b) Đúng**
  - **c) Sai**
  - **d) Đúng**
- **Giải chi tiết:**
  - Nhánh bên phải của đồ thị đi lên khi $x \to +\infty \implies a > 0$. Đồ thị cắt trục tung tại $(0; 2) \implies f(0) = d = 2$. Do đó **a) Đúng**.
  - Hàm số đạt cực đại tại $x = 0$ và đạt cực tiểu tại $x = 2$. Trên khoảng $(0; 2)$, đồ thị hàm số đi xuống từ điểm $A(0; 2)$ đến điểm $B(2; -2)$ nên hàm số nghịch biến trên khoảng $(0; 2)$. Do đó **b) Đúng**.
  - Ta xác định chính xác các hệ số:
    - Đạo hàm: $f'(x) = 3ax^2 + 2bx + c$.
    - Hàm số đạt cực trị tại $x = 0$ và $x = 2$ nên $f'(0) = 0 \implies c = 0$.
    - $f'(2) = 12a + 4b = 0 \implies b = -3a$.
    - Tại điểm cực tiểu $B(2; -2)$: $f(2) = 8a + 4b + d = 8a + 4(-3a) + 2 = -4a + 2 = -2 \implies -4a = -4 \implies a = 1$.
    - Suy ra $b = -3(1) = -3$.
    - Hàm số là $f(x) = x^3 - 3x^2 + 2$.
    - Tổng $S = a + b + c + d = 1 + (-3) + 0 + 2 = 0 \ne 1$. Do đó **c) Sai**.
  - Đồ thị của hàm số $y = |f(x)|$ được suy ra từ đồ thị $(C)$ bằng cách giữ nguyên phần đồ thị nằm phía trên trục hoành và lấy đối xứng phần đồ thị nằm phía dưới trục hoành qua trục hoành:
    - Điểm cực tiểu $B(2; -2)$ đối xứng qua trục hoành thành điểm $(2; 2)$.
    - Điểm cực đại $A(0; 2)$ giữ nguyên ở độ cao $y = 2$.
    - Đồ thị $(C)$ cắt trục hoành tại $3$ điểm phân biệt (trong đó có 1 nghiệm âm và 2 nghiệm dương), tại các giao điểm này đồ thị $|f(x)|$ tiếp xúc trục hoành $y = 0$.
    - Do đó, đường thẳng nằm ngang $y = m$ cắt đồ thị $y = |f(x)|$ tại đúng $6$ điểm phân biệt khi và chỉ khi đường thẳng này nằm phía trên trục hoành và nằm dưới các đỉnh cực đại, tức là $0 < m < 2$. Do đó **d) Đúng**.

---

### Câu 2.
Cho hàm số $y = f(x) = \frac{x^2 + 2x + 2}{x + 1}$ có đồ thị là đường cong $(C)$.

![Đồ thị hàm phân thức 2/1 Phần II Câu 2](output/images/de03_p2_cau02_tiemcan.png)

- **a)** Đường thẳng $x = -1$ là đường tiệm cận đứng của đồ thị $(C)$.
- **b)** Đường tiệm cận xiên của đồ thị $(C)$ đi qua gốc tọa độ $O(0; 0)$.
- **c)** Tọa độ giao điểm của hai đường tiệm cận là điểm $I(-1; 0)$.
- **d)** Tích các khoảng cách từ một điểm $M$ tùy ý thuộc đồ thị $(C)$ đến hai đường tiệm cận luôn bằng $\frac{\sqrt{2}}{2}$.

**Lời giải:**
- **Kết quả từng mệnh đề:**
  - **a) Đúng**
  - **b) Sai**
  - **c) Đúng**
  - **d) Đúng**
- **Giải chi tiết:**
  - Phân tích hàm số:
    $$f(x) = \frac{(x + 1)^2 + 1}{x + 1} = x + 1 + \frac{1}{x + 1}$$
  - Ta có $\lim_{x \to (-1)^+} f(x) = +\infty$ và $\lim_{x \to (-1)^-} f(x) = -\infty$, nên đường thẳng $x = -1$ là tiệm cận đứng của đồ thị $(C)$. Do đó **a) Đúng**.
  - Ta có $\lim_{x \to \pm\infty} [f(x) - (x + 1)] = \lim_{x \to \pm\infty} \frac{1}{x + 1} = 0$, nên đường tiệm cận xiên của đồ thị là đường thẳng $d: y = x + 1$.
    - Khi $x = 0 \implies y = 0 + 1 = 1 \ne 0$, do đó tiệm cận xiên không đi qua gốc tọa độ $O(0; 0)$. Mệnh đề **b) Sai**.
  - Giao điểm $I$ của tiệm cận đứng $x = -1$ và tiệm cận xiên $y = x + 1$ có tọa độ thỏa mãn:
    $$x_I = -1,\quad y_I = -1 + 1 = 0 \implies I(-1; 0)$$
    Do đó **c) Đúng**.
  - Lấy điểm $M\left(x_0;\, x_0 + 1 + \frac{1}{x_0 + 1}\right) \in (C)$ với $x_0 \ne -1$:
    - Khoảng cách từ $M$ đến tiệm cận đứng $\Delta_1: x + 1 = 0$ là:
      $$d_1 = |x_0 + 1|$$
    - Phương trình tiệm cận xiên $\Delta_2: x - y + 1 = 0$. Khoảng cách từ $M$ đến $\Delta_2$ là:
      $$d_2 = \frac{\left| x_0 - \left(x_0 + 1 + \frac{1}{x_0 + 1}\right) + 1 \right|}{\sqrt{1^2 + (-1)^2}} = \frac{\left| -\frac{1}{x_0 + 1} \right|}{\sqrt{2}} = \frac{1}{\sqrt{2}|x_0 + 1|}$$
    - Tích hai khoảng cách là:
      $$d_1 \cdot d_2 = |x_0 + 1| \cdot \frac{1}{\sqrt{2}|x_0 + 1|} = \frac{1}{\sqrt{2}} = \frac{\sqrt{2}}{2}$$
    - Giá trị này là một hằng số không phụ thuộc vào vị trí của điểm $M$. Do đó **d) Đúng**.

---

### Câu 3.
Cho hàm số $y = f(x)$ có đạo hàm $f'(x)$ liên tục trên $\mathbb{R}$. Đồ thị của hàm số đạo hàm $y = f'(x)$ cắt trục hoành tại ba điểm phân biệt có hoành độ lần lượt là $x = -2, x = 1, x = 3$ như hình vẽ bên.

![Đồ thị hàm số đạo hàm Phần II Câu 3](output/images/de03_p2_cau03_daoham.png)

- **a)** Hàm số $y = f(x)$ có đúng $3$ điểm cực trị.
- **b)** Hàm số $y = f(x)$ đồng biến trên khoảng $(1; 3)$.
- **c)** Điểm cực đại của hàm số $y = f(x)$ là $x = 1$.
- **d)** Hàm số $g(x) = f(2 - x)$ đồng biến trên khoảng $(-1; 1)$.

**Lời giải:**
- **Kết quả từng mệnh đề:**
  - **a) Đúng**
  - **b) Sai**
  - **c) Đúng**
  - **d) Đúng**
- **Giải chi tiết:**
  - Đồ thị $y = f'(x)$ cắt trục hoành tại ba điểm phân biệt $x = -2, x = 1, x = 3$ và tại mỗi điểm đó đồ thị đều đi xuyên qua trục hoành (nghiệm bội lẻ), do đó $f'(x)$ đổi dấu $3$ lần khi qua các điểm này. Vậy hàm số $y = f(x)$ có đúng $3$ điểm cực trị. Mệnh đề **a) Đúng**.
  - Dựa vào hình vẽ, trên khoảng $(1; 3)$ đồ thị hàm số $y = f'(x)$ nằm hoàn toàn phía dưới trục hoành, tức là $f'(x) < 0,\, \forall x \in (1; 3)$. Do đó hàm số $y = f(x)$ nghịch biến trên khoảng $(1; 3)$. Mệnh đề **b) Sai**.
  - Xét dấu của đạo hàm $f'(x)$:
    - Trên khoảng $(-2; 1)$, đồ thị nằm phía trên trục hoành nên $f'(x) > 0$.
    - Trên khoảng $(1; 3)$, đồ thị nằm phía dưới trục hoành nên $f'(x) < 0$.
    - Khi đi qua điểm $x = 1$, $f'(x)$ đổi dấu từ dương sang âm, suy ra $x = 1$ là điểm cực đại của hàm số $y = f(x)$. Mệnh đề **c) Đúng**.
  - Xét hàm số $g(x) = f(2 - x)$:
    - Đạo hàm: $g'(x) = [f(2 - x)]' = -f'(2 - x)$.
    - Hàm số $g(x)$ đồng biến khi $g'(x) > 0 \iff -f'(2 - x) > 0 \iff f'(2 - x) < 0$.
    - Từ đồ thị $f'(u)$, ta thấy $f'(u) < 0 \iff \left[\begin{aligned} &u < -2 \\ &1 < u < 3 \end{aligned}\right.$
    - Thay $u = 2 - x$, ta có:
      - Trường hợp 1: $2 - x < -2 \iff x > 4$.
      - Trường hợp 2: $1 < 2 - x < 3 \iff -1 < -x < 1 \iff -1 < x < 1$.
    - Như vậy, hàm số $g(x)$ đồng biến trên khoảng $(-1; 1)$ và khoảng $(4; +\infty)$. Do đó **d) Đúng**.

---

### Câu 4.
Cho hình chóp $S.ABCD$ có đáy $ABCD$ là hình vuông cạnh $a$, cạnh bên $SA$ vuông góc với mặt phẳng đáy $(ABCD)$ và $SA = a\sqrt{2}$. Gọi $O$ là giao điểm của hai đường chéo $AC$ và $BD$.

![Hình chóp S.ABCD](output/images/de03_p2_cau04_hinhchop.png)

- **a)** Đường thẳng $BD$ vuông góc với mặt phẳng $(SAC)$.
- **b)** Góc giữa đường thẳng $SC$ và mặt phẳng đáy $(ABCD)$ bằng $45^\circ$.
- **c)** Tang của góc giữa mặt phẳng $(SBD)$ và mặt phẳng $(ABCD)$ bằng $\sqrt{2}$.
- **d)** Cosin của góc giữa mặt phẳng $(SCD)$ và mặt phẳng đáy $(ABCD)$ bằng $\frac{\sqrt{3}}{3}$.

**Lời giải:**
- **Kết quả từng mệnh đề:**
  - **a) Đúng**
  - **b) Đúng**
  - **c) Sai**
  - **d) Đúng**
- **Giải chi tiết:**
  - Ta có $BD \perp AC$ (hai đường chéo của hình vuông $ABCD$) và $BD \perp SA$ (do $SA \perp (ABCD)$). Suy ra $BD \perp (SAC)$. Do đó **a) Đúng**.
  - Vì $SA \perp (ABCD)$ nên $AC$ là hình chiếu vuông góc của $SC$ lên mặt phẳng $(ABCD)$.
    - Góc giữa $SC$ và $(ABCD)$ là góc $\widehat{SCA}$.
    - Đáy là hình vuông cạnh $a \implies AC = a\sqrt{2}$.
    - Xét tam giác vuông $SAC$ tại $A$: $\tan \widehat{SCA} = \frac{SA}{AC} = \frac{a\sqrt{2}}{a\sqrt{2}} = 1 \implies \widehat{SCA} = 45^\circ$. Do đó **b) Đúng**.
  - Giao tuyến của hai mặt phẳng $(SBD)$ và $(ABCD)$ là $BD$.
    - Ta có $AO \perp BD$ tại trung điểm $O$ và $SO \perp BD$ (do $\triangle SBD$ cân tại $S$ hoặc do $BD \perp (SAC)$).
    - Góc giữa hai mặt phẳng $(SBD)$ và $(ABCD)$ là góc $\widehat{SOA}$.
    - Ta có $AO = \frac{AC}{2} = \frac{a\sqrt{2}}{2}$.
    - Xét tam giác $SAO$ vuông tại $A$:
      $$\tan \widehat{SOA} = \frac{SA}{AO} = \frac{a\sqrt{2}}{\frac{a\sqrt{2}}{2}} = 2 \ne \sqrt{2}$$
    - Vậy tang của góc giữa hai mặt phẳng bằng $2$. Mệnh đề **c) Sai**.
  - Giao tuyến của $(SCD)$ và $(ABCD)$ là $CD$.
    - Ta có $CD \perp AD$ (do hình vuông) và $CD \perp SA \implies CD \perp (SAD) \implies CD \perp SD$.
    - Do đó, góc giữa mặt phẳng $(SCD)$ và $(ABCD)$ là góc $\widehat{SDA}$.
    - Tam giác $SAD$ vuông tại $A$ có $AD = a, SA = a\sqrt{2} \implies SD = \sqrt{a^2 + (a\sqrt{2})^2} = a\sqrt{3}$.
    - Do đó:
      $$\cos \widehat{SDA} = \frac{AD}{SD} = \frac{a}{a\sqrt{3}} = \frac{\sqrt{3}}{3}$$
    - Mệnh đề **d) Đúng**.

---

## PHẦN III. Câu trắc nghiệm trả lời ngắn (6 câu — 3.00 điểm)
*Thí sinh trả lời từ câu 1 đến câu 6. Mỗi câu trả lời đúng được 0,5 điểm.*

---

### Câu 1.
Một bồn chứa nước bằng inox có dạng khối lăng trụ đứng $ABC.A'B'C'$ với đáy $ABC$ là tam giác vuông tại $A$, $AB = 3\text{ m}, AC = 4\text{ m}$. Biết góc giữa đường thẳng $B'C$ và mặt phẳng đáy $(ABC)$ bằng $45^\circ$. Tính thể tích của bồn chứa nước đó theo đơn vị mét khối ($\text{m}^3$).

![Lăng trụ đứng tam giác Phần III Câu 1](output/images/de03_p3_cau01_langtru.png)

**Lời giải:**
- **Đáp số:** `30`
- Trong tam giác vuông $ABC$ tại $A$:
  $$BC = \sqrt{AB^2 + AC^2} = \sqrt{3^2 + 4^2} = 5\text{ m}$$
- Diện tích đáy $ABC$ là:
  $$S_{\triangle ABC} = \frac{1}{2} AB \cdot AC = \frac{1}{2} \cdot 3 \cdot 4 = 6\text{ m}^2$$
- Lăng trụ đứng nên $BB' \perp (ABC)$, suy ra hình chiếu vuông góc của $B'C$ lên mặt phẳng đáy $(ABC)$ là đoạn thẳng $BC$.
- Do đó, góc giữa đường thẳng $B'C$ và mặt phẳng $(ABC)$ là góc $\widehat{B'CB} = 45^\circ$.
- Xét tam giác vuông $B'BC$ tại $B$:
  $$BB' = BC \cdot \tan 45^\circ = 5 \cdot 1 = 5\text{ m}$$
- Thể tích của bồn chứa nước hình lăng trụ là:
  $$V = S_{\triangle ABC} \cdot BB' = 6 \cdot 5 = 30\text{ m}^3$$

---

### Câu 2.
Trong không gian với hệ tọa độ $Oxyz$, cho mặt cầu $(S): x^2 + y^2 + z^2 - 4x + 6y - 2z - 11 = 0$ và điểm $A(5; 1; 13)$. Gọi $M$ là một điểm di động trên mặt cầu $(S)$. Tìm khoảng cách lớn nhất giữa điểm $A$ và điểm $M$.

**Lời giải:**
- **Đáp số:** `18`
- Biến đổi phương trình mặt cầu $(S)$ về dạng chính tắc:
  $$(x - 2)^2 + (y + 3)^2 + (z - 1)^2 = 11 + 2^2 + (-3)^2 + 1^2 = 25$$
- Tâm và bán kính của mặt cầu $(S)$ là:
  $$I(2; -3; 1),\quad R = \sqrt{25} = 5$$
- Khoảng cách từ điểm $A(5; 1; 13)$ đến tâm $I$ là:
  $$IA = \sqrt{(5 - 2)^2 + (1 - (-3))^2 + (13 - 1)^2} = \sqrt{3^2 + 4^2 + 12^2} = \sqrt{9 + 16 + 144} = \sqrt{169} = 13$$
- Vì $IA = 13 > R = 5$ nên điểm $A$ nằm ngoài mặt cầu $(S)$.
- Với mọi điểm $M \in (S)$, theo bất đẳng thức tam giác ta có:
  $$AM \le IA + IM = IA + R = 13 + 5 = 18$$
- Dấu đẳng thức xảy ra khi tia $IA$ cắt mặt cầu tại điểm $M$ xa điểm $A$ nhất (tức $I$ nằm giữa $A$ và $M$).
- Vậy khoảng cách lớn nhất giữa $A$ và $M$ bằng $18$.

---

### Câu 3.
Trong không gian với hệ tọa độ $Oxyz$, cho mặt cầu $(S): (x - 1)^2 + (y - 2)^2 + (z + 3)^2 = 9$. Có hai mặt phẳng $(\alpha)$ song song với mặt phẳng $(P): 2x - 2y + z - 7 = 0$ và đồng thời tiếp xúc với mặt cầu $(S)$. Phương trình mặt phẳng tiếp xúc có hệ số tự do mang dấu dương có dạng $2x - 2y + z + D = 0$ ($D > 0$). Tìm giá trị của $D$.

**Lời giải:**
- **Đáp số:** `14`
- Mặt cầu $(S)$ có tâm $I(1; 2; -3)$ và bán kính $R = \sqrt{9} = 3$.
- Vì $(\alpha) \parallel (P)$ nên phương trình mặt phẳng $(\alpha)$ có dạng:
  $$2x - 2y + z + D = 0\quad (D \ne -7)$$
- Mặt phẳng $(\alpha)$ tiếp xúc với mặt cầu $(S)$ khi và chỉ khi khoảng cách từ tâm $I$ đến $(\alpha)$ bằng bán kính $R$:
  $$d(I, (\alpha)) = R \iff \frac{|2(1) - 2(2) + 1(-3) + D|}{\sqrt{2^2 + (-2)^2 + 1^2}} = 3$$
  $$\iff \frac{|2 - 4 - 3 + D|}{\sqrt{9}} = 3 \iff \frac{|D - 5|}{3} = 3 \iff |D - 5| = 9$$
- Giải phương trình chứa dấu giá trị tuyệt đối:
  $$\left[\begin{aligned} &D - 5 = 9 \implies D = 14 \\ &D - 5 = -9 \implies D = -4 \end{aligned}\right.$$
- Theo yêu cầu đề bài $D > 0$, do đó giá trị cần tìm là $D = 14$.

---

### Câu 4.
Trong không gian với hệ tọa độ $Oxyz$, cho hai đường thẳng chéo nhau:
$$d_1: \frac{x + 1}{2} = \frac{y - 1}{1} = \frac{z - 5}{-2}\quad \text{và}\quad d_2: \frac{x + 2}{4} = \frac{y - 5}{-1} = \frac{z - 6}{-1}$$
Đường vuông góc chung $\Delta$ của $d_1$ và $d_2$ cắt $d_1$ tại điểm $M(a; b; c)$. Tính giá trị của biểu thức $T = a + b + c$.

**Lời giải:**
- **Đáp số:** `6`
- Đường thẳng $d_1$ có vectơ chỉ phương $\vec{u}_1 = (2; 1; -2)$. Điểm $M \in d_1$ có tọa độ phụ thuộc tham số $t$:
  $$M(-1 + 2t;\, 1 + t;\, 5 - 2t)$$
- Đường thẳng $d_2$ có vectơ chỉ phương $\vec{u}_2 = (4; -1; -1)$. Điểm $N \in d_2$ có tọa độ phụ thuộc tham số $s$:
  $$N(-2 + 4s;\, 5 - s;\, 6 - s)$$
- Vectơ chỉ phương của đường vuông góc chung là $\vec{MN}$:
  $$\vec{MN} = (-1 + 4s - 2t;\, 4 - s - t;\, 1 - s + 2t)$$
- Vì $MN$ là đoạn vuông góc chung nên:
  $$\left\{\begin{aligned} &\vec{MN} \cdot \vec{u}_1 = 0 \\ &\vec{MN} \cdot \vec{u}_2 = 0 \end{aligned}\right.$$
- Ta có hệ phương trình:
  $$\left\{\begin{aligned} &2(-1 + 4s - 2t) + 1(4 - s - t) - 2(1 - s + 2t) = 0 \\ &4(-1 + 4s - 2t) - 1(4 - s - t) - 1(1 - s + 2t) = 0 \end{aligned}\right.$$
  $$\iff \left\{\begin{aligned} &9s - 9t = 0 \\ &18s - 9t - 9 = 0 \end{aligned}\right. \iff \left\{\begin{aligned} &s = t \\ &9t = 9 \end{aligned}\right. \iff s = t = 1$$
- Thay $t = 1$ vào tọa độ điểm $M$:
  $$M(-1 + 2(1);\, 1 + 1;\, 5 - 2(1)) \implies M(1; 2; 3)$$
- Vậy $a = 1, b = 2, c = 3 \implies T = a + b + c = 1 + 2 + 3 = 6$.

---

### Câu 5.
Tìm số nghiệm nguyên của bất phương trình logarit sau:
$$\log_2(x^2 - 2x) \le 3$$

**Lời giải:**
- **Đáp số:** `4`
- Điều kiện xác định:
  $$x^2 - 2x > 0 \iff x(x - 2) > 0 \iff \left[\begin{aligned} &x < 0 \\ &x > 2 \end{aligned}\right.$$
- Vì cơ số $2 > 1$, bất phương trình tương đương:
  $$x^2 - 2x \le 2^3 \iff x^2 - 2x - 8 \le 0$$
- Tam thức bậc hai $x^2 - 2x - 8 = (x + 2)(x - 4)$ có hai nghiệm $-2$ và $4$. Do đó:
  $$-2 \le x \le 4$$
- Kết hợp với điều kiện xác định, ta được tập nghiệm của bất phương trình là:
  $$S = [-2; 0) \cup (2; 4]$$
- Các giá trị nguyên thuộc tập nghiệm $S$ là:
  $$x \in \{-2;\, -1;\, 3;\, 4\}$$
- Vậy có tất cả $4$ nghiệm nguyên thỏa mãn.

---

### Câu 6.
Biết rằng tích phân $I = \int_0^1 \frac{4x + 7}{x^2 + 3x + 2}\,\mathrm{d}x = a\ln 2 + b\ln 3$, trong đó $a, b$ là các số nguyên. Tính giá trị của biểu thức $T = 3a + 2b$.

**Lời giải:**
- **Đáp số:** `8`
- Ta phân tích đa thức mẫu số thành nhân tử: $x^2 + 3x + 2 = (x + 1)(x + 2)$.
- Tách phân thức thành tổng các phân thức đơn giản:
  $$\frac{4x + 7}{(x + 1)(x + 2)} = \frac{A}{x + 1} + \frac{B}{x + 2}$$
  $$\implies A(x + 2) + B(x + 1) = 4x + 7$$
  - Cho $x = -1 \implies A(-1 + 2) = 4(-1) + 7 \implies A = 3$.
  - Cho $x = -2 \implies B(-2 + 1) = 4(-2) + 7 \implies -B = -1 \implies B = 1$.
- Do đó:
  $$\frac{4x + 7}{x^2 + 3x + 2} = \frac{3}{x + 1} + \frac{1}{x + 2}$$
- Tính tích phân:
  $$I = \int_0^1 \left(\frac{3}{x + 1} + \frac{1}{x + 2}\right)\,\mathrm{d}x = \left[ 3\ln|x + 1| + \ln|x + 2| \right]_0^1$$
  $$= (3\ln 2 + \ln 3) - (3\ln 1 + \ln 2) = 2\ln 2 + \ln 3$$
- Đối chiếu với đề bài $I = a\ln 2 + b\ln 3$, ta suy ra:
  $$a = 2,\quad b = 1$$
- Giá trị của biểu thức $T$ là:
  $$T = 3a + 2b = 3(2) + 2(1) = 6 + 2 = 8$$

---
*--- HẾT ---*

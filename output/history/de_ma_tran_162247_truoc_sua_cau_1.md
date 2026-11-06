# ĐỀ KIỂM TRA CHUYÊN ĐỀ: ỨNG DỤNG ĐẠO HÀM KHẢO SÁT VÀ VẼ ĐỒ THỊ HÀM SỐ
**Môn: Toán 12 — Chương trình THPT Quốc Gia (Cấu trúc mới)**  
*Cấu trúc đề: 5 câu Trắc nghiệm 4 lựa chọn • 2 câu Trắc nghiệm Đúng/Sai • 2 câu Trả lời ngắn*  
*(Toàn bộ câu hỏi và đáp án đã được kiểm chứng tự động bằng Python SymPy)*

---

---

---

## PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn (5 câu)

---

### Câu 1.
Cho hàm số $y = x^3 - 3x^2 - 24x + 7$. Hàm số đã cho nghịch biến trên khoảng nào dưới đây?
- **A.** $(-\infty; -2)$
- **B.** $(-2; 4)$
- **C.** $(4; +\infty)$
- **D.** $(-4; 2)$

**Lời giải:**
- **Đáp án đúng:** B
- Tập xác định: $\mathcal{D} = \mathbb{R}$.
- Ta có đạo hàm:
  $$y' = 3x^2 - 6x - 24 = 3(x + 2)(x - 4)$$
- Cho $y' < 0 \iff 3(x + 2)(x - 4) < 0 \iff -2 < x < 4$.
- Vậy hàm số nghịch biến trên khoảng $(-2; 4)$.

---

### Câu 2.
Cho hàm số $y = x^4 - 2x^2 + 3$. Giá trị cực tiểu của hàm số đã cho bằng
- **A.** $3$
- **B.** $2$
- **C.** $1$
- **D.** $-1$

**Lời giải:**
#### Câu 2 — Chọn B
- Tập xác định: $\mathcal{D} = \mathbb{R}$.
- Ta có đạo hàm:
  $$y' = 4x^3 - 4x = 4x(x^2 - 1)$$
- Cho $y' = 0 \iff x = 0$ hoặc $x = \pm 1$.
- Đạo hàm cấp hai $y'' = 12x^2 - 4$. Tại $x = \pm 1$, ta có $y''(\pm 1) = 8 > 0$ nên $x = \pm 1$ là các điểm cực tiểu của hàm số.
- Giá trị cực tiểu của hàm số là:
  $$y_{\text{CT}} = y(\pm 1) = (\pm 1)^4 - 2(\pm 1)^2 + 3 = 2$$

---

### Câu 3.
Giá trị lớn nhất của hàm số $y = x^3 - 3x + 4$ trên đoạn $[0; 2]$ bằng
- **A.** $4$
- **B.** $2$
- **C.** $6$
- **D.** $8$

**Lời giải:**
#### Câu 3 — Chọn C
- Hàm số $y = x^3 - 3x + 4$ xác định và liên tục trên đoạn $[0; 2]$.
- Ta có đạo hàm:
  $$y' = 3x^2 - 3 = 0 \iff \left[\begin{array}{l} x = 1 \in [0; 2] \\ x = -1 \notin [0; 2] \end{array}\right.$$
- Tính giá trị của hàm số tại hai đầu mút và điểm dừng:
  $$y(0) = 4, \quad y(1) = 2, \quad y(2) = 2^3 - 3 \cdot 2 + 4 = 6$$
- Vậy $\max_{[0; 2]} y = 6$ tại $x = 2$.

---

### Câu 4.
Đường tiệm cận xiên của đồ thị hàm số $y = \dfrac{2x^2 - 3x + 5}{x - 2}$ là đường thẳng có phương trình
- **A.** $y = 2x - 3$
- **B.** $y = 2x - 1$
- **C.** $y = x - 2$
- **D.** $y = 2x + 1$

**Lời giải:**
#### Câu 4 — Chọn D
- Tập xác định: $\mathcal{D} = \mathbb{R} \setminus \{2\}$.
- Thực hiện phép chia đa thức tử cho mẫu:
  $$y = \dfrac{2x^2 - 3x + 5}{x - 2} = \dfrac{(2x + 1)(x - 2) + 7}{x - 2} = 2x + 1 + \dfrac{7}{x - 2}$$
- Vì $\lim_{x \to \pm\infty} \left[y - (2x + 1)\right] = \lim_{x \to \pm\infty} \dfrac{7}{x - 2} = 0$, nên đường thẳng $y = 2x + 1$ là tiệm cận xiên của đồ thị hàm số.

---

### Câu 5.
Có bao nhiêu giá trị nguyên của tham số $m \in [-10; 10]$ để hàm số $y = \dfrac{1}{3}x^3 - mx^2 + (2m + 3)x + 1$ đồng biến trên $\mathbb{R}$?
- **A.** $4$
- **B.** $5$
- **C.** $3$
- **D.** $6$

**Lời giải:**
#### Câu 5 — Chọn B
- Tập xác định: $\mathcal{D} = \mathbb{R}$.
- Ta có đạo hàm:
  $$y' = x^2 - 2mx + 2m + 3$$
- Hàm số đồng biến trên $\mathbb{R}$ khi và chỉ khi:
  $$y' \ge 0, \forall x \in \mathbb{R} \iff \begin{cases} a = 1 > 0 \\ \Delta' = (-m)^2 - (2m + 3) \le 0 \end{cases}$$
- Giải bất phương trình:
  $$m^2 - 2m - 3 \le 0 \iff (m + 1)(m - 3) \le 0 \iff -1 \le m \le 3$$
- Vì $m \in \mathbb{Z}$, nên $m \in \{-1; 0; 1; 2; 3\}$. Có tất cả $5$ giá trị nguyên của $m$.

---

## PHẦN II. Câu trắc nghiệm Đúng/Sai (2 câu)

---

### Câu 1.
Cho hàm số $y = f(x) = \dfrac{2x - 1}{x + 1}$ có đồ thị $(C)$. Xét tính đúng sai của các mệnh đề sau:
- **a)** Tập xác định của hàm số là $\mathcal{D} = \mathbb{R} \setminus \{-1\}$ và đạo hàm $f'(x) = \dfrac{3}{(x + 1)^2} > 0, \forall x \neq -1$.
- **b)** Đồ thị $(C)$ có đường tiệm cận ngang là $y = -1$ và đường tiệm cận đứng là $x = 2$.
- **c)** Tâm đối xứng của đồ thị $(C)$ là điểm $I(-1; 2)$.
- **d)** Đường thẳng $d: y = -x + 3$ cắt đồ thị $(C)$ tại hai điểm phân biệt $A, B$ sao cho độ dài đoạn thẳng $AB = 4\sqrt{2}$.

**Lời giải:**
#### Câu 1.
Xét hàm số $y = f(x) = \dfrac{2x - 1}{x + 1}$:
- **a) Đúng.** Điều kiện xác định $x + 1 \neq 0 \iff x \neq -1$, suy ra $\mathcal{D} = \mathbb{R} \setminus \{-1\}$. Đạo hàm:
  $$f'(x) = \dfrac{2 \cdot 1 - 1 \cdot (-1)}{(x + 1)^2} = \dfrac{3}{(x + 1)^2} > 0, \quad \forall x \neq -1$$
- **b) Sai.** Ta có $\lim_{x \to \pm\infty} f(x) = 2$ nên tiệm cận ngang là $y = 2$; $\lim_{x \to (-1)^+} f(x) = -\infty$ và $\lim_{x \to (-1)^-} f(x) = +\infty$ nên tiệm cận đứng là $x = -1$.
- **c) Đúng.** Tâm đối xứng của đồ thị hàm phân thức bậc nhất trên bậc nhất là giao điểm của tiệm cận đứng $x = -1$ và tiệm cận ngang $y = 2$, tức là điểm $I(-1; 2)$.
- **d) Đúng.** Phương trình hoành độ giao điểm của $(C)$ và $d: y = -x + 3$ (với $x \neq -1$):
  $$\dfrac{2x - 1}{x + 1} = -x + 3 \iff 2x - 1 = (-x + 3)(x + 1) \iff 2x - 1 = -x^2 + 2x + 3 \iff x^2 = 4 \iff x = \pm 2$$
  Suy ra tọa độ hai giao điểm là $A(-2; 5)$ và $B(2; 1)$. Độ dài đoạn thẳng $AB$ là:
  $$AB = \sqrt{(2 - (-2))^2 + (1 - 5)^2} = \sqrt{16 + 16} = 4\sqrt{2}$$

---

### Câu 2.
Cho hàm số $y = f(x) = \dfrac{x^2 - 2x + 5}{x - 1}$ có đồ thị $(C)$. Xét tính đúng sai của các mệnh đề sau:
- **a)** Với mọi $x \neq 1$, hàm số có thể viết lại dưới dạng $f(x) = x - 1 + \dfrac{4}{x - 1}$.
- **b)** Hàm số đạt cực đại tại $x = 3$ và đạt cực tiểu tại $x = -1$.
- **c)** Đường thẳng đi qua hai điểm cực trị của đồ thị $(C)$ có phương trình là $y = 2x - 2$.
- **d)** Khoảng cách từ tâm đối xứng $I$ của đồ thị $(C)$ đến đường tiệm cận xiên của nó bằng $\sqrt{2}$.

**Lời giải:**
#### Câu 2.
Xét hàm số $y = f(x) = \dfrac{x^2 - 2x + 5}{x - 1}$:
- **a) Đúng.** Với $x \neq 1$, ta có:
  $$f(x) = \dfrac{(x - 1)^2 + 4}{x - 1} = x - 1 + \dfrac{4}{x - 1}$$
- **b) Sai.** Đạo hàm của hàm số là:
  $$f'(x) = 1 - \dfrac{4}{(x - 1)^2} = \dfrac{(x - 1)^2 - 4}{(x - 1)^2} = \dfrac{(x + 1)(x - 3)}{(x - 1)^2}$$
  Cho $f'(x) = 0 \iff x = -1$ hoặc $x = 3$.
  - Qua $x = -1$, $f'(x)$ đổi dấu từ $+$ sang $-$ nên hàm số đạt **cực đại** tại $x = -1$ ($y_{\text{CĐ}} = -4$).
  - Qua $x = 3$, $f'(x)$ đổi dấu từ $-$ sang $+$ nên hàm số đạt **cực tiểu** tại $x = 3$ ($y_{\text{CT}} = 4$).
  Do đó mệnh đề phát biểu ngược vị trí cực đại và cực tiểu.
- **c) Đúng.** Hai điểm cực trị của đồ thị $(C)$ là $A(-1; -4)$ và $B(3; 4)$. Đường thẳng đi qua hai điểm cực trị có phương trình:
  $$y = \dfrac{(x^2 - 2x + 5)'}{(x - 1)'} = 2x - 2$$
  (Thay tọa độ $A(-1; -4)$ và $B(3; 4)$ đều thỏa mãn $y = 2x - 2$).
- **d) Sai.** Đồ thị $(C)$ có tiệm cận đứng $x = 1$ và tiệm cận xiên $y = x - 1$. Tâm đối xứng $I(1; 0)$ chính là giao điểm của tiệm cận đứng và tiệm cận xiên, nên $I$ nằm trên đường tiệm cận xiên. Do đó khoảng cách từ $I$ đến đường tiệm cận xiên bằng $0$ (không phải $\sqrt{2}$).

---

## PHẦN III. Câu trắc nghiệm trả lời ngắn (2 câu)

---

### Câu 1.
Một doanh nghiệp sản xuất một loại sản phẩm. Chi phí để sản xuất $x$ (đơn vị: trăm sản phẩm, $0 < x \le 13$) trong một tháng được mô hình hóa bởi hàm số $C(x) = x^3 - 6x^2 + 15x + 20$ (triệu đồng). Giá bán mỗi trăm sản phẩm phụ thuộc vào sản lượng theo hàm cầu $p(x) = 39 - 3x$ (triệu đồng). Giả sử toàn bộ sản phẩm sản xuất ra đều được bán hết. Hỏi doanh nghiệp cần sản xuất bao nhiêu trăm sản phẩm trong một tháng để lợi nhuận thu được là lớn nhất?

- **Đáp số:** `....`

**Lời giải:**
#### Câu 1 — Đáp số: `4`
- Doanh thu khi bán hết $x$ trăm sản phẩm là:
  $$R(x) = x \cdot p(x) = x(39 - 3x) = 39x - 3x^2 \text{ (triệu đồng)}$$
- Hàm lợi nhuận $L(x)$ thu được trong tháng là:
  $$L(x) = R(x) - C(x) = (39x - 3x^2) - (x^3 - 6x^2 + 15x + 20) = -x^3 + 3x^2 + 24x - 20$$
- Xét hàm số $L(x)$ với $x \in (0; 13]$, ta có đạo hàm:
  $$L'(x) = -3x^2 + 6x + 24 = -3(x^2 - 2x - 8) = -3(x - 4)(x + 2)$$
- Cho $L'(x) = 0 \implies x = 4 \in (0; 13]$ (vì $x = -2 < 0$ loại).
- Trên khoảng $(0; 4)$, $L'(x) > 0$ (hàm đồng biến); trên khoảng $(4; 13)$, $L'(x) < 0$ (hàm nghịch biến).
- Do đó lợi nhuận đạt giá trị lớn nhất bằng $L(4) = 60$ (triệu đồng) khi sản xuất $x = 4$ (trăm sản phẩm).

---

### Câu 2.
Cho hàm số bậc ba $y = f(x) = x^3 - 3x^2 - 9x + 12$ có đồ thị $(C)$. Gọi $A$ và $B$ là hai điểm cực trị của đồ thị $(C)$. Tính diện tích tam giác $OAB$ (với $O$ là gốc tọa độ).

- **Đáp số:** `....`

**Lời giải:**
#### Câu 2 — Đáp số: `18`
- Tập xác định: $\mathcal{D} = \mathbb{R}$.
- Ta có đạo hàm:
  $$f'(x) = 3x^2 - 6x - 9 = 3(x + 1)(x - 3)$$
- Cho $f'(x) = 0 \iff x = -1$ hoặc $x = 3$:
  - Với $x = -1 \implies y = (-1)^3 - 3(-1)^2 - 9(-1) + 12 = 17 \implies A(-1; 17)$.
  - Với $x = 3 \implies y = 3^3 - 3 \cdot 3^2 - 9 \cdot 3 + 12 = -15 \implies B(3; -15)$.
- Ta có $\overrightarrow{OA} = (-1; 17)$ và $\overrightarrow{OB} = (3; -15)$.
- Diện tích tam giác $OAB$ là:
  $$S_{\triangle OAB} = \dfrac{1}{2}\left|x_A y_B - x_B y_A\right| = \dfrac{1}{2}\left|(-1) \cdot (-15) - 3 \cdot 17\right| = \dfrac{1}{2}\left|15 - 51\right| = \dfrac{36}{2} = 18$$

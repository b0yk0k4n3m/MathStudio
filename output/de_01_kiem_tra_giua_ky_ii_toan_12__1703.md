# ĐỀ KIỂM TRA ĐỊNH KỲ GIỮA HỌC KỲ II — MÔN TOÁN 12
**NĂM HỌC 2025 – 2026**  
*Thời gian làm bài: 90 phút (không kể thời gian phát đề)*  
*Cấu trúc: 20 câu (70% Trắc nghiệm khách quan + 30% Tự luận) — Thang điểm 10*  
*(Đề thi và toàn bộ đáp án đã được kiểm chứng độc lập bằng Python SymPy)*

---

### KHUNG MA TRẬN ĐỀ THI BẮT BUỘC
- **Mức độ nhận thức:** Nhận biết: 8 câu (40%) | Thông hiểu: 7 câu (35%) | Vận dụng: 5 câu (25%) | Vận dụng cao: 0 câu.
- **Phần I:** Trắc nghiệm 4 lựa chọn (12 câu – 3,0 điểm): 8 Nhận biết, 4 Thông hiểu.
- **Phần II:** Trắc nghiệm Đúng/Sai (2 câu lớn, 8 lệnh hỏi – 2,0 điểm): 2 Vận dụng.
- **Phần III:** Trắc nghiệm trả lời ngắn (4 câu – 2,0 điểm): 2 Thông hiểu, 2 Vận dụng.
- **Phần IV:** Tự luận (2 câu – 3,0 điểm): 1 Thông hiểu, 1 Vận dụng.

---

## PHẦN I. Câu trắc nghiệm nhiều phương án lựa chọn (12 câu – 3,0 điểm)
*Thí sinh trả lời từ Câu 1 đến Câu 12. Mỗi câu hỏi chỉ chọn một phương án đúng nhất. Mỗi câu trả lời đúng được 0,25 điểm.*

---

### Câu 1.
Họ tất cả các nguyên hàm của hàm số $f(x) = 3x^2 + \cos x$ trên $\mathbb{R}$ là
- **A.** $x^3 - \sin x + C$.
- **B.** $x^3 + \sin x + C$.
- **C.** $6x - \sin x + C$.
- **D.** $x^3 + \cos x + C$.

**Lời giải:**
#### Câu 1 — Chọn B
- Áp dụng bảng nguyên hàm cơ bản của hàm đa thức và hàm lượng giác:
  $$\int (3x^2 + \cos x) dx = 3 \int x^2 dx + \int \cos x dx = 3 \cdot \dfrac{x^3}{3} + \sin x + C = x^3 + \sin x + C$$
- Vậy họ nguyên hàm cần tìm là $x^3 + \sin x + C$.

---

### Câu 2.
Cho hai hàm số $f(x), g(x)$ liên tục trên khoảng $K$ và $k$ là một hằng số thực khác $0$. Khẳng định nào sau đây **sai**?
- **A.** $\int [f(x) + g(x)] dx = \int f(x) dx + \int g(x) dx$.
- **B.** $\int k f(x) dx = k \int f(x) dx$.
- **C.** $\int [f(x) \cdot g(x)] dx = \int f(x) dx \cdot \int g(x) dx$.
- **D.** $\left(\int f(x) dx\right)' = f(x)$.

**Lời giải:**
#### Câu 2 — Chọn C
- Theo tính chất của nguyên hàm:
  - Phép lấy nguyên hàm có tính chất tuyến tính đối với phép cộng và phép nhân với hằng số: $\int [f(x) + g(x)] dx = \int f(x) dx + \int g(x) dx$ và $\int k f(x) dx = k \int f(x) dx$ ($k \ne 0$).
  - Đạo hàm của nguyên hàm là chính hàm số dưới dấu tích phân: $\left(\int f(x) dx\right)' = f(x)$.
  - Phép lấy nguyên hàm **không có tính chất nhân**: $\int [f(x) \cdot g(x)] dx \ne \int f(x) dx \cdot \int g(x) dx$.
- Do đó phương án C là khẳng định sai.

---

### Câu 3.
Nếu $\int_1^3 f(x) dx = 4$ và $\int_3^5 f(x) dx = -2$ thì giá trị của $\int_1^5 f(x) dx$ bằng
- **A.** $2$.
- **B.** $6$.
- **C.** $-6$.
- **D.** $-8$.

**Lời giải:**
#### Câu 3 — Chọn A
- Áp dụng tính chất chèn cận của tích phân xác định với hàm số $f(x)$ liên tục trên $[1; 5]$:
  $$\int_1^5 f(x) dx = \int_1^3 f(x) dx + \int_3^5 f(x) dx = 4 + (-2) = 2$$

---

### Câu 4.
Cho biết $\int_0^1 f(x) dx = 3$. Giá trị của tích phân $\int_0^1 [2f(x) - 1] dx$ bằng
- **A.** $4$.
- **B.** $6$.
- **C.** $7$.
- **D.** $5$.

**Lời giải:**
#### Câu 4 — Chọn D
- Áp dụng các tính chất cơ bản của tích phân:
  $$\int_0^1 [2f(x) - 1] dx = 2 \int_0^1 f(x) dx - \int_0^1 1 dx = 2 \cdot 3 - [x]_0^1 = 6 - (1 - 0) = 5$$

---

### Câu 5.
Tích phân $I = \int_0^1 (3x^2 + 2e^x) dx$ có giá trị bằng
- **A.** $2e - 1$.
- **B.** $2e + 1$.
- **C.** $e - 1$.
- **D.** $2e$.

**Lời giải:**
#### Câu 5 — Chọn A
- Ta tìm nguyên hàm của biểu thức dưới dấu tích phân:
  $$\int (3x^2 + 2e^x) dx = x^3 + 2e^x$$
- Áp dụng công thức Newton – Leibniz:
  $$I = [x^3 + 2e^x]_0^1 = (1^3 + 2e^1) - (0^3 + 2e^0) = (1 + 2e) - 2 = 2e - 1$$

---

### Câu 6.
Trong không gian $Oxyz$, cho vectơ $\vec{u} = 2\vec{i} - 3\vec{j} + 5\vec{k}$ (với $\vec{i}, \vec{j}, \vec{k}$ lần lượt là các vectơ đơn vị trên các trục $Ox, Oy, Oz$). Tọa độ của vectơ $\vec{u}$ là
- **A.** $(2; 3; 5)$.
- **B.** $(-2; 3; -5)$.
- **C.** $(2; -3; 5)$.
- **D.** $(5; -3; 2)$.

**Lời giải:**
#### Câu 6 — Chọn C
- Theo định nghĩa tọa độ vectơ trong hệ tọa độ $Oxyz$:
  $$\vec{u} = x\vec{i} + y\vec{j} + z\vec{k} \iff \vec{u} = (x; y; z)$$
- Do đó với $\vec{u} = 2\vec{i} - 3\vec{j} + 5\vec{k}$, ta có tọa độ của $\vec{u}$ là $(2; -3; 5)$.

---

### Câu 7.
Trong không gian $Oxyz$, cho hai điểm $A(1; 2; -1)$ và $B(3; 0; 0)$. Độ dài của đoạn thẳng $AB$ bằng
- **A.** $\sqrt{5}$.
- **B.** $3$.
- **C.** $9$.
- **D.** $\sqrt{13}$.

**Lời giải:**
#### Câu 7 — Chọn B
- Ta có tọa độ vectơ $\overrightarrow{AB} = (3 - 1; 0 - 2; 0 - (-1)) = (2; -2; 1)$.
- Độ dài đoạn thẳng $AB$ chính là độ dài của vectơ $\overrightarrow{AB}$:
  $$AB = |\overrightarrow{AB}| = \sqrt{2^2 + (-2)^2 + 1^2} = \sqrt{4 + 4 + 1} = \sqrt{9} = 3$$

---

### Câu 8.
Trong không gian $Oxyz$, cho hai vectơ $\vec{u} = (1; 0; -1)$ và $\vec{v} = (1; 1; 0)$. Góc giữa hai vectơ $\vec{u}$ và $\vec{v}$ bằng
- **A.** $30^\circ$.
- **B.** $45^\circ$.
- **C.** $120^\circ$.
- **D.** $60^\circ$.

**Lời giải:**
#### Câu 8 — Chọn D
- Ta tính tích vô hướng và độ dài của hai vectơ:
  $$\vec{u} \cdot \vec{v} = 1 \cdot 1 + 0 \cdot 1 + (-1) \cdot 0 = 1$$
  $$|\vec{u}| = \sqrt{1^2 + 0^2 + (-1)^2} = \sqrt{2}, \quad |\vec{v}| = \sqrt{1^2 + 1^2 + 0^2} = \sqrt{2}$$
- Côsin của góc giữa hai vectơ là:
  $$\cos(\vec{u}, \vec{v}) = \dfrac{\vec{u} \cdot \vec{v}}{|\vec{u}| \cdot |\vec{v}|} = \dfrac{1}{\sqrt{2} \cdot \sqrt{2}} = \dfrac{1}{2}$$
- Suy ra số đo góc giữa hai vectơ là $(\vec{u}, \vec{v}) = 60^\circ$.

---

### Câu 9.
Trong không gian $Oxyz$, cho mặt phẳng $(P): 2x - 3y + z - 4 = 0$. Một vectơ pháp tuyến của mặt phẳng $(P)$ là
- **A.** $\vec{n}_1 = (2; -3; 1)$.
- **B.** $\vec{n}_2 = (2; 3; 1)$.
- **C.** $\vec{n}_3 = (2; -3; -4)$.
- **D.** $\vec{n}_4 = (-3; 1; -4)$.

**Lời giải:**
#### Câu 9 — Chọn A
- Mặt phẳng có phương trình tổng quát $Ax + By + Cz + D = 0$ nhận vectơ $\vec{n} = (A; B; C)$ làm vectơ pháp tuyến.
- Với $(P): 2x - 3y + z - 4 = 0$, ta có $A = 2, B = -3, C = 1$ nên một vectơ pháp tuyến của $(P)$ là $\vec{n}_1 = (2; -3; 1)$.

---

### Câu 10.
Trong không gian $Oxyz$, phương trình tổng quát của mặt phẳng đi qua điểm $M(1; 2; -3)$ và nhận vectơ $\vec{n} = (2; -1; 4)$ làm vectơ pháp tuyến là
- **A.** $2x - y + 4z - 12 = 0$.
- **B.** $2x - y + 4z - 8 = 0$.
- **C.** $2x - y + 4z + 12 = 0$.
- **D.** $x + 2y - 3z + 12 = 0$.

**Lời giải:**
#### Câu 10 — Chọn C
- Phương trình mặt phẳng đi qua điểm $M(x_0; y_0; z_0)$ nhận $\vec{n} = (A; B; C)$ làm VTPT có dạng:
  $$A(x - x_0) + B(y - y_0) + C(z - z_0) = 0$$
- Thay số ta có:
  $$2(x - 1) - 1(y - 2) + 4(z + 3) = 0 \iff 2x - 2 - y + 2 + 4z + 12 = 0 \iff 2x - y + 4z + 12 = 0$$

---

### Câu 11.
Cho hai biến cố $A$ và $B$ có liên quan đến cùng một phép thử ngẫu nhiên, với $P(B) > 0$. Công thức tính xác suất có điều kiện của biến cố $A$ khi biết biến cố $B$ đã xảy ra là
- **A.** $P(A|B) = \dfrac{P(AB)}{P(A)}$.
- **B.** $P(A|B) = \dfrac{P(AB)}{P(B)}$.
- **C.** $P(A|B) = P(A) \cdot P(B)$.
- **D.** $P(A|B) = \dfrac{P(B)}{P(AB)}$.

**Lời giải:**
#### Câu 11 — Chọn B
- Theo định nghĩa xác suất có điều kiện trong chương trình Toán 12: Với hai biến cố $A$ và $B$ ($P(B) > 0$), xác suất của biến cố $A$ với điều kiện biến cố $B$ đã xảy ra được ký hiệu và tính bởi công thức:
  $$P(A|B) = \dfrac{P(AB)}{P(B)}$$

---

### Câu 12.
Cho hai biến cố $A$ và $B$ thỏa mãn $P(A) = 0{,}6$; $P(B) = 0{,}5$ và $P(AB) = 0{,}3$. Xác suất có điều kiện $P(A|B)$ bằng
- **A.** $0{,}5$.
- **B.** $0{,}3$.
- **C.** $0{,}8$.
- **D.** $0{,}6$.

**Lời giải:**
#### Câu 12 — Chọn D
- Áp dụng định nghĩa xác suất có điều kiện:
  $$P(A|B) = \dfrac{P(AB)}{P(B)} = \dfrac{0{,}3}{0{,}5} = 0{,}6$$

---

## PHẦN II. Câu trắc nghiệm Đúng/Sai (2 câu – 2,0 điểm)
*Thí sinh trả lời từ Câu 1 đến Câu 2. Trong mỗi ý a), b), c), d) ở mỗi câu, thí sinh chọn Đúng hoặc Sai.*  
*Điểm số mỗi câu: Đúng 1 ý: 0,10 điểm | Đúng 2 ý: 0,25 điểm | Đúng 3 ý: 0,50 điểm | Đúng cả 4 ý: 1,00 điểm.*

---

### Câu 1.
Cho hình phẳng $(H)$ giới hạn bởi đồ thị của hàm số bậc hai (parabol) $(P): y = -x^2 + 4x$ và đường thẳng $d: y = x$. Xét tính đúng sai của các mệnh đề sau:
- **a)** Hoành độ giao điểm của parabol $(P)$ và đường thẳng $d$ là các nghiệm của phương trình $-x^2 + 3x = 0$, gồm $x = 0$ và $x = 3$.
- **b)** Trên đoạn $[0; 3]$, ta luôn có $-x^2 + 4x \ge x$, do đó diện tích hình phẳng $(H)$ được xác định bởi công thức $S = \int_0^3 (-x^2 + 3x) dx$.
- **c)** Diện tích của hình phẳng $(H)$ bằng $\dfrac{9}{2}$ (đơn vị diện tích).
- **d)** Thể tích khối tròn xoay tạo thành khi quay hình phẳng $(H)$ quanh trục hoành $Ox$ bằng $\dfrac{27\pi}{2}$ (đơn vị thể tích).

**Lời giải:**
#### Câu 1.
- **a) Đúng.** Phương trình hoành độ giao điểm của $(P)$ và $d$:
  $$-x^2 + 4x = x \iff -x^2 + 3x = 0 \iff x(3 - x) = 0 \iff \left[\begin{array}{l} x = 0 \\ x = 3 \end{array}\right.$$
- **b) Đúng.** Xét hiệu hai hàm số $g(x) = (-x^2 + 4x) - x = -x^2 + 3x$. Vì tam thức bậc hai này có hai nghiệm là $0$ và $3$, hệ số $a = -1 < 0$ nên $g(x) \ge 0, \forall x \in [0; 3]$.
  Do đó parabol $(P)$ nằm phía trên đường thẳng $d$ trên đoạn $[0; 3]$, suy ra:
  $$S = \int_0^3 |(-x^2 + 4x) - x| dx = \int_0^3 (-x^2 + 3x) dx$$
- **c) Đúng.** Ta thực hiện tính tích phân:
  $$S = \int_0^3 (-x^2 + 3x) dx = \left[ -\dfrac{x^3}{3} + \dfrac{3x^2}{2} \right]_0^3 = \left( -\dfrac{27}{3} + \dfrac{3 \cdot 9}{2} \right) - 0 = -9 + \dfrac{27}{2} = \dfrac{9}{2}$$
- **d) Sai.** Khối tròn xoay tạo thành khi quay hình phẳng giới hạn bởi hai đồ thị hàm số không âm $y_1 = -x^2 + 4x$ và $y_2 = x$ (với $y_1 \ge y_2 \ge 0$ trên $[0; 3]$) quanh trục $Ox$ có thể tích là:
  $$V = \pi \int_0^3 \left[ (-x^2 + 4x)^2 - x^2 \right] dx$$
  Ta có:
  $$(-x^2 + 4x)^2 - x^2 = x^4 - 8x^3 + 16x^2 - x^2 = x^4 - 8x^3 + 15x^2$$
  Do đó:
  $$V = \pi \left[ \dfrac{x^5}{5} - 2x^4 + 5x^3 \right]_0^3 = \pi \left( \dfrac{243}{5} - 2 \cdot 81 + 5 \cdot 27 \right) = \pi \left( \dfrac{243}{5} - 162 + 135 \right) = \pi \left( \dfrac{243}{5} - 27 \right) = \dfrac{108\pi}{5}$$
  Vì $\dfrac{108\pi}{5} \ne \dfrac{27\pi}{2}$, mệnh đề d là Sai.

---

### Câu 2.
Trong không gian với hệ tọa độ $Oxyz$, cho ba điểm $A(1; 1; 0)$, $B(0; 2; 1)$, $C(1; 0; 2)$ và điểm $M(2; 3; -1)$. Xét tính đúng sai của các mệnh đề sau:
- **a)** Tọa độ của các vectơ chỉ phương là $\overrightarrow{AB} = (-1; 1; 1)$ và $\overrightarrow{AC} = (0; -1; 2)$.
- **b)** Tích có hướng của hai vectơ $[\overrightarrow{AB}, \overrightarrow{AC}] = (3; 2; 1)$, do đó một vectơ pháp tuyến của mặt phẳng $(ABC)$ là $\vec{n} = (3; 2; 1)$.
- **c)** Mặt phẳng $(ABC)$ có phương trình tổng quát là $3x + 2y + z + 5 = 0$.
- **d)** Khoảng cách từ điểm $M(2; 3; -1)$ đến mặt phẳng $(ABC)$ bằng $\dfrac{3\sqrt{14}}{7}$.

**Lời giải:**
#### Câu 2.
- **a) Đúng.** Ta tính tọa độ các vectơ:
  $$\overrightarrow{AB} = (0 - 1; 2 - 1; 1 - 0) = (-1; 1; 1)$$
  $$\overrightarrow{AC} = (1 - 1; 0 - 1; 2 - 0) = (0; -1; 2)$$
- **b) Đúng.** Tích có hướng của hai vectơ $\overrightarrow{AB}$ và $\overrightarrow{AC}$ là:
  $$[\overrightarrow{AB}, \overrightarrow{AC}] = \left( \begin{vmatrix} 1 & 1 \\ -1 & 2 \end{vmatrix}; \begin{vmatrix} 1 & -1 \\ 2 & 0 \end{vmatrix}; \begin{vmatrix} -1 & 1 \\ 0 & -1 \end{vmatrix} \right) = (1 \cdot 2 - 1(-1); 1 \cdot 0 - (-1) \cdot 2; (-1)(-1) - 1 \cdot 0) = (3; 2; 1)$$
  Vì $[\overrightarrow{AB}, \overrightarrow{AC}] \ne \vec{0}$, ba điểm $A, B, C$ không thẳng hàng và tạo thành một mặt phẳng nhận $\vec{n} = (3; 2; 1)$ làm vectơ pháp tuyến.
- **c) Sai.** Mặt phẳng $(ABC)$ đi qua $A(1; 1; 0)$ và nhận $\vec{n} = (3; 2; 1)$ làm VTPT có phương trình là:
  $$3(x - 1) + 2(y - 1) + 1(z - 0) = 0 \iff 3x - 3 + 2y - 2 + z = 0 \iff 3x + 2y + z - 5 = 0$$
  Phương trình trong đề là $3x + 2y + z + 5 = 0$ (sai dấu hệ số tự do).
- **d) Đúng.** Áp dụng công thức khoảng cách từ điểm $M(2; 3; -1)$ đến mặt phẳng $(ABC): 3x + 2y + z - 5 = 0$:
  $$d(M, (ABC)) = \dfrac{|3(2) + 2(3) + 1(-1) - 5|}{\sqrt{3^2 + 2^2 + 1^2}} = \dfrac{|6 + 6 - 1 - 5|}{\sqrt{9 + 4 + 1}} = \dfrac{6}{\sqrt{14}} = \dfrac{6\sqrt{14}}{14} = \dfrac{3\sqrt{14}}{7}$$

---

## PHẦN III. Câu trắc nghiệm trả lời ngắn (4 câu – 2,0 điểm)
*Thí sinh trả lời từ Câu 1 đến Câu 4. Mỗi câu trả lời đúng được 0,5 điểm.*

---

### Câu 1.
Cho hàm số $y = f(x)$ có đạo hàm liên tục trên đoạn $[1; 4]$, đồng thời thỏa mãn $f(1) = 2$ và $f(4) = 11$. Tính giá trị của tích phân $I = \int_1^4 [3f'(x) - 2x] dx$.

- **Đáp số:** `....`

**Lời giải:**
#### Câu 1 — Đáp số: `12`
- Tách tích phân đã cho thành hai phần:
  $$I = 3 \int_1^4 f'(x) dx - \int_1^4 2x dx$$
- Ta có:
  $$\int_1^4 f'(x) dx = [f(x)]_1^4 = f(4) - f(1) = 11 - 2 = 9$$
  $$\int_1^4 2x dx = [x^2]_1^4 = 4^2 - 1^2 = 16 - 1 = 15$$
- Do đó:
  $$I = 3 \cdot 9 - 15 = 27 - 15 = 12$$

---

### Câu 2.
Một chiếc xe ô tô đang di chuyển thẳng đều với vận tốc $20\text{ m/s}$ thì người lái xe bất ngờ phát hiện chướng ngại vật phía trước và nhấn bàn đạp phanh. Kể từ thời điểm bắt đầu đạp phanh, ô tô chuyển động chậm dần đều với vận tốc biến thiên theo thời gian là $v(t) = -4t + 20\text{ (m/s)}$, trong đó $t$ là thời gian tính bằng giây ($t \ge 0$). Tính quãng đường mà chiếc xe ô tô tiếp tục di chuyển được từ lúc đạp phanh cho đến khi dừng hẳn (đơn vị: mét).

- **Đáp số:** `....`

**Lời giải:**
#### Câu 2 — Đáp số: `50`
- Thời điểm ô tô dừng hẳn là khi vận tốc tức thời bằng $0$:
  $$v(t) = 0 \iff -4t + 20 = 0 \iff t = 5\text{ (giây)}$$
- Quãng đường $s$ mà xe đi được từ lúc bắt đầu đạp phanh ($t = 0$) đến khi dừng hẳn ($t = 5$) là tích phân của vận tốc theo thời gian:
  $$s = \int_0^5 v(t) dt = \int_0^5 (-4t + 20) dt = \left[ -2t^2 + 20t \right]_0^5 = (-2 \cdot 5^2 + 20 \cdot 5) - 0 = -50 + 100 = 50\text{ (m)}$$

---

### Câu 3.
Trong không gian với hệ tọa độ $Oxyz$, cho hai điểm $A(1; 2; 3)$ và $B(4; -2; 3)$. Tính khoảng cách giữa hai điểm $A$ và $B$.

- **Đáp số:** `....`

**Lời giải:**
#### Câu 3 — Đáp số: `5`
- Tọa độ vectơ $\overrightarrow{AB}$ là:
  $$\overrightarrow{AB} = (4 - 1; -2 - 2; 3 - 3) = (3; -4; 0)$$
- Khoảng cách giữa hai điểm $A$ và $B$ là:
  $$AB = |\overrightarrow{AB}| = \sqrt{3^2 + (-4)^2 + 0^2} = \sqrt{9 + 16 + 0} = \sqrt{25} = 5$$

---

### Câu 4.
Một nhà máy sản xuất linh kiện điện tử có hai dây chuyền phân xưởng I và II. Phân xưởng I đảm nhận sản xuất $60\%$ tổng sản lượng của nhà máy, phân xưởng II đảm nhận sản xuất $40\%$ tổng sản lượng còn lại. Qua kiểm tra chất lượng, tỷ lệ linh kiện phế phẩm do phân xưởng I sản xuất là $2\%$, và do phân xưởng II sản xuất là $3\%$. Lấy ngẫu nhiên một linh kiện từ kho hàng chung của nhà máy và phát hiện đó là linh kiện phế phẩm. Tính xác suất để linh kiện phế phẩm đó do phân xưởng I sản xuất.

- **Đáp số:** `....`

**Lời giải:**
#### Câu 4 — Đáp số: `0,5`
- Gọi các biến cố:
  - $B_1$: "Linh kiện lấy ra do phân xưởng I sản xuất", khi đó $P(B_1) = 60\% = 0{,}6$.
  - $B_2$: "Linh kiện lấy ra do phân xưởng II sản xuất", khi đó $P(B_2) = 40\% = 0{,}4$.
  - $A$: "Linh kiện lấy ra là phế phẩm".
- Theo đề bài, ta có xác suất có điều kiện:
  $$P(A|B_1) = 2\% = 0{,}02, \quad P(A|B_2) = 3\% = 0{,}03$$
- Theo công thức xác suất toàn phần, xác suất lấy được một linh kiện phế phẩm là:
  $$P(A) = P(B_1)P(A|B_1) + P(B_2)P(A|B_2) = 0{,}6 \times 0{,}02 + 0{,}4 \times 0{,}03 = 0{,}012 + 0{,}012 = 0{,}024$$
- Theo công thức Bayes, xác suất để phế phẩm đó do phân xưởng I sản xuất là:
  $$P(B_1|A) = \dfrac{P(B_1)P(A|B_1)}{P(A)} = \dfrac{0{,}012}{0{,}024} = 0{,}5$$

---

## PHẦN IV. Tự luận (2 câu – 3,0 điểm)
*Thí sinh trình bày chi tiết các bước biến đổi, lập luận và tính toán ra giấy thi.*

---

### Bài 1 (1,5 điểm).
Cho hình phẳng $(H)$ giới hạn bởi đồ thị hàm số $y = \sqrt{2x + 1}$, trục hoành $Ox$ và hai đường thẳng $x = 0$, $x = 4$.
1. Lập luận thiết lập công thức tích phân tính thể tích khối tròn xoay tạo thành khi quay hình phẳng $(H)$ quanh trục hoành $Ox$.
2. Tính chính xác thể tích khối tròn xoay đó theo $\pi$.

**Lời giải:**
#### Bài 1 (1,5 điểm).
- **Bước 1 (Thiết lập mô hình tích phân):**
  - Hàm số $y = f(x) = \sqrt{2x + 1}$ xác định và liên tục trên đoạn $[0; 4]$ với $2x + 1 \ge 0, \forall x \in [0; 4]$. *(0,25 điểm)*
  - Khi quay hình phẳng $(H)$ giới hạn bởi đường cong $y = f(x)$, trục $Ox$ và các đường thẳng $x = 0, x = 4$ quanh trục hoành $Ox$, thể tích của khối tròn xoay sinh ra được tính theo công thức:
    $$V = \pi \int_0^4 [f(x)]^2 dx = \pi \int_0^4 (\sqrt{2x + 1})^2 dx$$ *(0,50 điểm)*
- **Bước 2 (Tính tích phân):**
  - Ta có $(\sqrt{2x + 1})^2 = 2x + 1$. Biểu thức tích phân trở thành:
    $$V = \pi \int_0^4 (2x + 1) dx$$ *(0,25 điểm)*
  - Tìm nguyên hàm của hàm số:
    $$\int (2x + 1) dx = x^2 + x$$ *(0,25 điểm)*
  - Thay cận theo công thức Newton – Leibniz:
    $$V = \pi \left[ x^2 + x \right]_0^4 = \pi \left( 4^2 + 4 - (0^2 + 0) \right) = \pi (16 + 4) = 20\pi$$ *(0,25 điểm)*
- **Kết luận:** Thể tích của khối tròn xoay cần tìm là $V = 20\pi$ (đơn vị thể tích).

---

### Bài 2 (1,5 điểm).
Trong một dự án thiết kế cảnh quan khu nghỉ dưỡng sinh thái, các kỹ sư thiết kế một mái che sân vườn ngoài trời có dạng một phần của mặt phẳng $(P)$. Chọn hệ trục tọa độ $Oxyz$ với đơn vị trên mỗi trục là mét ($\text{m}$), mặt đất bằng phẳng trùng với mặt phẳng tọa độ $(Oxy)$. Mái che $(P)$ tựa trên ba trụ đỡ vững chắc tại ba điểm đỉnh $A(0; 0; 3)$, $B(6; 0; 4)$ và $C(0; 8; 5)$.
1. Hãy lập phương trình tổng quát của mặt phẳng mái che $(P)$.
2. Tại vị trí điểm $S(3; 4; 6)$, người ta muốn treo một cụm đèn trang trí.
   - Tính khoảng cách từ điểm treo đèn $S$ vuông góc đến mặt phẳng mái che $(P)$ (làm tròn kết quả đến hai chữ số thập phân sau dấu phẩy).
   - Tính số đo góc dốc nghiêng $\alpha$ của mái che so với mặt đất nằm ngang $(Oxy)$ (làm tròn kết quả đến hàng phần mười của độ).

**Lời giải:**
#### Bài 2 (1,5 điểm).
- **Ý 1: Lập phương trình tổng quát của mặt phẳng $(P)$ (0,75 điểm):**
  - Ta có tọa độ hai vectơ chỉ phương của mặt phẳng $(P)$ nằm trên mái che:
    $$\overrightarrow{AB} = (6 - 0; 0 - 0; 4 - 3) = (6; 0; 1)$$
    $$\overrightarrow{AC} = (0 - 0; 8 - 0; 5 - 3) = (0; 8; 2)$$ *(0,25 điểm)*
  - Tích có hướng của hai vectơ:
    $$[\overrightarrow{AB}, \overrightarrow{AC}] = (0 \cdot 2 - 1 \cdot 8; 1 \cdot 0 - 6 \cdot 2; 6 \cdot 8 - 0 \cdot 0) = (-8; -12; 48) = -4(2; 3; -12)$$
    Suy ra mặt phẳng $(P)$ nhận vectơ $\vec{n} = (2; 3; -12)$ làm một vectơ pháp tuyến. *(0,25 điểm)*
  - Mặt phẳng $(P)$ đi qua điểm $A(0; 0; 3)$ và có VTPT $\vec{n} = (2; 3; -12)$ nên có phương trình tổng quát:
    $$2(x - 0) + 3(y - 0) - 12(z - 3) = 0 \iff 2x + 3y - 12z + 36 = 0$$ *(0,25 điểm)*
- **Ý 2: Tính khoảng cách và góc dốc của mái che (0,75 điểm):**
  - **Khoảng cách từ $S$ đến mặt phẳng $(P)$:**
    Áp dụng công thức tính khoảng cách từ điểm $S(3; 4; 6)$ đến $(P): 2x + 3y - 12z + 36 = 0$:
    $$d(S, (P)) = \dfrac{|2 \cdot 3 + 3 \cdot 4 - 12 \cdot 6 + 36|}{\sqrt{2^2 + 3^2 + (-12)^2}} = \dfrac{|6 + 12 - 72 + 36|}{\sqrt{4 + 9 + 144}} = \dfrac{|-18|}{\sqrt{157}} = \dfrac{18}{\sqrt{157}}$$
    Thực hiện phép tính xấp xỉ:
    $$d(S, (P)) = \dfrac{18}{\sqrt{157}} \approx 1{,}4365\text{ m} \approx 1{,}44\text{ m}$$ *(0,50 điểm)*
  - **Góc nghiêng của mái che so với mặt đất $(Oxy)$:**
    Mặt đất nằm ngang trùng với mặt phẳng tọa độ $(Oxy): z = 0$, có một vectơ pháp tuyến là $\vec{k} = (0; 0; 1)$.
    Gọi $\alpha$ là góc giữa mặt phẳng mái che $(P)$ và mặt phẳng $(Oxy)$ ($0^\circ \le \alpha \le 90^\circ$). Ta có:
    $$\cos \alpha = \dfrac{|\vec{n} \cdot \vec{k}|}{|\vec{n}| \cdot |\vec{k}|} = \dfrac{|2 \cdot 0 + 3 \cdot 0 + (-12) \cdot 1|}{\sqrt{157} \cdot \sqrt{0^2 + 0^2 + 1^2}} = \dfrac{12}{\sqrt{157}} \approx 0{,}9577$$
    Suy ra:
    $$\alpha = \arccos\left(\dfrac{12}{\sqrt{157}}\right) \approx 16{,}72^\circ \approx 16{,}7^\circ$$ *(0,25 điểm)*
- **Kết luận:**
  - Phương trình mặt phẳng mái che $(P)$ là $2x + 3y - 12z + 36 = 0$.
  - Khoảng cách từ cụm đèn $S$ đến mái che là xấp xỉ $1{,}44\text{ m}$.
  - Góc dốc của mái che so với mặt phẳng nằm ngang là xấp xỉ $16{,}7^\circ$.

---

## BẢNG ĐÁP ÁN TỔNG HỢP TOÀN ĐỀ THI

### PHẦN I. TRẮC NGHIỆM NHIỀU LỰA CHỌN (12 CÂU)
| Câu 1 | Câu 2 | Câu 3 | Câu 4 | Câu 5 | Câu 6 | Câu 7 | Câu 8 | Câu 9 | Câu 10 | Câu 11 | Câu 12 |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **B** | **C** | **A** | **D** | **A** | **C** | **B** | **D** | **A** | **C** | **B** | **D** |

### PHẦN II. TRẮC NGHIỆM ĐÚNG / SAI (2 CÂU)
| Câu hỏi | Lệnh hỏi a) | Lệnh hỏi b) | Lệnh hỏi c) | Lệnh hỏi d) |
|:---|:---:|:---:|:---:|:---:|
| **Câu 1** | **ĐÚNG** | **ĐÚNG** | **ĐÚNG** | **SAI** |
| **Câu 2** | **ĐÚNG** | **ĐÚNG** | **SAI** | **ĐÚNG** |

### PHẦN III. TRẮC NGHIỆM TRẢ LỜI NGẮN (4 CÂU)
| Câu hỏi | Câu 1 | Câu 2 | Câu 3 | Câu 4 |
|:---|:---:|:---:|:---:|:---:|
| **Đáp số** | **12** | **50** | **5** | **0,5** |

### PHẦN IV. TỰ LUẬN (2 CÂU)
| Bài | Điểm | Kết quả then chốt |
|:---|:---:|:---|
| **Bài 1** | 1,5 điểm | $V = \pi \int_0^4 (2x + 1) dx = 20\pi$ (đvtt) |
| **Bài 2** | 1,5 điểm | $(P): 2x + 3y - 12z + 36 = 0$; $d(S, (P)) \approx 1{,}44\text{ m}$; $\alpha \approx 16{,}7^\circ$ |

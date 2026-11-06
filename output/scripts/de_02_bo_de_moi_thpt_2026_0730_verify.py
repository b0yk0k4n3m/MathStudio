"""
File verify_math.py: Kiem chung toan hoc bang SymPy cho toan bo 22 cau cua De thi Tot nghiep THPT 2026.
Chuyen de: Tong hop chuan cau truc THPT 2026 (Ham so, Giai tich 12, Oxyz, Xac suat - Thong ke, Thuc tien).
"""

import sympy as sp

print("=" * 60)
print("KIEM CHUNG DE THI TOT NGHIEP THPT 2026 - SYMPY VERIFICATION")
print("=" * 60)

x, y, z, t = sp.symbols('x y z t', real=True)

# ==============================================================================
# PHAN I: 12 CAU TRAC NGHIEM 4 LUA CHON (0,25 diem/cau)
# ==============================================================================
print("\n--- KIEM CHUNG PHAN I ---")

# Cau 1: Tiem can ngang cua y = (3x - 2)/(x + 1)
f1 = (3*x - 2)/(x + 1)
lim1 = sp.limit(f1, x, sp.oo)
assert lim1 == 3
print(f"Cau 1: OK (Tiem can ngang y = {lim1})")

# Cau 2: Nguyen ham cua f(x) = 4x^3 - 2x + 5
f2 = 4*x**3 - 2*x + 5
F2 = sp.integrate(f2, x)
assert F2 == x**4 - x**2 + 5*x
print(f"Cau 2: OK (Nguyen ham F(x) = {F2} + C)")

# Cau 3: Gia tri cuc tieu cua y = x^3 - 3x^2 - 9x + 2
f3 = x**3 - 3*x**2 - 9*x + 2
df3 = sp.diff(f3, x)
roots3 = sp.solve(df3, x) # [-1, 3]
d2f3 = sp.diff(df3, x)
ct3_x = [r for r in roots3 if d2f3.subs(x, r) > 0][0]
y_ct3 = f3.subs(x, ct3_x)
assert ct3_x == 3 and y_ct3 == -25
print(f"Cau 3: OK (x_CT = {ct3_x}, y_CT = {y_ct3})")

# Cau 4: Mat cau (S) tam I(2; -1; 3) di qua A(4; 1; 2)
I4 = sp.Matrix([2, -1, 3])
A4 = sp.Matrix([4, 1, 2])
R4_sq = (A4 - I4).dot(A4 - I4)
assert R4_sq == 9
print(f"Cau 4: OK (R^2 = {R4_sq})")

# Cau 5: GTLN cua y = x + 4/x tren [1; 3]
f5 = x + 4/x
df5 = sp.diff(f5, x)
crit5 = [r for r in sp.solve(df5, x) if 1 <= r <= 3]
pts5 = [1, 3] + crit5
vals5 = [f5.subs(x, p) for p in pts5] # [5, 13/3, 4]
assert max(vals5) == 5
print(f"Cau 5: OK (Max = {max(vals5)} tai x = 1)")

# Cau 6: So nghiem nguyen cua log_2(x^2 - 3x + 2) <= 1
# Dk: x^2 - 3x + 2 > 0 <=> x < 1 hoac x > 2
# x^2 - 3x + 2 <= 2 <=> 0 <= x <= 3
sols6 = [val for val in range(-5, 10) if (val**2 - 3*val + 2 > 0) and (val**2 - 3*val + 2 <= 2)]
assert sols6 == [0, 3] and len(sols6) == 2
print(f"Cau 6: OK (Nghiem nguyen = {sols6}, so luong = {len(sols6)})")

# Cau 7: Cho int_0^2 f(x)dx = 5. Tinh I = int_0^1 [3f(2x) - 4x] dx
# int_0^1 3f(2x)dx = 3/2 * 5 = 15/2. int_0^1 4x dx = 2. I = 15/2 - 2 = 11/2
I7 = sp.Rational(3, 2) * 5 - sp.integrate(4*x, (x, 0, 1))
assert I7 == sp.Rational(11, 2)
print(f"Cau 7: OK (I = {I7})")

# Cau 8: Dien tich hinh phang y = x^2 - 4x + 3 va y = x - 1
f8_1 = x**2 - 4*x + 3
f8_2 = x - 1
pts8 = sp.solve(f8_1 - f8_2, x) # [1, 4]
S8 = sp.integrate(f8_2 - f8_1, (x, pts8[0], pts8[1]))
assert S8 == sp.Rational(9, 2)
print(f"Cau 8: OK (S = {S8})")

# Cau 9: Khoang cach tu O den (P): x + 2y - 2z - 7 = 0
d9 = abs(-7) / sp.sqrt(1**2 + 2**2 + (-2)**2)
assert d9 == sp.Rational(7, 3)
print(f"Cau 9: OK (d(O, P) = {d9})")

# Cau 10: VTCP u = [n_P, u_d] voi n_P = (2; -1; 2), u_d = (2; 1; -1)
nP10 = sp.Matrix([2, -1, 2])
ud10 = sp.Matrix([2, 1, -1])
u10 = nP10.cross(ud10)
assert list(u10) == [-1, 6, 4]
print(f"Cau 10: OK (u = {list(u10)})")

# Cau 11: Khoang tu phan vi mau ghep nhom N=50
# Nhom [10; 20): 5, [20; 30): 12, [30; 40): 18, [40; 50): 10, [50; 60): 5
N11 = 50
Q1_11 = 20 + (sp.Rational(N11, 4) - 5) / 12 * 10 # 26.25
Q3_11 = 40 + (sp.Rational(3*N11, 4) - 35) / 10 * 10 # 42.5
Delta_Q11 = Q3_11 - Q1_11
assert Delta_Q11 == sp.Rational(65, 4) and float(Delta_Q11) == 16.25
print(f"Cau 11: OK (Q1 = {float(Q1_11)}, Q3 = {float(Q3_11)}, Delta_Q = {float(Delta_Q11)})")

# Cau 12: Xac suat toan phan linh kien phe pham
P12 = sp.Rational(60, 100) * sp.Rational(2, 100) + sp.Rational(40, 100) * sp.Rational(3, 100)
assert P12 == sp.Rational(3, 125) and float(P12) == 0.024
print(f"Cau 12: OK (P = {P12} = {float(P12)})")


# ==============================================================================
# PHAN II: 4 CAU TRAC NGHIEM DUNG/SAI (4,00 diem)
# ==============================================================================
print("\n--- KIEM CHUNG PHAN II ---")

# Cau 1 (Ham so): f(x) = (x^2 - 2x + 5)/(x - 1)
f_p2_1 = (x**2 - 2*x + 5)/(x - 1)
df_p2_1 = sp.simplify(sp.diff(f_p2_1, x))
crit_p2_1 = sp.solve(df_p2_1, x) # [-1, 3]
# a) Ham so dong bien tren (3; +oo) -> Dung (f' > 0 tren (3; +oo))
assert df_p2_1.subs(x, 4) > 0
# b) Tiem can xien y = x - 1 -> Dung (apart = x - 1 + 4/(x - 1))
poly_part, rem_part = sp.div(x**2 - 2*x + 5, x - 1)
assert poly_part == x - 1
# c) Gia tri cuc dai bang 6 -> Sai (f(-1) = -4)
val_cd = f_p2_1.subs(x, -1)
assert val_cd == -4 and val_cd != 6
# d) Duong qua 2 cuc tri y = 2x - 2 -> Dung (A(-1; -4), B(3; 4))
y_A = f_p2_1.subs(x, -1)
y_B = f_p2_1.subs(x, 3)
assert (2*(-1) - 2 == y_A) and (2*(3) - 2 == y_B)
print(f"Cau 13 (P2.1): OK (a: Dung, b: Dung, c: Sai, d: Dung)")

# Cau 2 (Giai tich 12 - Chuyen dong): v(t) = -4t + 20
v2 = -4*t + 20
# a) Gia toc a = -4 m/s^2 -> Dung
a2 = sp.diff(v2, t)
assert a2 == -4
# b) Dung han sau 5s -> Dung
t_stop = sp.solve(v2, t)[0]
assert t_stop == 5
# c) Quang duong 3s dau la 48 m -> Sai (vi s(3) = 42 m)
s_3s = sp.integrate(v2, (t, 0, 3))
assert s_3s == 42 and s_3s != 48
# d) Tong quang duong 7s (2s deu + 5s phanh) la 90 m -> Dung (20*2 + 50 = 90)
s_phanh = sp.integrate(v2, (t, 0, 5))
s_total_7 = 20 * 2 + s_phanh
assert s_phanh == 50 and s_total_7 == 90
print(f"Cau 14 (P2.2): OK (a: Dung, b: Dung, c: Sai, d: Dung)")

# Cau 3 (Oxyz): A(1; 2; -1), B(3; 0; 1), (P): x - y + 2z - 3 = 0
A3 = sp.Matrix([1, 2, -1])
B3 = sp.Matrix([3, 0, 1])
nP3 = sp.Matrix([1, -1, 2])
# a) Trung diem M(2; 1; 0) -> Dung
M3 = (A3 + B3) / 2
assert list(M3) == [2, 1, 0]
# b) VTCP duong thang AB la u = (1; -1; 1) -> Dung (B - A = (2, -2, 2) = 2*(1, -1, 1))
AB_vec = B3 - A3
assert list(AB_vec) == [2, -2, 2]
# c) Khoang cach tu A den (P) bang 2*sqrt(6) -> Sai (vi bang sqrt(6))
d_AP = abs(1*1 - 1*2 + 2*(-1) - 3) / sp.sqrt(1**2 + (-1)**2 + 2**2)
assert d_AP == sp.sqrt(6) and d_AP != 2*sp.sqrt(6)
# d) Hinh chieu H cua A tren (P) la H(2; 1; 1) -> Dung
# A + t*nP = (1+t, 2-t, -1+2t) thuoc (P) => (1+t) - (2-t) + 2(-1+2t) - 3 = 0 => 6t - 6 = 0 => t = 1 => H(2, 1, 1)
t_val = sp.solve((1+t) - (2-t) + 2*(-1+2*t) - 3, t)[0]
H_pt = A3 + t_val * nP3
assert list(H_pt) == [2, 1, 1]
print(f"Cau 15 (P2.3): OK (a: Dung, b: Dung, c: Sai, d: Dung)")

# Cau 4 (Xac suat Bayes Y te):
# P(A) = 0.02 (mac benh), P(not A) = 0.98.
# P(B|A) = 0.98 (do nhay), P(not B | not A) = 0.98 (do dac hieu) => P(B|not A) = 0.02 (duong tinh gia).
P_A4 = sp.Rational(2, 100)
P_notA4 = sp.Rational(98, 100)
P_B_given_A4 = sp.Rational(98, 100)
P_B_given_notA4 = sp.Rational(2, 100)
# a) Xac suat khong mac benh la 0.98 -> Dung
assert P_notA4 == sp.Rational(98, 100)
# b) Xac suat khong mac benh nhung duong tinh (duong tinh gia) la 0.02 -> Dung
assert P_B_given_notA4 == sp.Rational(2, 100)
# c) Xac suat mot nguoi bat ky duong tinh la 0.05 -> Sai (vi bang 0.0392)
P_B4 = P_A4 * P_B_given_A4 + P_notA4 * P_B_given_notA4
assert float(P_B4) == 0.0392 and float(P_B4) != 0.05
# d) Biet nguoi do duong tinh, xac suat mac benh la 0.5 (50%) -> Dung
P_A_given_B4 = (P_A4 * P_B_given_A4) / P_B4
assert P_A_given_B4 == sp.Rational(1, 2)
print(f"Cau 16 (P2.4): OK (a: Dung, b: Dung, c: Sai, d: Dung)")


# ==============================================================================
# PHAN III: 6 CAU TRAC NGHIEM TRA LOI NGAN (0,50 diem/cau)
# ==============================================================================
print("\n--- KIEM CHUNG PHAN III ---")

# Cau 1 (P3.1): Loi nhuan L(x) = x(190 - x) - (x^2 + 30x + 400). Tim x de L max.
L1 = x*(190 - x) - (x**2 + 30*x + 400)
dL1 = sp.diff(L1, x)
x_opt1 = sp.solve(dL1, x)[0]
L_max1 = L1.subs(x, x_opt1)
assert x_opt1 == 40 and L_max1 == 2800
print(f"Cau 17 (P3.1): OK (x_opt = {x_opt1})")

# Cau 2 (P3.2): Cong parabol y = 9 - x^2 tren [-3; 3]. Cua go hcn rong 4m (x tu -2 den 2), chieu cao y(2) = 5.
# Dien tich phan con lai lap kinh: S_kinh = S_toanbo - S_go
S_total2 = sp.integrate(9 - x**2, (x, -3, 3))
S_go2 = 4 * (9 - 2**2) # 4 * 5 = 20
S_kinh2 = S_total2 - S_go2
assert S_total2 == 36 and S_go2 == 20 and S_kinh2 == 16
print(f"Cau 18 (P3.2): OK (S_kinh = {S_kinh2})")

# Cau 3 (P3.3): Hinh chop S.ABCD day hinh vuong canh 6, SA vuong goc day, SA = 3. M la trung diem BC. d(SB, DM)
A_p3 = sp.Matrix([0, 0, 0])
B_p3 = sp.Matrix([6, 0, 0])
D_p3 = sp.Matrix([0, 6, 0])
C_p3 = sp.Matrix([6, 6, 0])
S_p3 = sp.Matrix([0, 0, 3])
M_p3 = sp.Matrix([6, 3, 0])
u_SB = B_p3 - S_p3 # (6, 0, -3)
u_DM = M_p3 - D_p3 # (6, -3, 0)
cross_3 = u_SB.cross(u_DM) # (-9, -18, -18)
SD_vec = D_p3 - S_p3 # (0, 6, -3)
d_SB_DM = abs(cross_3.dot(SD_vec)) / cross_3.norm()
assert d_SB_DM == 2
print(f"Cau 19 (P3.3): OK (d(SB, DM) = {d_SB_DM})")

# Cau 4 (P3.4): Oxyz UAV bay tren d qua A(2; 4; 4) va B(1; 2; 5). Gan O nhat tai M(a; b; c). T = a + 2b + 3c.
u_d4 = sp.Matrix([-1, -2, 1])
# M(t) = A + t*u_d4 = (2 - t, 4 - 2t, 4 + t)
dist_sq4 = (2 - t)**2 + (4 - 2*t)**2 + (4 + t)**2
t_opt4 = sp.solve(sp.diff(dist_sq4, t), t)[0]
M_opt4 = sp.Matrix([2 - t_opt4, 4 - 2*t_opt4, 4 + t_opt4])
T4 = M_opt4[0] + 2*M_opt4[1] + 3*M_opt4[2]
assert t_opt4 == 1 and list(M_opt4) == [1, 2, 5] and T4 == 20
print(f"Cau 20 (P3.4): OK (M = {list(M_opt4)}, T = {T4})")

# Cau 5 (P3.5): Hop I (3 do, 5 xanh), Hop II (4 do, 5 xanh). Chuyen 1 vien tu I sang II, roi lay 2 vien tu II.
# Biet 2 vien lay ra tu II deu do. Xac suat vien chuyen tu I sang II la do = ?
P_A5 = sp.Rational(3, 8)
P_notA5 = sp.Rational(5, 8)
P_B_given_A5 = sp.binomial(5, 2) / sp.binomial(10, 2) # 10/45
P_B_given_notA5 = sp.binomial(4, 2) / sp.binomial(10, 2) # 6/45
P_B5 = P_A5 * P_B_given_A5 + P_notA5 * P_B_given_notA5
P_A_given_B5 = (P_A5 * P_B_given_A5) / P_B5
assert P_B5 == sp.Rational(1, 6) and P_A_given_B5 == sp.Rational(1, 2) and float(P_A_given_B5) == 0.5
print(f"Cau 21 (P3.5): OK (P(A|B) = {float(P_A_given_B5)})")

# Cau 6 (P3.6): Nha may tai A, dao C cach bien CB = 4 km, AB = 10 km.
# Chi phi tren bo 300 tr/km, duoi bien 500 tr/km. Chi phi nho nhat (trieu dong)?
# Dat BM = x => f(x) = 300*(10 - x) + 500*sqrt(x^2 + 16)
f_cost = 300*(10 - x) + 500*sp.sqrt(x**2 + 16)
df_cost = sp.diff(f_cost, x)
x_crit = [r for r in sp.solve(df_cost, x) if 0 <= r <= 10][0]
cost_min = f_cost.subs(x, x_crit)
assert x_crit == 3 and cost_min == 4600
print(f"Cau 22 (P3.6): OK (x_opt = {x_crit} km, Chi phi min = {cost_min} trieu dong)")

print("\n" + "=" * 60)
print("TAT CA 22 CAU HOI DA DUOC KIEM CHUNG CHINH XAC 100%!")
print("=" * 60)

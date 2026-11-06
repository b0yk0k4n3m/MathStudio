import sympy as sp
from fractions import Fraction
import math

print("=== KIEM CHUNG DE THI TOT NGHIEP THPT 2026 (22 CAU) ===")

x, y, z, t, m = sp.symbols('x y z t m', real=True)

# ---------------------------------------------------------
# PHAN I: 12 CAU TRAC NGHIEM 4 LUA CHON
# ---------------------------------------------------------

# Cau 1 [Nhan biet - Ham so]: Tim tiem can ngang cua do thi ham so y = (3x - 2)/(x + 1)
f1 = (3*x - 2)/(x + 1)
tcn_1 = sp.limit(f1, x, sp.oo)
print(f"P1 - Cau 1: Tiem can ngang y = {tcn_1}")

# Cau 2 [Nhan biet - Nguyen ham]: Ho nguyen ham cua ham so f(x) = 4x^3 - 2x + 5
f2 = 4*x**3 - 2*x + 5
F2 = sp.integrate(f2, x)
print(f"P1 - Cau 2: Nguyen ham F(x) = {F2} + C")

# Cau 3 [Thong hieu - Ham so (Cuc tri/Don dieu)]: Cho ham so y = x^3 - 3x^2 - 9x + 2. Gia tri cuc tieu cua ham so.
f3 = x**3 - 3*x**2 - 9*x + 2
df3 = sp.diff(f3, x)
crit_3 = sp.solve(df3, x)
d2f3 = sp.diff(df3, x)
y_ct_3 = [f3.subs(x, c) for c in crit_3 if d2f3.subs(x, c) > 0][0]
print(f"P1 - Cau 3: Cuc tri x = {crit_3}, Gia tri cuc tieu y_CT = {y_ct_3}")

# Cau 4 [Thong hieu - Oxyz]: Mat cau (S) tam I(2; -1; 3) va di qua diem A(4; 1; 2) co phuong trinh
I4 = sp.Matrix([2, -1, 3])
A4 = sp.Matrix([4, 1, 2])
R4_sq = (A4 - I4).dot(A4 - I4)
print(f"P1 - Cau 4: R^2 = {R4_sq}")

# Cau 5 [Van dung - Ham so (GTLN-GTNN)]: Tim GTLN cua ham so y = x + 4/x tren doan [1; 3]
f5 = x + 4/x
df5 = sp.diff(f5, x)
sol5 = [s for s in sp.solve(df5, x) if 1 <= s <= 3]
pts5 = [1, 3] + sol5
vals5 = [f5.subs(x, p) for p in pts5]
print(f"P1 - Cau 5: Gia tri tren [1;3] tai {pts5} la {vals5}, Max = {max(vals5)}, Min = {min(vals5)}")

# Cau 6 [Van dung - Mu & Logarit / Lai suat thuc tien]: Bat phuong trinh log_2(x^2 - 3x + 2) <= 1
# Dieu kien: x^2 - 3x + 2 > 0 <=> x < 1 hoac x > 2
# BPT <=> x^2 - 3x + 2 <= 2 <=> x^2 - 3x <= 0 <=> 0 <= x <= 3
# Ket hop: [0; 1) U (2; 3]. Tong cac nghiem nguyen: 0 + 3 = 3, so nghiem nguyen la 2 (x=0, x=3)
int_sols_6 = [i for i in range(-5, 10) if (i**2 - 3*i + 2 > 0) and (i**2 - 3*i + 2 <= 2)]
print(f"P1 - Cau 6: Nghiem nguyen = {int_sols_6}, so nghiem nguyen = {len(int_sols_6)}")

# Cau 7 [Van dung - Tich phan]: Cho int_0^2 f(x)dx = 5. Tinh I = int_0^1 [3*f(2x) - 4x] dx
# Dat t = 2x => dx = dt/2. int_0^1 3*f(2x)dx = (3/2)*int_0^2 f(t)dt = 3/2 * 5 = 15/2.
# int_0^1 4x dx = 2. I = 15/2 - 2 = 11/2.
I7 = sp.Rational(3, 2) * 5 - sp.integrate(4*x, (x, 0, 1))
print(f"P1 - Cau 7: I = {I7}")

# Cau 8 [Van dung - Ung dung tich phan]: Dien tich hinh phang gioi han boi y = x^2 - 4x + 3 va y = x - 1
f8_1 = x**2 - 4*x + 3
f8_2 = x - 1
inter8 = sp.solve(f8_1 - f8_2, x)
S8 = sp.integrate(sp.Abs(f8_1 - f8_2), (x, inter8[0], inter8[1]))
print(f"P1 - Cau 8: Giao diem = {inter8}, Dien tich S = {S8}")

# Cau 9 [Van dung - Oxyz (Mat phang & Duong thang)]: Cho diem M(1; 2; -1) va duong thang d: (x-2)/1 = (y+1)/2 = z/(-2).
# Mat phang (P) chua M va vuong goc voi d co phuong trinh:
# VTPT n = (1, 2, -2) => 1(x-1) + 2(y-2) - 2(z+1) = 0 <=> x + 2y - 2z - 7 = 0. Khoang cach tu O den (P):
d_O_P9 = abs(-7) / sp.sqrt(1**2 + 2**2 + (-2)**2)
print(f"P1 - Cau 9: Khoang cach tu O den (P) = {d_O_P9}")

# Cau 10 [Van dung - Oxyz (Goc / Giao diem)]: Duong thang di qua A(1; 0; -2), song song voi (P): 2x - y + 2z + 3 = 0
# va vuong goc voi d: (x-1)/2 = y/1 = (z+1)/(-1).
# VTCP u = [n_P, u_d]
n_P10 = sp.Matrix([2, -1, 2])
u_d10 = sp.Matrix([2, 1, -1])
u10 = n_P10.cross(u_d10)
print(f"P1 - Cau 10: VTCP u = [n_P, u_d] = {list(u10)}")

# Cau 11 [Van dung - Thong ke ghep nhom]: Mau so lieu ghep nhom ve thoi gian (phut) tap the duc moi ngay:
# Nhom: [10; 20), [20; 30), [30; 40), [40; 50), [50; 60)
# Tan so: 5, 12, 18, 10, 5 (Tong N = 50)
# Tinh phuong sai / do lech chuan hoac khoang tu phan vi Delta_Q:
# Co mau N = 50:
# Q1: vi tri 50/4 = 12.5 -> nhom 2 [20; 30), cf truoc = 5, f = 12 => Q1 = 20 + (12.5 - 5)/12 * 10 = 20 + 75/12 = 26.25
# Q3: vi tri 3*50/4 = 37.5 -> cf: 5, 17, 35, 45 -> nhom 4 [40; 50), cf truoc = 35, f = 10 => Q3 = 40 + (37.5 - 35)/10 * 10 = 42.5
# Delta_Q = Q3 - Q1 = 42.5 - 26.25 = 16.25 (hoac 65/4)
Q1_11 = 20 + sp.Rational(25, 2 - 0) # let's compute exact with Rational
N11 = 50
Q1_11 = 20 + (sp.Rational(N11, 4) - 5) / 12 * 10
Q3_11 = 40 + (sp.Rational(3*N11, 4) - 35) / 10 * 10
Delta_Q11 = Q3_11 - Q1_11
print(f"P1 - Cau 11: Q1 = {Q1_11} ({float(Q1_11)}), Q3 = {Q3_11} ({float(Q3_11)}), Delta_Q = {Delta_Q11} ({float(Delta_Q11)})")

# Cau 12 [Van dung - Xac suat co dieu kien]: Mot hop co 6 bi do va 4 bi xanh. Lay ngau nhien lan luot 2 vien bi khong hoan lai.
# Tinh xac suat vien thu hai la bi do, biet vien thu nhat la bi xanh (hoac tinh P(A|B)).
# Hay bai toan: P(A) = 0.6, P(B) = 0.5, P(A cap B) = 0.3...
# Dung bai toan thuc tien: Mot nha may co 2 phan xuong I va II san xuat 60% va 40% san pham. Ti le phe pham tuong ung la 2% va 3%.
# Chon ngau nhien 1 san pham, xac suat chon duoc phe pham la:
P_phe_12 = sp.Rational(60, 100)*sp.Rational(2, 100) + sp.Rational(40, 100)*sp.Rational(3, 100)
print(f"P1 - Cau 12: Xac suat phe pham = {P_phe_12} = {float(P_phe_12)}")

# ---------------------------------------------------------
# PHAN II: 4 CAU TRAC NGHIEM DUNG/SAI
# ---------------------------------------------------------

print("\n--- PHAN II ---")
# Cau 1 [Ham so & Do thi]: Cho ham so f(x) = (x^2 - 2x + 5)/(x - 1)
f_p2_1 = (x**2 - 2*x + 5)/(x - 1)
df_p2_1 = sp.simplify(sp.diff(f_p2_1, x))
crit_p2_1 = sp.solve(df_p2_1, x)
asym_oblique = sp.apart(f_p2_1, x) # x - 1 + 4/(x - 1)
print(f"P2 - Cau 1: f(x) = {asym_oblique}, f'(x) = {df_p2_1}, cuc tri = {crit_p2_1}")
# a) Ham so dong bien tren (3; +oo) -> Dung (vi cuc tri tai x = -1, x = 3; f'(x) > 0 tren (-oo;-1) va (3;+oo))
# b) Do thi ham so co tiem can xien la duong thang y = x - 1 -> Dung
# c) Gia tri cuc dai cua ham so bang 6 -> Sai (Tai x = -1 la cuc dai: f(-1) = -4; tai x = 3 la cuc tieu: f(3) = 4)
# d) Duong thang di qua hai diem cuc tri cua do thi ham so co phuong trinh y = 2x - 2 -> Dung/Sai?
A_cd = (-1, f_p2_1.subs(x, -1))
B_ct = (3, f_p2_1.subs(x, 3))
print(f"   Cuc dai: {A_cd}, Cuc tieu: {B_ct}")
# Duong thang qua (-1, -4) va (3, 4): he so goc k = (4 - (-4))/(3 - (-1)) = 8/4 = 2 => y = 2(x - 3) + 4 = 2x - 2! Dung!

# Cau 2 [Giai tich 12 - Tich phan & Chuyen dong thuc tien]:
# Mot o to dang chay voi van toc 20 m/s thi nguoi lai xe dap phanh. Tu thoi diem do, o to chuyen dong cham dan deu
# voi van toc v(t) = -4t + 20 (m/s), trong do t la thoi gian tinh bang giay ke tu luc dap phanh.
v_t = -4*t + 20
t_stop = sp.solve(v_t, t)[0]
s_3 = sp.integrate(v_t, (t, 0, 3))
s_total = sp.integrate(v_t, (t, 0, t_stop))
# Gia su truoc khi dap phanh o to di voi van toc khong doi 20 m/s trong 2 giay, tong quang duong trong 7 giay (2s dau + 5s phanh):
s_total_7s = 20 * 2 + s_total
print(f"P2 - Cau 2: t_stop = {t_stop}s, s(3s) = {s_3}m, s_stop = {s_total}m, s(2s truoc + 5s phanh) = {s_total_7s}m")

# Cau 3 [Hinh hoc Oxyz]: Trong khong gian Oxyz, cho diem A(1; 2; -1), B(3; 0; 1) va mat phang (P): x - y + 2z - 5 = 0.
A_p2 = sp.Matrix([1, 2, -1])
B_p2 = sp.Matrix([3, 0, 1])
n_P_p2 = sp.Matrix([1, -1, 2])
AB_vec = B_p2 - A_p2 # (2, -2, 2)
M_mid = (A_p2 + B_p2) / 2 # (2, 1, 0)
# a) Vectơ AB = (2; -2; 2) -> Dung
# b) Mat phang trung truc cua doan thang AB co phuong trinh x - y + z - 1 = 0 -> Kiem tra: VTPT (1, -1, 1), qua M(2, 1, 0): 2 - 1 + 0 - 1 = 0 -> Dung
# c) Khoang cach tu diem A den mat phang (P) bang sqrt(6) -> Kiem tra: |1 - 2 + 2(-1) - 5|/sqrt(1+1+4) = 8/sqrt(6) = 4*sqrt(6)/3 -> Sai
d_A_P = abs(1 - 2 + 2*(-1) - 5) / sp.sqrt(1**2 + (-1)**2 + 2**2)
# d) Goi H la hinh chieu vuong goc cua A len (P). Toa do H:
# A + t*n_P = (1+t, 2-t, -1+2t) thuoc (P) => (1+t) - (2-t) + 2(-1+2t) - 5 = 0 => 6t - 8 = 0 (le).
# Doi phuong trinh (P) thanh x - y + 2z - 2 = 0 de H dep!
# Kiem tra voi (P): x - y + 2z + 3 = 0 => tai A(1,2,-1): 1 - 2 - 2 + 3 = 0 (A thuoc P).
# Thu (P): x - y + 2z - 3 = 0 => tai A(1,2,-1): 1 - 2 - 2 - 3 = -6 => 6t - 6 = 0 => t = 1!
# Khi do d(A, (P)) = 6/sqrt(6) = sqrt(6)! Va H = (1+1, 2-1, -1+2) = (2, 1, 1)! Rat dep!
t_H = sp.solve((1+t) - (2-t) + 2*(-1+2*t) - 3, t)[0]
H_coord = A_p2 + t_H * n_P_p2
d_A_P_new = abs(1 - 2 + 2*(-1) - 3) / sp.sqrt(1 + 1 + 4)
print(f"P2 - Cau 3 (voi P: x - y + 2z - 3 = 0): AB = {list(AB_vec)}, M = {list(M_mid)}, d(A,P) = {d_A_P_new}, H = {list(H_coord)}")

# Cau 4 [Xac suat co dieu kien & Bayes trong y hoc]:
# Mot benh vien thuc hien xet nghiem phat hien mot loai virus. Ti le nguoi mac benh trong cong dong la 5% (0.05).
# Neu mot nguoi mac benh, xac suat xet nghiem cho ket qua duong tinh la 96% (0.96).
# Neu mot nguoi khong mac benh, xac suat xet nghiem cho ket qua am tinh la 95% (0.95) (tuc duong tinh gia la 5% = 0.05).
P_A = sp.Rational(5, 100) # mac benh
P_notA = 1 - P_A # 0.95
P_B_given_A = sp.Rational(96, 100) # duong tinh | mac benh
P_B_given_notA = 1 - sp.Rational(95, 100) # 0.05 (duong tinh | khong mac benh)
P_B = P_A * P_B_given_A + P_notA * P_B_given_notA
P_A_given_B = (P_A * P_B_given_A) / P_B
print(f"P2 - Cau 4: P(A)={float(P_A)}, P(B|notA)={float(P_B_given_notA)}, P(B)={float(P_B)} ({P_B}), P(A|B)={float(P_A_given_B):.4f} ({P_A_given_B})")

# ---------------------------------------------------------
# PHAN III: 6 CAU TRAC NGHIEM TRA LOI NGAN
# ---------------------------------------------------------
print("\n--- PHAN III ---")

# Cau 1 [Van dung - Ham so / Toi uu thuc tien]:
# Mot doanh nghiep san xuat x san pham (1 <= x <= 1000). Chi phi san xuat x san pham la C(x) = x^2 + 30x + 400 (trieu dong),
# gia ban moi san pham la p(x) = 190 - x (trieu dong) voi 1 <= x <= 150.
# Loi nhuan L(x) = x * p(x) - C(x) = x(190 - x) - (x^2 + 30x + 400) = -2x^2 + 160x - 400.
# Tim x de loi nhuan lon nhat va tinh loi nhuan lon nhat do.
L_x = x*(190 - x) - (x**2 + 30*x + 400)
x_opt_1 = sp.solve(sp.diff(L_x, x), x)[0]
L_max_1 = L_x.subs(x, x_opt_1)
print(f"P3 - Cau 1: x_opt = {x_opt_1}, L_max = {L_max_1} (trieu dong)")

# Cau 2 [Van dung cao - Ung dung tich phan (Kinh te / Kien truc)]:
# Mot cong chao co hinh dang parabol y = -1/2 * x^2 + 8 (don vi: met), chan cong dat tren mat dat (truc hoanh Ox).
# Nguoi ta thiet ke mot khung cua hinh chu nhat noi tiep ben duoi cong parabol (hai dinh tren nam tren parabol, hai dinh duoi nam tren Ox)
# sao cho dien tich khung cua lon nhat. Tinh phan dien tich con lai cua cong chao (nam ngoai khung cua), lam tron den hang phan muoi.
# Hoac: Phan cua kinh trang tri gioi han boi y = -1/2 x^2 + 8 va y = 1/2 x^2, son 2 loai mau voi chi phi...
# Ta lam bai toan cong parabol + chi phi thuc tien:
# Cong parabol co chieu cao 8 m va chieu rong chan cong la 8 m => he truc Oxy voi dinh (0; 8), chan (-4; 0) va (4; 0) => y = 8 - x^2/2.
# Phan trung tam la cua go hinh chu nhat co chieu rong 4 m (tu x = -2 den x = 2) va chieu cao cham vao vach cong tai x = +-2 => cao y(2) = 8 - 2 = 6 m.
# Dien tich cua go: S_go = 4 * 6 = 24 m^2.
# Tong dien tich cong: S_total = int_{-4}^4 (8 - x^2/2) dx = 128/3 m^2.
# Phan con lai trang tri kinh nghe thuat. Gia lam cua go la 1.5 trieu/m^2, gia lam kinh nghe thuat la 2.4 trieu/m^2.
# Tinh tong chi phi (trieu dong): 24 * 1.5 + (128/3 - 24)*2.4 = 36 + (56/3)*2.4 = 36 + 56 * 0.8 = 36 + 44.8 = 80.8 (trieu dong)! So tuyet dep!
S_total_p3_2 = sp.integrate(8 - x**2 / 2, (x, -4, 4))
S_go_p3_2 = 4 * (8 - 2**2 / 2)
S_kinh_p3_2 = S_total_p3_2 - S_go_p3_2
cost_p3_2 = S_go_p3_2 * sp.Rational(15, 10) + S_kinh_p3_2 * sp.Rational(24, 10)
print(f"P3 - Cau 2: S_total = {S_total_p3_2}, S_go = {S_go_p3_2}, S_kinh = {S_kinh_p3_2}, Chi phi = {float(cost_p3_2)} trieu dong")

# Cau 3 [Van dung cao - Hinh hoc khong gian / Khoang cach giua 2 duong thang cheo nhau]:
# Cho hinh chop S.ABCD co day ABCD la hinh vuong canh 6, SA vuong goc voi day va SA = 3.
# Tinh khoang cach giua hai duong thang SB va DM, voi M la trung diem cua BC.
# Dat he truc Oxyz: A(0,0,0), B(6,0,0), D(0,6,0), C(6,6,0), S(0,0,3), M(6,3,0).
A3 = sp.Matrix([0, 0, 0])
B3 = sp.Matrix([6, 0, 0])
D3 = sp.Matrix([0, 6, 0])
C3 = sp.Matrix([6, 6, 0])
S3 = sp.Matrix([0, 0, 3])
M3 = sp.Matrix([6, 3, 0])
u_SB = B3 - S3 # (6, 0, -3)
u_DM = M3 - D3 # (6, -3, 0)
cross_3 = u_SB.cross(u_DM) # (-9, -18, -18)
SD_vec = D3 - S3 # (0, 6, -3)
dist_SB_DM = abs(cross_3.dot(SD_vec)) / cross_3.norm()
print(f"P3 - Cau 3: d(SB, DM) = {dist_SB_DM} = {float(dist_SB_DM)} (chinh xac 2!)")

# Cau 4 [Van dung cao - Oxyz Toi uu / Thuc tien]:
# Trong khong gian Oxyz (don vi tren moi truc la km), mot tram radar dat tai O(0;0;0), mot may bay khong nguoi lai (UAV)
# bay theo duong thang d đi qua A(2; 4; 4) va B(1; 2; 5). Tai diem M(a; b; c) tren quy dao bay d, UAV o gan tram radar O nhat.
# Tinh gia tri cua T = a + 2b + 3c (hoac tinh khoang cach ngan nhat, hoac a+b+c).
A4_p3 = sp.Matrix([2, 4, 4])
B4_p3 = sp.Matrix([1, 2, 5])
u4_p3 = B4_p3 - A4_p3 # (-1, -2, 1)
M4_t = A4_p3 + t * u4_p3
dist_sq_4 = M4_t.dot(M4_t)
t_min_4 = sp.solve(sp.diff(dist_sq_4, t), t)[0]
M4_opt = M4_t.subs(t, t_min_4)
T4 = M4_opt[0] + 2*M4_opt[1] + 3*M4_opt[2]
print(f"P3 - Cau 4: t_min = {t_min_4}, M = {list(M4_opt)}, OM_min = {sp.sqrt(dist_sq_4.subs(t, t_min_4))}, a+b+c = {sum(M4_opt)}, T = {T4}")

# Cau 5 [Van dung cao - Xac suat Bayes / Toan phan]:
# Co hai hop dung bi. Hop I co 5 vien bi do va 3 vien bi xanh. Hop II co 4 vien bi do va 6 vien bi xanh.
# Lay ngau nhien 1 vien bi tu hop I bo sang hop II, sau do lay ngau nhien 2 vien bi tu hop II.
# Biet rang 2 vien bi lay ra tu hop II deu la bi do, tinh xac suat vien bi chuyen tu hop I sang hop II la bi do.
# Goi A la bien co "vien bi chuyen tu I sang II la bi do": P(A) = 5/8, P(not A) = 3/8.
# Khi A xay ra: Hop II co 5 do, 6 xanh (tong 11). Xac suat lay 2 do: P(B|A) = C(5,2)/C(11,2) = 10/55 = 2/11.
# Khi not A xay ra: Hop II co 4 do, 7 xanh (tong 11). Xac suat lay 2 do: P(B|not A) = C(4,2)/C(11,2) = 6/55.
# P(B) = 5/8 * 10/55 + 3/8 * 6/55 = (50 + 18)/440 = 68/440 = 17/110.
# P(A|B) = 50 / 68 = 25/34.
# De ra so thap phan dep (vd phan tram hoac so thap phan dung):
# Thu Hop I co 6 do, 4 xanh: P(A) = 0.6, P(not A) = 0.4.
# Neu lay 1 vien tu Hop II (ban dau Hop II co 3 do, 6 xanh = 9 vien, them 1 vien la 10 vien!):
# Khi A xay ra (chuyen do): Hop II co 4 do, 6 xanh (10 vien) => lay 1 do: P(B|A) = 4/10 = 0.4.
# Khi not A xay ra (chuyen xanh): Hop II co 3 do, 7 xanh (10 vien) => lay 1 do: P(B|not A) = 3/10 = 0.3.
# P(B) = 0.6 * 0.4 + 0.4 * 0.3 = 0.24 + 0.12 = 0.36.
# Neu lay 2 vien tu Hop II (ban dau Hop II co 4 do, 5 xanh = 9 vien, them 1 vien la 10 vien):
# Khi A xay ra (chuyen do): Hop II co 5 do, 5 xanh => C(5,2)/C(10,2) = 10/45.
# Khi not A xay ra (chuyen xanh): Hop II co 4 do, 6 xanh => C(4,2)/C(10,2) = 6/45.
# Thu P(A) = p, P(not A) = 1-p sao cho 10*p + 6*(1-p) chia het:
# Voi Hop I co 7 do, 3 xanh (p = 0.7): 10*7 + 6*3 = 70 + 18 = 88.
# Voi Hop I co 3 do, 2 xanh (p = 3/5): 10*3 + 6*2 = 30 + 12 = 42.
# Voi Hop I co 3 do, 5 xanh: 10*3 + 6*5 = 30 + 30 = 60!
# Kiem tra: Hop I co 3 bi do, 5 bi xanh (8 vien). Hop II co 4 bi do, 5 bi xanh (9 vien).
# Chuyen 1 vien tu I sang II, roi lay ngau nhien 2 vien tu II:
# P(A) = 3/8, P(not A) = 5/8.
# P(B|A) = C(5,2)/C(10,2) = 10/45.
# P(B|not A) = C(4,2)/C(10,2) = 6/45.
# P(A|B) = (3/8 * 10/45) / (3/8 * 10/45 + 5/8 * 6/45) = 30 / (30 + 30) = 30/60 = 0.5! CUC KY DEP!
P_A_5 = sp.Rational(3, 8)
P_notA_5 = sp.Rational(5, 8)
P_B_A_5 = sp.binomial(5, 2) / sp.binomial(10, 2)
P_B_notA_5 = sp.binomial(4, 2) / sp.binomial(10, 2)
P_B_5 = P_A_5 * P_B_A_5 + P_notA_5 * P_B_notA_5
P_A_given_B_5 = (P_A_5 * P_B_A_5) / P_B_5
print(f"P3 - Cau 5: P(B) = {P_B_5} ({float(P_B_5):.2f}), P(A|B) = {P_A_given_B_5} = {float(P_A_given_B_5)}")

# Cau 6 [Van dung cao - Ham so / Tham so m hoac Toi uu hinh hoc 3D]:
# Mot tam nhom hinh vuong canh 12 dm. Nguoi ta cat o bon goc bon hinh vuong bang nhau co canh x (dm),
# roi gap tam nhom lai thanh mot cai hop khong nap. De the tich cua hop la lon nhat thi the tich do bang bao nhieu dm^3?
# Hoac bai toan duong day dien duoi nuoc & tren bo (Toi uu thuc tien VDC):
# Mot nha may dien dat tai A tren bo bien thang, mot hon dao C cach bo bien mot khoang CB = 4 km (CB vuong goc voi bo bien tai B),
# va khoang cach AB = 10 km. Chi phi lap dat day dien tren bo la 300 trieu dong/km, duoi nuoc la 500 trieu dong/km.
# Nguoi ta keo day tren bo tu A den M (nam giua A va B), roi keo ngam duoi nuoc tu M den C.
# Tim chi phi thap nhat (trieu dong) de lap dat duong day dien tu A den C.
# Goi BM = x (0 <= x <= 10) => AM = 10 - x, MC = sqrt(x^2 + 16).
# Chi phi F(x) = 300*(10 - x) + 500*sqrt(x^2 + 16).
F_cost = 300*(10 - x) + 500*sp.sqrt(x**2 + 16)
x_opt_6 = sp.solve(sp.diff(F_cost, x), x)[0]
min_cost_6 = F_cost.subs(x, x_opt_6)
print(f"P3 - Cau 6: BM = x = {x_opt_6} km, Chi phi nho nhat = {min_cost_6} trieu dong")

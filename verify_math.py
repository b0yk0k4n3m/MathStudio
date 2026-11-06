import sympy as sp

def verify_all():
    print("=== KIỂM CHỨNG TOÁN HỌC CHO ĐỀ THI ===")
    
    # ----------------------------------------------------
    # PHẦN I
    # ----------------------------------------------------
    print("\n--- PHẦN I ---")
    x = sp.Symbol('x')
    
    # Câu 1: Nguyên hàm 3x^2 + cos(x)
    f1 = 3*x**2 + sp.cos(x)
    F1 = sp.integrate(f1, x)
    print(f"Câu 1: int(3x^2 + cos(x)) = {F1} + C -> Đúng là x^3 + sin(x)")
    
    # Câu 2: Tính chất nguyên hàm
    print("Câu 2: Khẳng định sai: int(f*g) = int(f)*int(g) -> Lý thuyết chuẩn")
    
    # Câu 3: Tích phân int_1^5 = int_1^3 + int_3^5 = 4 + (-2) = 2
    print("Câu 3: 4 + (-2) = 2 -> Đáp án A")
    
    # Câu 4: int_0^1 (2f(x) - 1) dx = 2*3 - 1 = 5
    print("Câu 4: 2*3 - 1 = 5 -> Đáp án A")
    
    # Câu 5: int_0^1 (3x^2 + 2*e^x) dx
    f5 = 3*x**2 + 2*sp.exp(x)
    I5 = sp.integrate(f5, (x, 0, 1))
    print(f"Câu 5: int_0^1 (3x^2 + 2e^x) dx = {I5} = 2*E - 1 -> Đáp án A")
    
    # Câu 6: Tọa độ u = 2i - 3j + 5k -> (2; -3; 5)
    print("Câu 6: (2; -3; 5) -> Đáp án A")
    
    # Câu 7: A(1; 2; -1), B(3; 0; 0) -> AB = (2; -2; 1) -> |AB| = sqrt(4+4+1) = 3
    A = sp.Matrix([1, 2, -1])
    B = sp.Matrix([3, 0, 0])
    AB = B - A
    len_AB = AB.norm()
    print(f"Câu 7: AB = {AB.T}, len = {len_AB} -> Đáp án A")
    
    # Câu 8: u = (1, 0, -1), v = (1, 1, 0) -> cos = 1 / (sqrt(2)*sqrt(2)) = 1/2 -> 60 deg
    u = sp.Matrix([1, 0, -1])
    v = sp.Matrix([1, 1, 0])
    cos_uv = u.dot(v) / (u.norm() * v.norm())
    print(f"Câu 8: cos(u, v) = {cos_uv} -> góc = 60 độ -> Đáp án A")
    
    # Câu 9: (P): 2x - 3y + z - 4 = 0 -> n = (2; -3; 1)
    print("Câu 9: n = (2; -3; 1) -> Đáp án A")
    
    # Câu 10: Đi qua M(1; 2; -3), n = (2; -1; 4)
    # 2(x-1) - (y-2) + 4(z+3) = 2x - y + 4z + 12 = 0
    print("Câu 10: 2x - y + 4z + 12 = 0 -> Đáp án A")
    
    # Câu 11: P(A|B) = P(AB)/P(B)
    print("Câu 11: P(A|B) = P(AB)/P(B) -> Đáp án A")
    
    # Câu 12: P(A)=0.6, P(B)=0.5, P(AB)=0.3 -> P(A|B) = 0.3/0.5 = 0.6
    print(f"Câu 12: P(A|B) = 0.3/0.5 = {0.3/0.5} -> Đáp án A")

    # ----------------------------------------------------
    # PHẦN II
    # ----------------------------------------------------
    print("\n--- PHẦN II ---")
    # Câu 1: (P): y = -x^2 + 4x và d: y = x
    # a) Hoành độ giao điểm: -x^2 + 4x = x <=> -x^2 + 3x = 0 <=> x=0, x=3
    sols = sp.solve(-x**2 + 4*x - x, x)
    print(f"Câu 1a: Giao điểm x = {sols} -> Đúng")
    
    # b) Công thức S = int_0^3 (-x^2 + 3x) dx
    print("Câu 1b: Trên [0; 3], -x^2 + 4x >= x nên S = int_0^3 (-x^2 + 3x) dx -> Đúng")
    
    # c) S = 9/2
    S = sp.integrate(-x**2 + 3*x, (x, 0, 3))
    print(f"Câu 1c: S = {S} -> Đúng")
    
    # d) Thể tích khối tròn xoay khi quay (H) quanh Ox:
    # V = pi * int_0^3 [(-x^2 + 4x)^2 - x^2] dx
    integrand_V = (-x**2 + 4*x)**2 - x**2
    V = sp.pi * sp.integrate(integrand_V, (x, 0, 3))
    print(f"Câu 1d: V = {V} = {float(V/sp.pi)}*pi = 108pi/5")
    
    # Câu 2: Trong không gian Oxyz, cho A(1; 1; 0), B(0; 2; 1), C(1; 0; 2) và điểm M(2; 3; -1).
    A2 = sp.Matrix([1, 1, 0])
    B2 = sp.Matrix([0, 2, 1])
    C2 = sp.Matrix([1, 0, 2])
    M2 = sp.Matrix([2, 3, -1])
    
    AB2 = B2 - A2 # (-1, 1, 1)
    AC2 = C2 - A2 # (0, -1, 2)
    n_ABC = AB2.cross(AC2) # (3, 2, 1)
    print(f"Câu 2a, b: AB = {AB2.T}, AC = {AC2.T}, n = AB x AC = {n_ABC.T}")
    # Mặt phẳng (ABC): 3(x-1) + 2(y-1) + 1(z-0) = 0 <=> 3x + 2y + z - 5 = 0
    # Khoảng cách từ M(2; 3; -1) đến (ABC):
    # d = |3(2) + 2(3) + 1(-1) - 5| / sqrt(3^2 + 2^2 + 1^2) = |6 + 6 - 1 - 5| / sqrt(14) = 6 / sqrt(14) = 3*sqrt(14)/7
    dist_M = abs(3*2 + 2*3 + 1*(-1) - 5) / sp.sqrt(3**2 + 2**2 + 1**2)
    print(f"Câu 2c, d: d(M, (ABC)) = {dist_M} = {sp.simplify(dist_M)}")

    # ----------------------------------------------------
    # PHẦN III
    # ----------------------------------------------------
    print("\n--- PHẦN III ---")
    # Câu 1: int_1^4 [3f'(x) - 2x] dx = 3(f(4) - f(1)) - (4^2 - 1^2) = 3(11 - 2) - 15 = 27 - 15 = 12
    ans_III_1 = 3*(11 - 2) - (16 - 1)
    print(f"Phần III - Câu 1: {ans_III_1}")
    
    # Câu 2: v(t) = -4t + 20. Khi dừng v=0 => t=5. s = int_0^5 (-4t+20) dt
    t = sp.Symbol('t')
    s_stop = sp.integrate(-4*t + 20, (t, 0, 5))
    print(f"Phần III - Câu 2: Quãng đường dừng hẳn = {s_stop}")
    
    # Câu 3: Khoảng cách giữa 2 điểm A(1; 2; 3) và B(4; -2; 3)
    # AB = sqrt((4-1)^2 + (-2-2)^2 + (3-3)^2) = sqrt(9 + 16) = 5
    pA = sp.Matrix([1, 2, 3])
    pB = sp.Matrix([4, -2, 3])
    dist_AB = (pB - pA).norm()
    print(f"Phần III - Câu 3: Khoảng cách AB = {dist_AB}")
    
    # Câu 4: Xác suất Bayes
    # P(B1) = 0.6, P(B2) = 0.4
    # P(A|B1) = 0.02, P(A|B2) = 0.03
    # P(A) = 0.6*0.02 + 0.4*0.03 = 0.012 + 0.012 = 0.024
    # P(B1|A) = 0.012 / 0.024 = 0.5
    PA = 0.6*0.02 + 0.4*0.03
    PB1_given_A = (0.6*0.02) / PA
    print(f"Phần III - Câu 4: P(A) = {PA}, P(B1|A) = {PB1_given_A}")

    # ----------------------------------------------------
    # PHẦN IV
    # ----------------------------------------------------
    print("\n--- PHẦN IV ---")
    # Bài 1: y = sqrt(2x + 1), x in [0, 4] quanh Ox
    # V = pi * int_0^4 (2x + 1) dx = pi * [x^2 + x]_0^4 = pi * (16 + 4) = 20*pi
    V_rot = sp.pi * sp.integrate(2*x + 1, (x, 0, 4))
    print(f"Phần IV - Bài 1: Thể tích = {V_rot}")
    
    # Bài 2: Mái che qua A(0; 0; 3), B(6; 0; 4), C(0; 8; 5).
    # u = AB = (6, 0, 1), v = AC = (0, 8, 2)
    # n = AB x AC = (0*2 - 1*8; 1*0 - 6*2; 6*8 - 0*0) = (-8; -12; 48) = -4 * (2; 3; -12)
    # Chọn n = (2; 3; -12)
    # Mp (P): 2(x-0) + 3(y-0) - 12(z-3) = 0 <=> 2x + 3y - 12z + 36 = 0.
    u_roof = sp.Matrix([6, 0, 1])
    v_roof = sp.Matrix([0, 8, 2])
    n_roof = u_roof.cross(v_roof)
    print(f"Phần IV - Bài 2: n_raw = {n_roof.T}")
    n_roof_simp = sp.Matrix([2, 3, -12])
    dist_S = abs(2*3 + 3*4 - 12*6 + 36) / n_roof_simp.norm()
    print(f"Phần IV - Bài 2: Khoảng cách = {dist_S} ≈ {float(dist_S):.2f} m")
    cos_angle = 12 / n_roof_simp.norm()
    angle_deg = sp.acos(cos_angle) * 180 / sp.pi
    print(f"Phần IV - Bài 2: cos(alpha) = {cos_angle} ≈ {float(cos_angle):.4f}, góc = {float(angle_deg):.2f} độ")

if __name__ == '__main__':
    verify_all()

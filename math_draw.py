"""
Module math_draw.py: Thư viện tự động vẽ Đồ thị hàm số và Hình học không gian chuẩn sư phạm THPT.
Sử dụng Matplotlib với phong cách sách giáo khoa chuẩn Việt Nam:
- Trục tọa độ Oxy có mũi tên, gốc O, nhãn trục, vạch chia rõ ràng.
- Tiệm cận đứng, ngang, xiên vẽ nét đứt (dashed).
- Các điểm đặc biệt (cực trị, giao điểm) có đường gióng nét đứt tới các trục.
- Hình học không gian tuân thủ quy ước nét thấy (solid), nét khuất (dashed), ký hiệu đỉnh và góc vuông.
- Xuất file ảnh PNG chất lượng cao vào output/images/ để nhúng trực tiếp vào Đề thi Markdown & Word.
"""

import math
import os
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Chế độ headless cho server
import matplotlib.pyplot as plt
import numpy as np

# Thư mục lưu ảnh mặc định
IMAGES_DIR = Path("output/images")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)


def _setup_oxy_axes(ax, x_min=-5, x_max=5, y_min=-5, y_max=5):
    """Thiết lập hệ trục tọa độ Oxy chuẩn phong cách toán học Việt Nam."""
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_color("none")
    ax.spines["top"].set_color("none")

    # Mũi tên ở đầu trục
    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False, markersize=5)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False, markersize=5)

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # Nhãn trục
    ax.text(x_max + 0.15, -0.35, "$x$", fontsize=12, fontweight="bold", fontstyle="italic")
    ax.text(-0.35, y_max + 0.15, "$y$", fontsize=12, fontweight="bold", fontstyle="italic")
    ax.text(-0.35, -0.35, "$O$", fontsize=11, fontstyle="italic")

    # Tọa độ chia vạch
    x_ticks = [i for i in range(math.floor(x_min), math.ceil(x_max) + 1) if i != 0]
    y_ticks = [i for i in range(math.floor(y_min), math.ceil(y_max) + 1) if i != 0]
    ax.set_xticks(x_ticks)
    ax.set_yticks(y_ticks)
    ax.tick_params(axis="both", which="major", labelsize=9)
    ax.grid(True, linestyle=":", alpha=0.35, color="#94A3B8")


def draw_cubic(a: float, b: float, c: float, d: float, x_range=(-4, 4), y_range=None, out_name="dothi_bac3.png") -> Path:
    """
    Vẽ đồ thị hàm số bậc ba: y = ax^3 + bx^2 + cx + d
    Tự động xác định các điểm cực trị, điểm uốn và gióng nét đứt tới các trục.
    """
    out_path = IMAGES_DIR / out_name
    fig, ax = plt.subplots(figsize=(6, 5), dpi=200)

    # 1. Tính toán cực trị
    # y' = 3ax^2 + 2bx + c
    delta_prime = b**2 - 3*a*c
    crit_pts = []
    if delta_prime > 1e-9:
        x1 = (-b - math.sqrt(delta_prime)) / (3*a)
        x2 = (-b + math.sqrt(delta_prime)) / (3*a)
        crit_pts = sorted([x1, x2])

    # Điểm uốn
    x_u = -b / (3*a)
    y_u = a*x_u**3 + b*x_u**2 + c*x_u + d

    # Tự động cân đối y_range nếu chưa cho
    y_vals_crit = [a*x**3 + b*x**2 + c*x + d for x in crit_pts] + [d, y_u]
    if y_range is None:
        y_min = min(y_vals_crit) - 3 if y_vals_crit else -5
        y_max = max(y_vals_crit) + 3 if y_vals_crit else 5
        y_span = max(abs(y_min), abs(y_max), 4)
        y_range = (-y_span, y_span)

    _setup_oxy_axes(ax, x_range[0], x_range[1], y_range[0], y_range[1])

    # Vẽ đường cong
    xs = np.linspace(x_range[0], x_range[1], 400)
    ys = a*xs**3 + b*xs**2 + c*xs + d
    ax.plot(xs, ys, color="#1E40AF", linewidth=2.0, label=f"$y = {a}x^3 + {b}x^2 + {c}x + {d}$")

    # Đánh dấu các điểm cực trị & đường gióng nét đứt
    for xc in crit_pts:
        yc = a*xc**3 + b*xc**2 + c*xc + d
        if x_range[0] <= xc <= x_range[1] and y_range[0] <= yc <= y_range[1]:
            ax.plot(xc, yc, "o", color="#DC2626", markersize=5)
            ax.plot([xc, xc], [0, yc], "--", color="#DC2626", alpha=0.6, linewidth=1)
            ax.plot([0, xc], [yc, yc], "--", color="#DC2626", alpha=0.6, linewidth=1)

    # Đánh dấu giao điểm trục Oy
    if y_range[0] <= d <= y_range[1]:
        ax.plot(0, d, "o", color="#1E40AF", markersize=4)

    plt.tight_layout()
    fig.savefig(str(out_path), bbox_inches="tight")
    plt.close(fig)
    return out_path


def draw_rational_1_1(a: float, b: float, c: float, d: float, x_range=(-5, 5), y_range=(-5, 5), out_name="dothi_nhat_bien.png") -> Path:
    """
    Vẽ đồ thị hàm nhất biến y = (ax + b) / (cx + d)
    Bao gồm tiệm cận đứng x = -d/c và tiệm cận ngang y = a/c nét đứt màu đỏ.
    """
    out_path = IMAGES_DIR / out_name
    fig, ax = plt.subplots(figsize=(6, 5), dpi=200)
    _setup_oxy_axes(ax, x_range[0], x_range[1], y_range[0], y_range[1])

    x_tc = -d / c
    y_tc = a / c

    # Vẽ tiệm cận đứng (nét đứt)
    if x_range[0] <= x_tc <= x_range[1]:
        ax.axvline(x=x_tc, color="#DC2626", linestyle="--", linewidth=1.2, label=f"TCĐ: $x = {x_tc:.2g}$")
        ax.text(x_tc + 0.1, y_range[1] - 0.7, f"$x = {x_tc:.2g}$", color="#DC2626", fontsize=9)

    # Vẽ tiệm cận ngang (nét đứt)
    if y_range[0] <= y_tc <= y_range[1]:
        ax.axhline(y=y_tc, color="#DC2626", linestyle="--", linewidth=1.2, label=f"TCN: $y = {y_tc:.2g}$")
        ax.text(x_range[1] - 1.5, y_tc + 0.15, f"$y = {y_tc:.2g}$", color="#DC2626", fontsize=9)

    # Tâm đối xứng I
    if x_range[0] <= x_tc <= x_range[1] and y_range[0] <= y_tc <= y_range[1]:
        ax.plot(x_tc, y_tc, "o", color="#DC2626", markersize=4)
        ax.text(x_tc - 0.35, y_tc + 0.2, "$I$", color="#DC2626", fontsize=10, fontweight="bold")

    # Vẽ 2 nhánh đồ thị (tránh điểm gián đoạn)
    delta = 0.05
    x_left = np.linspace(x_range[0], x_tc - delta, 250)
    y_left = (a*x_left + b) / (c*x_left + d)
    mask_l = (y_left >= y_range[0]) & (y_left <= y_range[1])
    ax.plot(x_left[mask_l], y_left[mask_l], color="#1E40AF", linewidth=2.0)

    x_right = np.linspace(x_tc + delta, x_range[1], 250)
    y_right = (a*x_right + b) / (c*x_right + d)
    mask_r = (y_right >= y_range[0]) & (y_right <= y_range[1])
    ax.plot(x_right[mask_r], y_right[mask_r], color="#1E40AF", linewidth=2.0)

    # Giao điểm trục tung (0, b/d)
    y_oy = b / d
    if y_range[0] <= y_oy <= y_range[1]:
        ax.plot(0, y_oy, "o", color="#1E40AF", markersize=4)

    plt.tight_layout()
    fig.savefig(str(out_path), bbox_inches="tight")
    plt.close(fig)
    return out_path


def draw_rational_2_1(a: float, b: float, c: float, p: float, q: float, x_range=(-6, 6), y_range=(-6, 6), out_name="dothi_phan_thuc_2_1.png") -> Path:
    """
    Vẽ đồ thị hàm phân thức bậc 2 / bậc 1 (Toán 12 GDPT 2018): y = (ax^2 + bx + c) / (px + q)
    Bao gồm Tiệm cận đứng x = -q/p và Tiệm cận xiên y = mx + n nét đứt.
    """
    out_path = IMAGES_DIR / out_name
    fig, ax = plt.subplots(figsize=(6, 5), dpi=200)
    _setup_oxy_axes(ax, x_range[0], x_range[1], y_range[0], y_range[1])

    # Chia đa thức: (ax^2 + bx + c) / (px + q) = (a/p)x + (b - a*q/p)/p + ...
    m = a / p
    n = (b - a * q / p) / p
    x_tc = -q / p

    # 1. Tiệm cận đứng
    if x_range[0] <= x_tc <= x_range[1]:
        ax.axvline(x=x_tc, color="#DC2626", linestyle="--", linewidth=1.2)
        ax.text(x_tc + 0.1, y_range[1] - 0.7, f"TCĐ: $x = {x_tc:.2g}$", color="#DC2626", fontsize=9)

    # 2. Tiệm cận xiên y = mx + n
    xs_ob = np.linspace(x_range[0], x_range[1], 100)
    ys_ob = m * xs_ob + n
    mask_ob = (ys_ob >= y_range[0]) & (ys_ob <= y_range[1])
    ax.plot(xs_ob[mask_ob], ys_ob[mask_ob], color="#DC2626", linestyle="--", linewidth=1.2)
    ax.text(x_range[1] - 2.2, m*(x_range[1]-2.2) + n + 0.3, "TCX: $y = mx + n$", color="#DC2626", fontsize=8.5)

    # Giao điểm 2 tiệm cận (Tâm đối xứng)
    y_I = m * x_tc + n
    if x_range[0] <= x_tc <= x_range[1] and y_range[0] <= y_I <= y_range[1]:
        ax.plot(x_tc, y_I, "o", color="#DC2626", markersize=4)
        ax.text(x_tc - 0.4, y_I + 0.2, "$I$", color="#DC2626", fontsize=10, fontweight="bold")

    # 3. Vẽ 2 nhánh đường cong
    delta = 0.05
    x_left = np.linspace(x_range[0], x_tc - delta, 300)
    y_left = (a*x_left**2 + b*x_left + c) / (p*x_left + q)
    mask_l = (y_left >= y_range[0]) & (y_left <= y_range[1])
    ax.plot(x_left[mask_l], y_left[mask_l], color="#1E40AF", linewidth=2.0)

    x_right = np.linspace(x_tc + delta, x_range[1], 300)
    y_right = (a*x_right**2 + b*x_right + c) / (p*x_right + q)
    mask_r = (y_right >= y_range[0]) & (y_right <= y_range[1])
    ax.plot(x_right[mask_r], y_right[mask_r], color="#1E40AF", linewidth=2.0)

    plt.tight_layout()
    fig.savefig(str(out_path), bbox_inches="tight")
    plt.close(fig)
    return out_path


def draw_pyramid_sa_bottom(out_name="hinh_chop_sa_vuong_day.png") -> Path:
    """
    Vẽ khối chóp S.ABCD có SA vuông góc đáy ABCD (Đáy hình chữ nhật/hình vuông).
    Chuẩn quy ước hình học SGK:
    - Nét khuất (AB, AD, SA): nét đứt '--'
    - Nét thấy (BC, CD, SB, SC, SD): nét liền '-'
    - Ký hiệu góc vuông tại A.
    """
    out_path = IMAGES_DIR / out_name
    fig, ax = plt.subplots(figsize=(5.5, 4.8), dpi=200)
    ax.set_aspect("equal")
    ax.axis("off")

    # Tọa độ các đỉnh (phép chiếu song song)
    # Đáy ABCD dạng hình bình hành
    A = np.array([0.0, 0.0])
    B = np.array([3.5, 0.0])
    D = np.array([-1.5, -1.5])
    C = B + D - A  # = [2.0, -1.5]

    # Đỉnh S dựng thẳng đứng từ A (SA vuông góc đáy)
    S = np.array([0.0, 3.2])

    # Các đoạn nét khuất (dashed)
    ax.plot([A[0], B[0]], [A[1], B[1]], "--k", linewidth=1.2)  # AB
    ax.plot([A[0], D[0]], [A[1], D[1]], "--k", linewidth=1.2)  # AD
    ax.plot([S[0], A[0]], [S[1], A[1]], "--k", linewidth=1.2)  # SA

    # Các đoạn nét thấy (solid)
    ax.plot([D[0], C[0]], [D[1], C[1]], "-k", linewidth=1.5)  # DC
    ax.plot([B[0], C[0]], [B[1], C[1]], "-k", linewidth=1.5)  # BC
    ax.plot([S[0], B[0]], [S[1], B[1]], "-k", linewidth=1.5)  # SB
    ax.plot([S[0], C[0]], [S[1], C[1]], "-k", linewidth=1.5)  # SC
    ax.plot([S[0], D[0]], [S[1], D[1]], "-k", linewidth=1.5)  # SD

    # Ký hiệu góc vuông tại đỉnh A (đáy)
    sq_size = 0.35
    v_b = (B - A) / np.linalg.norm(B - A) * sq_size
    v_d = (D - A) / np.linalg.norm(D - A) * sq_size
    p1 = A + v_b
    p2 = A + v_b + v_d
    p3 = A + v_d
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], "--k", linewidth=0.8)

    # Nhãn các đỉnh
    offset = 0.18
    ax.text(S[0], S[1] + offset, "$S$", fontsize=13, fontweight="bold", ha="center")
    ax.text(A[0] - offset, A[1] + offset, "$A$", fontsize=12, fontweight="bold")
    ax.text(B[0] + offset, B[1], "$B$", fontsize=12, fontweight="bold")
    ax.text(C[0] + offset, C[1] - offset, "$C$", fontsize=12, fontweight="bold")
    ax.text(D[0] - offset*1.5, D[1] - offset, "$D$", fontsize=12, fontweight="bold")

    plt.tight_layout()
    fig.savefig(str(out_path), bbox_inches="tight")
    plt.close(fig)
    return out_path


def draw_prism_abc(out_name="lang_tru_tam_giac.png") -> Path:
    """
    Vẽ hình lăng trụ đứng tam giác ABC.A'B'C'.
    Quy ước nét khuất nét thấy chuẩn SGK.
    """
    out_path = IMAGES_DIR / out_name
    fig, ax = plt.subplots(figsize=(5.5, 4.8), dpi=200)
    ax.set_aspect("equal")
    ax.axis("off")

    A = np.array([0.0, 0.0])
    B = np.array([3.0, -0.6])
    C = np.array([1.2, -1.6])

    h = np.array([0.0, 3.0])
    A1, B1, C1 = A + h, B + h, C + h

    # Đáy trên A'B'C': Nét thấy
    ax.plot([A1[0], B1[0]], [A1[1], B1[1]], "-k", linewidth=1.5)
    ax.plot([B1[0], C1[0]], [B1[1], C1[1]], "-k", linewidth=1.5)
    ax.plot([C1[0], A1[0]], [C1[1], A1[1]], "-k", linewidth=1.5)

    # Đáy dưới ABC: AC, BC thấy, AB khuất
    ax.plot([A[0], B[0]], [A[1], B[1]], "--k", linewidth=1.2)  # AB khuất
    ax.plot([B[0], C[0]], [B[1], C[1]], "-k", linewidth=1.5)
    ax.plot([C[0], A[0]], [C[1], A[1]], "-k", linewidth=1.5)

    # Cạnh bên: AA', BB', CC'
    ax.plot([A[0], A1[0]], [A[1], A1[1]], "--k", linewidth=1.2)  # AA' khuất
    ax.plot([B[0], B1[0]], [B[1], B1[1]], "-k", linewidth=1.5)
    ax.plot([C[0], C1[0]], [C[1], C1[1]], "-k", linewidth=1.5)

    # Nhãn
    off = 0.18
    ax.text(A[0] - off*1.5, A[1], "$A$", fontsize=12, fontweight="bold")
    ax.text(B[0] + off, B[1], "$B$", fontsize=12, fontweight="bold")
    ax.text(C[0], C[1] - off*1.5, "$C$", fontsize=12, fontweight="bold", ha="center")

    ax.text(A1[0] - off*1.5, A1[1], "$A'$", fontsize=12, fontweight="bold")
    ax.text(B1[0] + off, B1[1], "$B'$", fontsize=12, fontweight="bold")
    ax.text(C1[0], C1[1] + off, "$C'$", fontsize=12, fontweight="bold", ha="center")

    plt.tight_layout()
    fig.savefig(str(out_path), bbox_inches="tight")
    plt.close(fig)
    return out_path

import sympy as sp

x, m = sp.symbols('x m', real=True)

# Original function: f(x) = x^3 - 6*x^2 + 9*x - 5
# f'(x) = 3*x^2 - 12*x + 9 = 3*(x - 1)*(x - 3)
# Let's consider a VDC (Van dung cao) problem developed from f(x) = x^3 - 6*x^2 + 9*x - 5:
# Find the number of integer values of parameter m in [-20; 20] such that the function
# g(x) = f(x^2 - 2*x + m) - 3*x^2 + 6*x is decreasing on (1; 2) (or strictly increasing on (2; 3)).
# Wait, let's check g'(x):
# Let u = x^2 - 2*x + m, u' = 2*(x - 1).
# g(x) = f(x^2 - 2*x + m) - 3/2 * (x^2 - 2*x)^2 + ... or simpler:
# g(x) = f(|x^2 - 4x + m|) or g(x) = f(x^2 - 2x + m)
# If g(x) = f(x^2 - 2x + m), then g'(x) = 2*(x - 1) * f'(x^2 - 2x + m) = 6*(x - 1)*(x^2 - 2x + m - 1)*(x^2 - 2x + m - 3).
# On interval (1; 3), x - 1 > 0.
# For g(x) to be decreasing on (1; 2):
# Since x in (1; 2) => x - 1 > 0, we need f'(x^2 - 2x + m) <= 0 for all x in (1; 2).
# f'(u) <= 0 <=> 1 <= u <= 3.
# On (1; 2), t = x^2 - 2x takes values in (-1; 0).
# So 1 <= t + m <= 3 for all t in (-1; 0) <=> 1 - t <= m <= 3 - t for all t in (-1; 0)
# max_{(-1, 0]} (1 - t) = 1 - (-1) = 2; min_{[-1, 0)} (3 - t) = 3 - 0 = 3.
# Wait, if we ask for g(x) = |f(x^2 - 4x) + m| or g(x) = f(|x + m|) or g(x) = f(x^2 - 2x + m) - 9*(x^2 - 2x)...
# Let's make an even better VDC question:
# "Cho hàm số f(x) = x^3 - 6x^2 + 9x - 5. Có bao nhiêu giá trị nguyên của tham số m thuộc đoạn [-10; 10] để hàm số g(x) = f(x^2 - 2x + m) nghịch biến trên khoảng (1; 2)?" -> Only m in [2, 3], too easy or maybe good?
# What if g(x) = f(x^2 - 6x + m) nghịch biến trên khoảng (1; 2)?
# Let's test with sympy!

f = x**3 - 6*x**2 + 9*x - 5
# Let u = x**2 - 4*x + m
# Or let's consider: g(x) = f(x - m) - 3*m*x ...
# Better VDC: Cho hàm số f(x) = x^3 - 6x^2 + 9x - 5. Gọi S là tập hợp tất cả các giá trị nguyên của tham số m để hàm số g(x) = |f(x^2 - 4x + 3) - m| đồng biến trên khoảng (2; 3) (hoặc có bao nhiêu giá trị nguyên của m để hàm số g(x) = f(|x^3 - 3x + m|) ...).
# Wait, the original question is about "Hàm số nghịch biến trên khoảng nào dưới đây?".
# Developing it to VDC while keeping the theme of "khoảng nghịch biến của hàm hợp" or "tìm tham số m để hàm số hợp nghịch biến trên khoảng":
# Let's check both types or a classic VDC parameter problem on monotonicity of composite function derived directly from f(x) = x^3 - 6x^2 + 9x - 5:
# Problem: Cho hàm số f(x) = x^3 - 6x^2 + 9x - 5. Có bao nhiêu giá trị nguyên của tham số m để hàm số g(x) = f(x^2 - 2mx + m^2 + 1) nghịch biến trên khoảng (1; 2)?
# Wait: u = (x - m)^2 + 1 >= 1.
# g'(x) = 2(x - m) * f'((x - m)^2 + 1).
# Since f'(u) = 3(u - 1)(u - 3), for u = (x - m)^2 + 1:
# u - 1 = (x - m)^2 >= 0!
# That's SO CLEAN! Look at that:
# f'(u) = 3 * (x - m)^2 * ((x - m)^2 - 2).
# Then g'(x) = 6 * (x - m)^3 * ((x - m)^2 - 2) = 6 * (x - m)^3 * (x - m - sqrt(2)) * (x - m + sqrt(2)).

u = x**2 - 2*m*x + m**2 + 1
g = f.subs(x, u)
g_prime = sp.factor(sp.diff(g, x))
print("g'(x) =", g_prime)

# What if u = x^2 - 2*m*x + m^2 + 3 = (x - m)^2 + 3? No, u = (x - m)^2 + 1 gives (x - m)^2 - 2.
# If we want integer roots, let's see: f'(u) = 3(u - 1)(u - 3).
# If we want u - 1 and u - 3 to factor nicely, or if we use:
# g(x) = f(x^2 - 2x + m) + 12*x^2 - 24*x
# Let h(u) = f(u) + 12*u = u^3 - 6u^2 + 21u - 5 -> h'(u) > 0.
# What if g(x) = f(2 - x^2) + ...
# Or what if: Cho hàm số f(x) = x^3 - 6x^2 + 9x - 5. Hàm số g(x) = f(x^2 - 2x) - \frac{3}{2}x^4 + 6x^3 - \frac{3}{2}x^2 - 6x + 2026 nghịch biến trên khoảng nào?
# Wait: let u = x^2 - 2x. Then u^2 = x^4 - 4x^3 + 4x^2.
# So -3/2 * u^2 = -3/2 x^4 + 6 x^3 - 6 x^2.
# Let's check g(x) = f(u) - 3/2 u^2 - 9 u!
# Let's test k(u) = f(u) - 3/2 u^2 + ...
# Or how about a parameter m problem with integer values?
# Let's check: g(x) = f(-x^2 + 2x + m).
# g'(x) = (-2x + 2) * f'(-x^2 + 2x + m) = -6(x - 1)(-x^2 + 2x + m - 1)(-x^2 + 2x + m - 3).
# Suppose we ask: Có bao nhiêu giá trị nguyên của tham số m thuộc đoạn [-20; 20] để hàm số g(x) = f(|x^2 - 4x + m|) nghịch biến trên khoảng (1; 2)?
# No, let's make sure the condition is unambiguous and 100% solid in Vietnamese high school curriculum:
# Let's check:
# "Cho hàm số f(x) = x^3 - 6x^2 + 9x - 5. Có bao nhiêu giá trị nguyên của tham số m thuộc đoạn [-10; 10] để hàm số g(x) = f(x^2 - 4x + m) nghịch biến trên khoảng (0; 1)?"
# Wait: on (0; 1), u(x) = x^2 - 4x + m has u'(x) = 2x - 4 < 0 on (0; 1).
# Since g'(x) = u'(x) * f'(u(x)), and u'(x) < 0 on (0; 1),
# g(x) nghịch biến trên (0; 1) <=> g'(x) <= 0 on (0; 1) <=> f'(u(x)) >= 0 on (0; 1).
# Since f'(u) = 3(u - 1)(u - 3), f'(u) >= 0 <=> u <= 1 or u >= 3.
# Since u(x) = x^2 - 4x + m is continuous on [0; 1] and strictly decreasing on (0; 1), its image on (0; 1) is (m - 3; m).
# Therefore, f'(u(x)) >= 0 for all x in (0; 1) <=> (m - 3; m) is a subset of (-infty; 1] OR (m - 3; m) is a subset of [3; +infty).
# Case 1: m <= 1.
# Case 2: m - 3 >= 3 <=> m >= 6.
# With m in [-10; 10] and m integer:
# Case 1: m in {-10, -9, ..., 1} -> 12 values.
# Case 2: m in {6, 7, 8, 9, 10} -> 5 values.
# Total = 17 values!
# Let's verify this with SymPy!

u2 = x**2 - 4*x + m
g2 = f.subs(x, u2)
g2_prime = sp.factor(sp.diff(g2, x))
print("g2'(x) =", g2_prime)

valid_m = []
for m_val in range(-10, 11):
    expr = g2_prime.subs(m, m_val)
    # Check if expr <= 0 for all x in (0, 1)
    # Test at sample points and check roots in (0, 1)
    roots_in_interval = [r for r in sp.solve(expr, x) if r.is_real and 0 < r < 1]
    val_mid = expr.subs(x, sp.Rational(1, 2))
    if val_mid <= 0 and all(expr.subs(x, sp.Rational(k, 100)) <= 0 for k in range(1, 100)):
        valid_m.append(m_val)

print("Valid m in [-10, 10]:", valid_m)
print("Count:", len(valid_m))

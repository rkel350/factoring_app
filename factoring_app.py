import streamlit as st
import math

st.title("Polynomial Factoring Assistant")
st.markdown("Enter the coefficients of your polynomial as comma-separated values (e.g. `2, 3, 1` for `2x² + 3x + 1`)")

def is_perfect_square(n):
    return n >= 0 and int(math.isqrt(n)) ** 2 == n

def is_perfect_cube(n):
    if n < 0:
        root = round(abs(n) ** (1/3))
        return -root**3 == n
    root = round(n ** (1/3))
    return root ** 3 == n

def gcd_list(nums):
    result = abs(nums[0])
    for n in nums[1:]:
        result = math.gcd(result, abs(n))
    return result

def format_binomial(coef, var, const):
    if coef == 1:
        x_part = var
    elif coef == -1:
        x_part = f"-{var}"
    else:
        x_part = f"{coef}{var}"
    sign = "+" if const >= 0 else "-"
    return f"({x_part} {sign} {abs(const)})"

input_str = st.text_input("Polynomial Coefficients:")

if input_str:
    try:
        terms = [int(x.strip()) for x in input_str.split(",")]
        num_terms = len(terms)
        factoring_method = ""
        factored_form = ""

        # GCF
        gcf = gcd_list(terms)
        if gcf != 1:
            terms = [x // gcf for x in terms]
            factoring_method += "GCF + "

        # 2-term Cubes
        if num_terms == 2:
            a, b = terms
            if is_perfect_cube(a) and is_perfect_cube(b):
                a_root = round(abs(a) ** (1/3)) * (-1 if a < 0 else 1)
                b_root = round(abs(b) ** (1/3)) * (-1 if b < 0 else 1)
                if b > 0:
                    factoring_method += "Sum of Cubes"
                    factored_form = f"({a_root}x + {b_root})({a_root**2}x^2 - {a_root*b_root}x + {b_root**2})"
                else:
                    factoring_method += "Difference of Cubes"
                    factored_form = f"({a_root}x - {abs(b_root)})({a_root**2}x^2 + {abs(a_root*b_root)}x + {b_root**2})"

        # 3-term Trinomials
        elif num_terms == 3:
            a, b, c = terms
            if b == 0 and is_perfect_square(a) and is_perfect_square(-c):
                sqrt_a = int(math.isqrt(a))
                sqrt_c = int(math.isqrt(-c))
                factoring_method += "Difference of Squares"
                factored_form = f"({sqrt_a}x + {sqrt_c})({sqrt_a}x - {sqrt_c})"
            elif is_perfect_square(a) and is_perfect_square(c):
                sqrt_a = int(math.isqrt(a))
                sqrt_c = int(math.isqrt(c))
                if b == 2 * sqrt_a * sqrt_c:
                    factoring_method += "Perfect Square Trinomial"
                    factored_form = f"({sqrt_a}x + {sqrt_c})^2"
                elif b == -2 * sqrt_a * sqrt_c:
                    factoring_method += "Perfect Square Trinomial"
                    factored_form = f"({sqrt_a}x - {sqrt_c})^2"
            if not factored_form:
                for m in range(1, abs(a) * 10 + 1):
                    if a % m != 0:
                        continue
                    n = a // m
                    for p in range(-abs(c) * 10, abs(c) * 10 + 1):
                        if p == 0 or c % p != 0:
                            continue
                        q = c // p
                        if m * q + n * p == b:
                            factoring_method += "Trinomial (AC Method)"
                            factored_form = format_binomial(m, "x", p) + format_binomial(n, "x", q)
                            break
                    if factored_form:
                        break

        # 4-term Grouping
        elif num_terms == 4:
            a, b, c, d = terms
            def factor_pair(x, y):
                g = math.gcd(x, y)
                return (g, x // g, y // g) if g else (0, x, y)
            g1, a1, b1 = factor_pair(a, b)
            g2, c1, d1 = factor_pair(c, d)
            if (a1, b1) == (c1, d1):
                inner = f"({a1}x + {b1})"
                outer1 = "x" if g1 == 1 else (f"-x" if g1 == -1 else f"{g1}x")
                outer2 = f"{g2}"
                factoring_method += "Factoring by Grouping"
                factored_form = f"({outer1} + {outer2}){inner}"

        if factored_form:
            st.success(f"**Factoring method used:** {factoring_method}")
            st.code(factored_form, language="latex")
        else:
            st.warning("This expression cannot be factored over the integers.")

    except:
        st.error("Invalid input. Please enter comma-separated integers.")

import streamlit as st
import math
import re
import random

from PIL import Image

logo = Image.open("JJsMathLab.png")
st.image(logo, width=150)

st.title("Polynomial Factoring Assistant")
st.subheader("Hi JJ! 👋 I made this app just for you ❤️\n Use responsibly!")
st.markdown("For 2 or 3 term polynomials, enter the full equation (e.g. `x^2 -49` or `2x^2 +6x -3`). For 4 terms or higher, enter the coefficients of your polynomial as comma-separated values (e.g. `2, 3, 1` for `2x² + 3x + 1`)")

def parse_quadratic(equation):
    equation = equation.replace(" ", "")
    if equation[0] != "-":
        equation = "+" + equation
    terms = re.findall(r'[+-][^+-]+', equation)
    a = b = c = 0
    for term in terms:
        if "x^2" in term:
            num = term.replace("x^2", "")
            a = int(num) if num not in ["+", "-"] else int(num + "1")
        elif "x" in term:
            num = term.replace("x", "")
            b = int(num) if num not in ["+", "-"] else int(num + "1")
        else:
            c = int(term)
    return [a, b, c]

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

def clean_input(expr):
    # Insert * between variables and coefficients (e.g., 2xy → 2*x*y)
    # This finds things like "2xy" or "ab", and adds the *s
    expr = re.sub(r'(?<=[a-zA-Z])(?=[a-zA-Z])', '*', expr)      # ab → a*b
    expr = re.sub(r'(?<=\d)(?=[a-zA-Z])', '*', expr)            # 2x → 2*x
    expr = re.sub(r'(?<=[a-zA-Z])(?=\()', '*', expr)            # x(y+1) → x*(y+1)
    return expr

input_str = st.text_input("Enter a polynomial (e.g. `x^2 + 5x + 6` or `1,5,6`):")

if input_str:
    try:
        # Detect if it's a full expression or just coefficients
        if "x" in input_str.lower():
            terms = parse_quadratic(input_str)
        else:
            terms = [int(x.strip()) for x in input_str.split(",")]
        st.caption(f"Parsed coefficients: {terms}")
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

                    if factored_form:
                        # Display factored form immediately
                        st.success(f"**Factoring method used:** {factoring_method}")
                        st.code(factored_form, language="latex")

                        # Step 1: Create the step-by-step breakdown
                        step_by_step = f"""
                            1. **Identify coefficients**: A = {a}, B = {b}, C = {c}  
                            2. **Multiply A × C**: {a} × {c} = {a * c}  
                            3. **Find two numbers that multiply to A × C ( {a * c} ) and add to B ({b})**:  
                               → {m} × {q} = {a * c} and {m} + {q} = {b}  
                            4. **Rewrite middle term using those numbers**:  
                               {a}x² + {m}x + {q}x + {c}  
                            5. **Group and factor**:  
                               ({a}x² + {m}x) + ({q}x + {c})  
                            6. **Factor each group**:  
                               {math.gcd(a, m)}x({a // math.gcd(a, m)}x + {m // math.gcd(a, m)}) + {math.gcd(q, c)}({q // math.gcd(q, c)})x + {c // math.gcd(q, c)}  
                            7. **Final factor**: {factored_form}
                        """

                        # Step 2: Add the "Show steps" button below the factored form
                        if st.button("Show steps"):
                            st.markdown(step_by_step)  # Show the detailed steps only when clicked

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

            messages = [
                "Griddy on 'em, JJ! 🕺🔥",
                "Certified Math Savage 😤",
                "Clean factor. Clean Griddy. ✅",
                "Ain’t no one stopping this Algebra drip 💧",
                "Big brain energy. 🧠🎉",
                "That math move was disrespectful 🔥",
                "That was illegal in 47 states 💥",
                "That factor was so clean it squeaked ✨",
                "JJ just speedran algebra like it's minecraft ⛏️",
                "That polynomial just got bodied 💪",
                "+1000 XP unlocked 🔓",
            ]
            st.info(random.choice(messages))
        else:
            st.warning("This expression cannot be factored over the integers.")

    except:
        st.error("Invalid input. Please enter comma-separated integers.")

#advanced logic block
from sympy import symbols, sympify, factor, latex

st.markdown("---")
st.subheader("Advanced: Factor any algebraic expression (like `ab^2 + a^2b - 5a - 5b`)")

advanced_input = st.text_input("Enter expression (multivariable OK):")

if advanced_input:
    try:
        cleaned = clean_input(advanced_input)
        expr = sympify(cleaned)
        factored_expr = factor(expr)
        st.success("Factored expression:")
        st.latex(latex(factored_expr))  # ✅ Pretty LaTeX output
    except Exception as e:
        st.error(f"Could not factor expression: {e}")


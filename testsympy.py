# --- SymPy test (optional) ---
if __name__ == "__main__":
    from sympy import symbols, factor

    a, b = symbols('a b')
    expr = a*b**2 + a**2*b - 5*a - 5*b
    print("Test factor result:", factor(expr))

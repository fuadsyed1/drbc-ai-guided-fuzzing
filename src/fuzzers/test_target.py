from src.targets.calculator import eval_expr

try:
    result = eval_expr("1+2")
    print(result)

except Exception as e:
    print(f"ERROR: {e}")
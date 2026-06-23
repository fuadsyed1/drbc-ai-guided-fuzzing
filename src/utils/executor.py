import time
from src.targets.calculator import eval_expr


def execute_input(test_input):
    start_time = time.perf_counter()

    try:
        output = eval_expr(test_input)
        status = "PASS"
        error_type = None
        error_message = None

    except Exception as error:
        output = None
        status = "CRASH"
        error_type = type(error).__name__
        error_message = str(error)

    end_time = time.perf_counter()

    return {
        "input": test_input,
        "status": status,
        "output": output,
        "error_type": error_type,
        "error_message": error_message,
        "execution_time": end_time - start_time,
    }
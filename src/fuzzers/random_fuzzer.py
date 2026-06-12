import random
from src.targets.calculator import eval_expr

CHARS = "0123456789+-*/()abcxyz"

def generate_input(max_length=20):
    length = random.randint(1, max_length)
    return "".join(random.choice(CHARS) for _ in range(length))

def run_fuzzer(iterations=100):
    ok_count = 0
    error_count = 0

    with open("results/logs/random_fuzzer.log", "w") as log:

        for i in range(iterations):
            test_input = generate_input()

            try:
                result = eval_expr(test_input)
                ok_count += 1
                print(f"[OK] {test_input} => {result}")

            except Exception as e:
                error_count += 1
                message = f"[ERROR] {test_input} => {e}"
                print(message)
                log.write(message + "\n")

        summary = (
            f"\nSummary:\n"
            f"Total inputs: {iterations}\n"
            f"Successful inputs: {ok_count}\n"
            f"Error inputs: {error_count}\n"
        )

        print(summary)
        log.write(summary)

if __name__ == "__main__":
    run_fuzzer()
from src.targets.calculator import eval_expr

TEST_INPUTS = [
    "1+2",
    "(4+5)*3",
    "10/0",
    "999999999999999999999*999999999999999999999",
    "1++2",
    "abc+1",
    "(1+2",
    "5/0",
    "7*(8+9)",
]

def run_ai_fuzzer():
    ok_count = 0
    error_count = 0

    with open("results/logs/ai_fuzzer.log", "w") as log:

        for test_input in TEST_INPUTS:

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
            f"Total inputs: {len(TEST_INPUTS)}\n"
            f"Successful inputs: {ok_count}\n"
            f"Error inputs: {error_count}\n"
        )

        print(summary)
        log.write(summary)

if __name__ == "__main__":
    run_ai_fuzzer()
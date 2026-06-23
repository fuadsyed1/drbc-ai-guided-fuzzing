from src.utils.executor import execute_input


TEST_INPUTS = [
    "1+2",
    "1/0",
    "(1+2",
    "abc+1",
    "999*999",
]


def verify_crash_detection():
    for test_input in TEST_INPUTS:
        result = execute_input(test_input)

        print("\n------------------")
        print(result)


if __name__ == "__main__":
    verify_crash_detection()
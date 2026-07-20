import random
import string


STRATEGY_NAME = "basic_character_random"

GENERAL_CHARSET = (
    string.ascii_letters
    + string.digits
    + string.punctuation
    + " \n\t"
)


def generate_input(max_length=50):
    length = random.randint(0, max_length)
    return "".join(random.choice(GENERAL_CHARSET) for _ in range(length))


def generate_inputs(target, count=100):
    return [generate_input() for _ in range(count)]
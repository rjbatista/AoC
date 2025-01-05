""" Advent of code 2024 - day 22 """

from collections import defaultdict
from pathlib import Path

########
# PART 1


def read(filename: str) -> list[str]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [int(line.strip()) for line in file.readlines()]


def gen_secret_number(number: int, count: int = 2000) -> int:
    """ Generate the secret number after count times """

    for _ in range(count):
        number = (number << 6 ^ number) % 16777216
        number = (number >> 5 ^ number) % 16777216
        number = (number << 11 ^ number) % 16777216

    return number


ex1 = read("example1.txt")
assert sum(gen_secret_number(n) for n in ex1) == 37327623

inp = read("input.txt")
ANSWER = sum(gen_secret_number(n) for n in inp)
print("Part 1 =", ANSWER)
assert ANSWER == 17163502021  # check with accepted answer

########
# PART 2


def get_best_sequence(numbers: list[int], count: int = 2000, seq_size: int = 4) -> tuple[int, tuple[int, ...]]:
    """ Get the best sequence value """
    total_for_seq = defaultdict(lambda: 0)

    for number in numbers:
        current_sequence = ()
        last_digit = None
        seen_sequences = set()
        for _ in range(count):
            number = (number << 6 ^ number) % 16777216
            number = (number >> 5 ^ number) % 16777216
            number = (number << 11 ^ number) % 16777216

            digit = number % 10
            if last_digit is not None:
                diff = digit - last_digit
                current_sequence = (current_sequence + (diff,))[-seq_size:]

                if len(current_sequence) == seq_size and current_sequence not in seen_sequences:
                    total_for_seq[current_sequence] += digit
                    seen_sequences.add(current_sequence)

            last_digit = digit

    return max(total_for_seq.values())


ex2 = read("example2.txt")
assert get_best_sequence(ex2) == 23

ANSWER = get_best_sequence(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 1938  # check with accepted answer

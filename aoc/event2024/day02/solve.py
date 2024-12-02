""" Advent of code 2024 - day 02 """

from pathlib import Path

########
# PART 1

def read(filename: str) -> list[list[int]]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return list(list(map(int, line.split())) for line in file)


def unsafe_pos(lst: list[int]) -> int:
    """ Check if a list is safe """
    diffs = list(x-y for x, y in zip(lst, lst[1:]))

    first = diffs[0]

    if not 1 <= abs(first) <= 3:
        return 0

    sign = first > 0

    for p, d in enumerate(diffs[1:], 1):
        if (not 1 <= abs(d) <= 3) or (sign and d < 0) or (not sign and d > 0):
            return p

    return None


def is_safe(lst: list[int]) -> bool:
    """ Check if a list is safe """
    return unsafe_pos(lst) is None


ex1 = read("example1.txt")
assert sum(1 for x in ex1 if is_safe(x)) == 2

inp = read("input.txt")
ANSWER = sum(1 for x in inp if is_safe(x))
print("Part 1 =", ANSWER)
assert ANSWER == 383  # check with accepted answer


########
# PART 2

def is_safe_with_dampener(lst: list[int]):
    """ Check is a list is safe using dampener if necessary """

    pos = unsafe_pos(lst)
    if pos is None:
        return True

    before = pos - 1 if pos > 0 else 0
    after = pos + 1 if pos < len(lst) else len(lst)

    return any(is_safe(lst[:x] + lst[x + 1:]) for x in tuple({pos, before, after}))


assert sum(1 for x in ex1 if is_safe_with_dampener(x)) == 4

ANSWER = sum(1 for x in inp if is_safe_with_dampener(x))
print("Part 2 =", ANSWER)
assert ANSWER == 436  # check with accepted answer

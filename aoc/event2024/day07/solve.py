""" Advent of code 2024 - day 07 """

from pathlib import Path
from operator import mul, add

########
# PART 1

type Equation = tuple[int, tuple[int, ...]]


def read(filename: str) -> list[Equation]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:

        equations = []
        for line in file:
            total, numbers = line.split(':')
            numbers = map(int, numbers.split())

            equations.append((int(total), tuple(numbers)))

        return equations


def has_valid_combination(equation: Equation,
                          valid_operators=(mul, add)) -> bool:
    def _try(equation: Equation, current, valid_operators) -> bool:

        result, numbers = equation
        first, rest = numbers[0], numbers[1:]

        for op in valid_operators:
            val = op(current, first)

            if rest:
                if val <= result:
                    if _try((result, rest), val, valid_operators):
                        return True
            else:
                if val == result:
                    return True

        return False

    result, numbers = equation
    first, rest = numbers[0], numbers[1:]
    return _try((result, rest), first, valid_operators)


ex1 = read("example1.txt")

assert sum(result for result, numbers in ex1
           if has_valid_combination((result, numbers))) == 3749

inp = read("input.txt")
ANSWER = sum(result for result, numbers in inp
             if has_valid_combination((result, numbers)))
print("Part 1 =", ANSWER)
assert ANSWER == 1298300076754  # check with accepted answer

########
# PART 2


def concat(x: int, y: int) -> int:
    """
    The concatenation operator (||) combines the digits from its left and
    right inputs into a single number.
    For example, 12 || 345 would become 12345.
    """
    return int(str(x) + str(y))


assert sum(result for result, numbers in ex1
           if has_valid_combination((result, numbers), (mul, add, concat))) == 11387


ANSWER = sum(result for result, numbers in inp
             if has_valid_combination((result, numbers), (mul, add, concat)))
print("Part 2 =", ANSWER)
assert ANSWER == 248427118972289  # check with accepted answer

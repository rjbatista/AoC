""" Advent of code 2023 - day 06 """
from functools import reduce
import math
from pathlib import Path

########
# PART 1


def read(filename: str) -> list[tuple[int, int]]:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        times = map(int, file.readline().split()[1:])
        distances = map(int, file.readline().split()[1:])

        return list(zip(times, distances))


def quadratic(coef_a, coef_b, coef_c):
    """ Solve the quadratic for ax^2 + bx + c """
    if coef_a == 0:
        if coef_b == 0:
            return [0] if coef_c == 0 else []

        return [-coef_c / coef_b]

    discriminant = coef_b**2 - 4 * coef_a * coef_c

    if discriminant < 0:
        return []  # only complex solutions - not relevant

    if discriminant == 0:
        return [-coef_b / 2 * coef_a]

    return [(-coef_b + math.sqrt(discriminant)) / (2 * coef_a),
            (-coef_b - math.sqrt(discriminant)) / (2 * coef_a)]


def find_values(time: int, distance: int) -> int:
    """ find the values that win """
    # f(x) = - x ^ 2 + time * x - distance, for inequality, find the roots for one more millimeter
    coef = quadratic(-1, time, -(distance + 1))

    min_value = math.ceil(coef[0])
    max_value = math.floor(coef[1])

    return max_value - min_value + 1


ex1 = read("example1.txt")
assert reduce(lambda x, y: x * y, (find_values(t, d) for (t, d) in ex1)) == 288


inp = read("input.txt")
ANSWER = reduce(lambda x, y: x * y, (find_values(t, d) for (t, d) in inp))
print("Part 1 =", ANSWER)
assert ANSWER == 138915  # check with accepted answer

########
# PART 2


def reinterpret(values: list[tuple[int, int]]) -> tuple[int, int]:
    """ reinterpret the input for part 2 """
    return list(map(int,
                    reduce(lambda x, y: (str(x[0]) + str(y[0]), str(x[1]) + str(y[1])), values)))


assert find_values(*reinterpret(ex1)) == 71503

ANSWER = find_values(*reinterpret(inp))
print("Part 2 =", ANSWER)
assert ANSWER == 27340847  # check with accepted answer

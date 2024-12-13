""" Advent of code 2024 - day 13 """

from math import inf
from pathlib import Path
import re
import numpy as np

########
# PART 1

Equation = tuple[int, int, int]


def read(filename: str) -> list[tuple[Equation, Equation]]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        button_pattern = re.compile(r"^Button .: X\+(\d+), Y\+(\d+)$")
        prize_pattern = re.compile(r"^Prize: X=(\d+), Y=(\d+)$")

        equations = []
        while True:
            x_a, y_a = tuple(map(int, button_pattern.match(file.readline()).groups()))
            x_b, y_b = tuple(map(int, button_pattern.match(file.readline()).groups()))
            res_x, res_y = tuple(map(int, prize_pattern.match(file.readline()).groups()))

            eq1 = x_a, y_a, res_x
            eq2 = x_b, y_b, res_y

            equations.append((eq1, eq2))

            if not file.readline():
                break

        return equations


def solve(equations: list[tuple[Equation, Equation]], limit=100) -> list[tuple[int, int]]:
    """ solve the equations """

    results = []
    for eq1, eq2 in equations:
        x_a, y_a, res_x = eq1
        x_b, y_b, res_y = eq2

        a = np.array([[x_a, x_b], [y_a, y_b]])
        b = np.array([res_x, res_y])
        presses_a, presses_b = map(round, np.linalg.solve(a, b))

        if (0 <= presses_a <= limit and 0 <= presses_b <= limit
                and presses_a * x_a + presses_b * x_b == res_x
                and presses_a * y_a + presses_b * y_b == res_y):

            results.append((int(presses_a), int(presses_b)))

    return results


def cost(presses_a: int, presses_b: int) -> int:
    """ calculate the cost """
    return presses_a * 3 + presses_b


ex1 = read("example1.txt")
assert sum(cost(*presses) for presses in solve(ex1)) == 480

inp = read("input.txt")
ANSWER = sum(cost(*presses) for presses in solve(inp))
print("Part 1 =", ANSWER)
assert ANSWER == 37128  # check with accepted answer

########
# PART 2


def raise_prizes(equations: list[tuple[Equation, Equation]],
                 value=10000000000000) -> list[tuple[Equation, Equation]]:
    """ Raize the prizes """

    return [((x_a, y_a, res_x + value), (x_b, y_b, res_y + value))
            for (x_a, y_a, res_x), (x_b, y_b, res_y) in equations]


ANSWER = sum(cost(*presses) for presses in solve(raise_prizes(inp), limit=inf))
print("Part 2 =", ANSWER)
assert ANSWER == 74914228471331  # check with accepted answer

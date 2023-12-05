""" Advent of code 2023 - day 01 """
from pathlib import Path
import re

########
# PART 1


def read(filename: str) -> list[str]:
    """ Read the file """
    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [x.strip() for x in file.readlines()]


def get_calibration_value(text: str) -> int:
    """ Get the calibration value """

    first = 0
    while not text[first].isdigit():
        first += 1

    last = len(text) - 1
    while not text[last].isdigit():
        last -= 1

    return int(text[first] + text[last])


def get_calibration_values(values: list[str]):
    """ Get the calibration value for the list """
    return [get_calibration_value(x) for x in values]


ex1 = read("example1.txt")
assert sum(get_calibration_values(ex1)) == 142

inp = read("input.txt")
ANSWER = sum(get_calibration_values(inp))
print("Part 1 =", ANSWER)
assert ANSWER == 54450  # check with accepted answer

########
# PART 2

_DIGITS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

# using lookahead because it requires overlapping matches to find the right answer
_RE_DIGITS = re.compile(r'(?=(\d|' + '|'.join(_DIGITS.keys()) + '))')


def get_calibration_value_p2(text: str) -> int:
    """ Get the calibration value for part 2 """
    all_matches = _RE_DIGITS.findall(text)
    first = all_matches[0]
    last = all_matches[-1]

    return int(
        (first if first.isdigit() else _DIGITS[first])
        + (last if last.isdigit() else _DIGITS[last]))


def get_calibration_values_p2(values: list[str]):
    """ Get the calibration value for the list """
    return [get_calibration_value_p2(x) for x in values]


ex2 = read("example2.txt")
assert sum(get_calibration_values_p2(ex2)) == 281

ANSWER = sum(get_calibration_values_p2(inp))
print("Part 2 =", ANSWER)
assert ANSWER == 54265  # check with accepted answer

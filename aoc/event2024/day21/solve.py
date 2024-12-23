""" Advent of code 2024 - day 21 """

from collections import Counter
from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]


def read_keypads(filename: str) -> list[dict[str, Coord]]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        all_keypads = []
        keypad = {}
        start = 0

        for y, line in enumerate(file):
            line = line.rstrip()

            if not line:
                all_keypads.append(keypad)
                keypad = {}
                start = y

            for x, ch in enumerate(line):
                keypad[ch] = x, y - start

        if keypad:
            all_keypads.append(keypad)

        return all_keypads


def read(filename: str) -> list[str]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [line.strip() for line in file.readlines()]


def update_moves(wanted: str, keypad: dict[str, Coord], counter: Counter, times=1):
    """ Get the moves for the wanted string, for the specified number of times """
    x, y = keypad['A']
    nope = keypad[' ']

    for ch in wanted:
        nx, ny = keypad[ch]
        must_skip_hole = nope in ((x, ny), (nx, y))
        counter[((nx - x, ny - y), must_skip_hole)] += times
        x, y = nx, ny


def get_directions(pos: Coord, must_skip_hole: bool):
    """ Get the directions for the specified position, checking for holes """
    x, y = pos

    return ("<" * -x + "v" * y + "^" * -y + ">" * x)[:: -1 if must_skip_hole else 1] + "A"


def get_keystrokes_for_you(wanted: str, no_robots: int = 2):
    """ Get the keystrokes for you necessary for the wanted string """

    todo = Counter()
    update_moves(wanted, KEYPADS[0], todo)

    for _ in range(no_robots + 1):
        new_todo = Counter()
        for (pos, f), times in todo.items():
            update_moves(get_directions(pos, f), KEYPADS[1], new_todo, times)

        todo = new_todo

    return todo.total()


def get_complexity(wanted: str, no_robots: int = 2):
    """ Get the complexy for the wanted string """

    return get_keystrokes_for_you(wanted, no_robots) * int(wanted[:-1])


KEYPADS = read_keypads("keypads.txt")
ex1 = read("example1.txt")

assert sum(get_complexity(wanted) for wanted in ex1) == 126384

inp = read("input.txt")
ANSWER = sum(get_complexity(wanted) for wanted in inp)
print("Part 1 =", ANSWER)
assert ANSWER == 278748  # check with accepted answer

########
# PART 2

ANSWER = sum(get_complexity(wanted, 25) for wanted in inp)
print("Part 2 =", ANSWER)
assert ANSWER == 337744744231414  # check with accepted answer

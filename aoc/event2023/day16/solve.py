""" Advent of code 2023 - day 16 """
from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]
type Contraption = tuple[int, int, dict[Coord, str]]


def read(filename: str) -> Contraption:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        max_x = 0
        max_y = 0
        layout = {}

        for y, line in enumerate(file):
            max_y = max(y, max_y)
            for x, val in enumerate(line.strip()):
                max_x = max(x, max_x)

                if val != '.':
                    layout[x, y] = val

        return max_x + 1, max_y + 1, layout


# pylint: disable-msg=too-many-locals
def calculate_light(contraption: Contraption,
                    start: Coord = (-1, 0), direction: Coord = (1, 0)) -> int:
    """ Calculate the number of energized tiles """

    def bitwise_direction(dx: int, dy: int) -> int:
        val = 0
        val |= (1 if dx < 0 else 0) << 0
        val |= (1 if dx > 0 else 0) << 1
        val |= (1 if dy < 0 else 0) << 2
        val |= (1 if dy > 0 else 0) << 3

        return val

    width, height, layout = contraption
    todo = [(start, direction)]
    energized = {}
    while todo:
        (x, y), (dx, dy) = todo.pop()

        current_value = energized.get((x, y), 0)
        new_value = bitwise_direction(dx, dy)

        if new_value & current_value == new_value:
            # bean already passed here in this direction
            continue

        energized[x, y] = current_value | new_value
        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height:
            tile = layout.get((nx, ny), 0)

            if tile == '-' and dy != 0:
                todo.append(((nx, ny), (-1, 0)))
                todo.append(((nx, ny), (1, 0)))
            elif tile == '|' and dx != 0:
                todo.append(((nx, ny), (0, -1)))
                todo.append(((nx, ny), (0, 1)))
            elif tile == '\\':
                todo.append(((nx, ny), (dy, dx)))
            elif tile == '/':
                todo.append(((nx, ny), (-dy, -dx)))
            else:
                todo.append(((nx, ny), (dx, dy)))

    return len(energized) - 1


ex1 = read("example1.txt")
assert calculate_light(ex1) == 46

inp = read("input.txt")
ANSWER = calculate_light(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 7939  # check with accepted answer

########
# PART 2


def calculate_best(contraption: Contraption) -> int:
    """ Calculate the most energized by picking the start """

    # should be done by a depth first search discarding
    # results with the same status and less energized
    # but this is quick enough, so mehhhh

    width, height, _ = contraption
    best = 0
    for x in range(width):
        best = max(best, calculate_light(contraption, (x, -1), (0, 1)))
        best = max(best, calculate_light(contraption, (x, height), (0, -1)))
    for y in range(height):
        best = max(best, calculate_light(contraption, (-1, y), (1, 0)))
        best = max(best, calculate_light(contraption, (width, y), (-1, 0)))

    return best


assert calculate_best(ex1) == 51

ANSWER = calculate_best(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 8318  # check with accepted answer

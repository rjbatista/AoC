""" Advent of code 2023 - day XX """
from math import inf
from pathlib import Path
from PIL import Image

########
# PART 1

type DigInstr = tuple[str, int, int]
type Coord = tuple[int, int]
type DigSite = dict[Coord, int]


def read(filename: str) -> list[DigInstr]:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [(val[0], int(val[1]), int(val[2][2:-1], 16))
                for val in (line.split() for line in file)]


def print_dig(dig_site: DigSite) -> None:
    """ Print the dig site onto a image file """

    min_x, min_y = inf, inf
    max_x, max_y = -inf, -inf

    for x, y in dig_site:
        min_x, min_y = min(min_x, x), min(min_y, y)
        max_x, max_y = max(max_x, x), max(max_y, y)

    img = Image.new("RGB", (max_x - min_x + 1, max_y - min_y + 1))
    img.putdata([dig_site.get((x, y), 0xffffff)
                 for y in range(min_y, max_y + 1)
                 for x in range(min_x, max_x + 1)])
    img.save(Path(__file__).parent.joinpath('dig_site.png'))


def flood_fill(dig_site: DigSite):
    """ Fill the dig site """

    start = min(dig_site.keys())
    start = start[0] + 1, start[1] + 1
    dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    todo = [start]

    while todo:
        x, y = todo.pop()

        dig_site[x, y] = 0xb0b0b0

        for dx, dy in dirs:
            nx, ny = x + dx, y + dy

            if (nx, ny) not in dig_site:
                todo.append((nx, ny))


def dig(dig_plan: list[DigInstr]) -> DigSite:
    """ Run through the dig plan """
    dig_site = {}
    x, y = 0, 0
    directions = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}
    for direction, length, color in dig_plan:
        dx, dy = directions[direction]
        for _ in range(length):
            dig_site[x, y] = color
            x += dx
            y += dy

    flood_fill(dig_site)

    return dig_site


ex1 = read("example1.txt")
assert len(dig(ex1)) == 62

inp = read("input.txt")
ANSWER = len(dig(inp))
print("Part 1 =", ANSWER)
assert ANSWER == 47527  # check with accepted answer


########
# PART 2


def shoelace_area(polygon: list[Coord]) -> int:
    """
    Calculate the area for the polygon using the shoelace formula
    (https://en.wikipedia.org/wiki/Shoelace_formula)

    The absolute value is used so we don't have to check
    if the polygon is positively oriented or negatively oriented

    A = 1/2 * abs(sum(x{i} * (y{i + 1} - y{y - 1})))
    """
    total = 0
    for i, (xi, _) in enumerate(polygon):
        next_index = (i + 1) % len(polygon)
        prev_index = i - 1
        total += xi * (polygon[next_index][1] - polygon[prev_index][1])

    return abs(total) // 2


def get_dig_area(dig_plan: list[DigInstr]) -> list[Coord]:
    """ Run through the dig plan """
    vertices = []
    x, y = 0, 0
    directions = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}
    border_area = 0
    for direction, length, _ in dig_plan:
        dx, dy = directions[direction]
        x += dx * length
        y += dy * length
        border_area += length
        vertices.append((x, y))

    # the area calculated includes the points on the left top of the border,
    # but not the right, bottom. So I calculate the border and add half the border

    return shoelace_area(vertices) + border_area // 2 + 1


def correct_instructions(dig_plan: list[DigInstr]) -> list[Coord]:
    """ Correct the instructions """
    directions = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}

    return [(directions[color % 0x10], color // 0x10, 0) for _, _, color in dig_plan]


# reuse for part 1
assert get_dig_area(ex1) == 62
assert get_dig_area(inp) == 47527

assert get_dig_area(correct_instructions(ex1)) == 952408144115

ANSWER = get_dig_area(correct_instructions(inp))
print("Part 2 =", ANSWER)
assert ANSWER == 52240187443190  # check with accepted answer

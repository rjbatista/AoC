""" Advent of code 2023 - day 14 """
from pathlib import Path

########
# PART 1

type Coord = tuple(int, int)
type Platform = tuple(int, int, dict[Coord, str])


def read(filename: str) -> Platform:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        area = {}
        max_x = 0
        max_y = 0
        for y, line in enumerate(file):
            max_y = max(max_y, y)
            for x, ch in enumerate(line.strip()):
                max_x = max(max_x, x)
                if ch in ['#', 'O']:
                    area[x, y] = ch

        return max_x + 1, max_y + 1, area


def print_platform(platform: Platform) -> None:
    """ Prints the platform """
    width, height, area = platform

    for y in range(height):
        for x in range(width):
            ch = area.get((x, y), '.')

            print(ch, end="")
        print()
    print()


def tilt(platform: Platform, dx: int, dy: int) -> None:
    """ Tilts the platform in the specified direction """
    width, height, area = platform

    if dy:
        def sort_key(coord: Coord):
            return coord[1]
        sort_dir = dy > 0
    else:
        def sort_key(coord: Coord):
            return coord[0]
        sort_dir = dx > 0

    todo = sorted((c for c, ch in area.items() if ch == 'O'), key=sort_key, reverse=sort_dir)
    for x, y in todo:
        while True:
            nx, ny = x + dx, y + dy

            if not 0 <= nx < width:
                break
            if not 0 <= ny < height:
                break
            if area.get((nx, ny), '.') != '.':
                break

            del area[x, y]
            area[nx, ny] = 'O'

            todo.append((nx, ny))


def calculate_load(platform: Platform) -> int:
    """ Calculate the load on the platform """
    _, len_y, area = platform

    return sum(len_y - y for (_, y), ch in area.items() if ch == 'O')


ex1 = read("example1.txt")
tilt(ex1, 0, -1)
assert calculate_load(ex1) == 136

inp = read("input.txt")
tilt(inp, 0, -1)
ANSWER = calculate_load(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 108144  # check with accepted answer

########
# PART 2


def do_cycle(platform: Platform):
    """ Executes a cycle """
    for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        tilt(platform, dx, dy)


def find_cycle(platform: Platform) -> tuple[int, int]:
    """ Repeat the tilts until a cycle is found, returning the cycle start and length """
    known = {}
    width, height, area = platform
    area = area.copy()

    count = 0
    while True:
        key = str(sorted(area.items()))

        if key in known:
            break

        known[key] = count
        count += 1
        do_cycle((width, height, area))

    return known[key], count - known[key]


def do_cycles(platform: Platform, num: int = 1000000000):
    """ Simulate a large number of cycles """

    cycle_start, cycle_len = find_cycle(platform)

    todo_cycles = (num - cycle_start) % cycle_len + cycle_start
    for _ in range(todo_cycles):
        do_cycle(platform)


ex1 = read("example1.txt")
do_cycles(ex1)
assert calculate_load(ex1) == 64

inp = read("input.txt")
do_cycles(inp)
ANSWER = calculate_load(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 108404  # check with accepted answer

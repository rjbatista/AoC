""" Advent of code 2023 - day 03 """
from functools import reduce
from pathlib import Path

########
# PART 1

Coord = tuple[int, int]
Symbols = dict[Coord, str]
Numbers = dict[Coord, int]
Schematic = tuple[Coord, Symbols, Numbers]


def read(filename: str) -> Schematic:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        symbols = {}
        numbers = {}
        acc = None
        acc_x = 0
        max_x = 0
        max_y = 0

        for y, line in enumerate(file):
            max_y = max(y, max_y)
            for x, val in enumerate(line.strip()):
                max_x = max(x, max_x)

                if acc:
                    if val.isdigit():
                        acc = acc * 10 + int(val)
                        continue

                    numbers[acc_x, y] = acc
                    acc = None

                if val != '.':
                    if val.isdigit():
                        acc = int(val)
                        acc_x = x
                    else:
                        symbols[x, y] = val

            if acc:
                numbers[acc_x, y] = acc
                acc = None

        return (max_y, max_y), symbols, numbers


def is_part_number(coord: Coord, val: int, schematic: Schematic) -> bool:
    """ Check if the specified item is a part number """

    (max_x, max_y), symbols, _ = schematic
    x, y = coord
    val_len = len(str(val))

    for dy in [-1, 0, 1]:
        for dx in range(-1, val_len + 1):
            if dy == 0 and 0 <= dx < val_len:
                continue

            nx, ny = x + dx, y + dy
            if (0 <= nx <= max_x) and (0 <= ny <= max_y):
                if (nx, ny) in symbols:
                    return True

    return False


def get_part_numbers(schematic: Schematic) -> list[int]:
    """ Get all the part numbers in the schematic """
    _, _, numbers = schematic

    return [val for coord, val in numbers.items() if is_part_number(coord, val, schematic)]


ex1 = read("example1.txt")
assert sum(get_part_numbers(ex1)) == 4361

inp = read("input.txt")
ANSWER = sum(get_part_numbers(inp))
print("Part 1 =", ANSWER)
assert ANSWER == 540131  # check with accepted answer

########
# PART 2

Gear = list[int]


def find_potential_gears(coord: Coord, val: int, schematic: Schematic) -> list[Coord]:
    """ Check if the specified item is a part number """

    (max_x, max_y), symbols, _ = schematic
    x, y = coord
    val_len = len(str(val))
    potential_gears = []

    for dy in [-1, 0, 1]:
        for dx in range(-1, val_len + 1):
            if dy == 0 and 0 <= dx < val_len:
                continue

            nx, ny = x + dx, y + dy
            if (0 <= nx <= max_x) and (0 <= ny <= max_y):
                if symbols.get((nx, ny), None) == '*':
                    potential_gears.append((nx, ny))

    return potential_gears


def get_gear_ratio(gear: Gear) -> int:
    """ Calculate the gear ratio """
    return reduce(lambda x, y: x * y, gear)


def get_gear_ratios(schematic: Schematic) -> list[Gear]:
    """ Get all the gears in the schematic """
    _, _, numbers = schematic
    potential_gears = {}

    for coord, val in numbers.items():
        for potential_gear_pos in find_potential_gears(coord, val, schematic):
            parts = potential_gears.setdefault(potential_gear_pos, [])
            parts.append(val)

    return [get_gear_ratio(gear) for gear in potential_gears.values() if len(gear) == 2]


assert sum(get_gear_ratios(ex1)) == 467835

ANSWER = sum(get_gear_ratios(inp))
print("Part 2 =", ANSWER)
assert ANSWER == 86879020  # check with accepted answer

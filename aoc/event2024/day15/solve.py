""" Advent of code 2024 - day 15 """

from itertools import count
from pathlib import Path

########
# PART 1

type Coord = tuple[int, int]
type Warehouse = dict[Coord, str]
DIRECTIONS = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1)
}


def read(filename: str) -> tuple[Warehouse, Coord, str]:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        warehouse = {}
        robot = None
        for y in count():
            line = file.readline().strip()

            if not line:
                break

            for x, ch in enumerate(line):
                if ch == '@':
                    robot = (x, y)

                if ch != '.':
                    warehouse[(x, y)] = ch

        commands = "".join(line.strip() for line in file)

        return warehouse, robot, commands


def run(warehouse: Warehouse, robot: Coord, commands: list[str]) -> Coord:
    """ Run the command list """

    def move(warehouse: Warehouse, pos: Coord, velocity: Coord) -> tuple[bool, Coord]:
        """ move a piece """
        x, y = pos
        dx, dy = velocity
        item = warehouse.get((x, y), None)

        if item == '#':
            return False, pos

        if item in ('O', '@'):
            nx, ny = x + dx, y + dy

            if warehouse.get((nx, ny), None) is None or move(warehouse, (nx, ny), velocity)[0]:
                del warehouse[x, y]
                warehouse[nx, ny] = item

                return True, (nx, ny)

        return False, pos

    warehouse = dict(warehouse)
    for command in commands:
        velocity = DIRECTIONS[command]

        _, robot = move(warehouse, robot, velocity)

    return warehouse, robot, commands


def print_map(warehouse: Warehouse, robot: Coord, width, height):
    """ print the map """
    for y in range(height):
        for x in range(width):
            print(warehouse.get((x, y), '.'), end="")
        print()
    print()


def calc_gps(warehouse: Warehouse) -> int:
    """ Calculate the GPS for all the boxes """
    return sum(x + y * 100 for (x, y), ch in warehouse.items() if ch in ('O', '['))


ex1 = read("example1.txt")
assert calc_gps(run(*ex1)[0]) == 10092

ex2 = read("example2.txt")
assert calc_gps(run(*ex2)[0]) == 2028

inp = read("input.txt")
ANSWER = calc_gps(run(*inp)[0])
print("Part 1 =", ANSWER)
assert ANSWER == 1451928  # check with accepted answer

########
# PART 2


def widen(warehouse: Warehouse, robot: Coord, commands: list[str]) -> tuple[Warehouse, Coord, str]:
    """ Widen the warehouse """
    wider = {}
    for (x, y), ch in warehouse.items():
        if ch in ('O', '#'):
            wider[(x * 2, y)] = ch if ch != 'O' else '['
            wider[(x * 2 + 1, y)] = ch if ch != 'O' else ']'
        elif ch == '@':
            wider[(x * 2, y)] = ch

    x, y = robot

    return wider, (x * 2, y), commands


def run_wider(warehouse: Warehouse, robot: Coord, commands: list[str]) -> Coord:
    """ Run the command list """

    def can_move(warehouse: Warehouse, pos: Coord, velocity: Coord) -> tuple[bool, Coord]:
        """ check if a piece can move """
        x, y = pos
        _, dy = velocity

        item = warehouse.get((x, y), None)
        if item == '#':
            return False

        if item == '[':
            return (can_move(warehouse, (x, y + dy), velocity)
                    and can_move(warehouse, (x + 1, y + dy), velocity))

        if item == ']':
            return (can_move(warehouse, (x, y + dy), velocity)
                    and can_move(warehouse, (x - 1, y + dy), velocity))

        if item == '@':
            return can_move(warehouse, (x, y + dy), velocity)

        return True

    def just_move(warehouse: Warehouse, pos: Coord, velocity: Coord):
        """ just move, assuming check is made before """
        x, y = pos
        _, dy = velocity
        ny = y + dy

        item = warehouse.get((x, y), None)

        if item == '[':
            just_move(warehouse, (x, ny), velocity)
            just_move(warehouse, (x + 1, ny), velocity)

            del warehouse[x, y]
            del warehouse[x + 1, y]

            warehouse[x, ny] = '['
            warehouse[x + 1, ny] = ']'

        elif item == ']':
            just_move(warehouse, (x, y + dy), velocity)
            just_move(warehouse, (x - 1, y + dy), velocity)

            del warehouse[x, y]
            del warehouse[x - 1, y]

            warehouse[x, ny] = ']'
            warehouse[x - 1, ny] = '['
        elif item == '@':
            just_move(warehouse, (x, y + dy), velocity)

            del warehouse[x, y]
            warehouse[x, ny] = item

        return x, ny

    def move(warehouse: Warehouse, pos: Coord, velocity: Coord) -> tuple[bool, Coord]:
        """ move a piece """
        x, y = pos
        dx, dy = velocity
        item = warehouse.get((x, y), None)

        if item == '#':
            return False, pos

        if item in ('[', ']', '@'):
            if dx != 0:
                nx, ny = x + dx, y + dy

                # horizontally, nothing has changed
                if warehouse.get((nx, ny), None) is None or move(warehouse, (nx, ny), velocity)[0]:
                    del warehouse[x, y]
                    warehouse[nx, ny] = item

                    return True, (nx, ny)
            else:
                # vertically, must check first and move boxes as a whole
                if can_move(warehouse, pos, velocity):
                    return True, just_move(warehouse, pos, velocity)

        return False, pos

    warehouse = dict(warehouse)
    for command in commands:
        velocity = DIRECTIONS[command]

        robot = move(warehouse, robot, velocity)[1]

    return warehouse, robot, commands


# ex3 = read("example3.txt")
# ex3_w = widen(*ex3)
# print_map(*ex3_w[0:2], 14, 7)
# print_map(*run_wider(*ex3_w)[0:2], 14, 7)

assert calc_gps(run_wider(*widen(*ex1))[0]) == 9021

ANSWER = calc_gps(run_wider(*widen(*inp))[0])
print("Part 2 =", ANSWER)
assert ANSWER == 1462788  # check with accepted answer

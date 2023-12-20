""" Advent of code 2023 - day 10 """
from enum import Enum
import math
from pathlib import Path
from typing import Self

########
# PART 1

type Coord = tuple[int, int]
type Field = tuple[Coord, dict[Coord, int]]


class Connection(Enum):
    """ Enum for connections """
    NORTH = 1 << 0
    EAST = 1 << 1
    SOUTH = 1 << 2
    WEST = 1 << 3

    @property
    def oposite(self) -> Self:
        """ returns the oposite side """
        if self == Connection.NORTH:
            return Connection.SOUTH
        if self == Connection.SOUTH:
            return Connection.NORTH
        if self == Connection.EAST:
            return Connection.WEST
        if self == Connection.WEST:
            return Connection.EAST

        raise RuntimeError("Unexpected")

    def is_connected_from(self, val: int) -> bool:
        """ Returns true if it is connected from this direction """
        return val & self.value == self.value

    @classmethod
    def get_moves(cls, val: int) -> list[Coord]:
        """ Return the possible moves """
        moves = []

        if Connection.NORTH.is_connected_from(val):
            moves.append((0, -1))
        if Connection.SOUTH.is_connected_from(val):
            moves.append((0, 1))
        if Connection.EAST.is_connected_from(val):
            moves.append((1, 0))
        if Connection.WEST.is_connected_from(val):
            moves.append((-1, 0))

        return moves

    @classmethod
    def from_char(cls, ch: str) -> int:
        """ Get the connection value for the specified char """

        # north
        val = Connection.NORTH.value if ch in ['|', 'L', 'J'] else 0

        # east
        val |= Connection.EAST.value if ch in ['-', 'L', 'F'] else 0

        # south
        val |= Connection.SOUTH.value if ch in ['|', '7', 'F'] else 0

        # east
        val |= Connection.WEST.value if ch in ['-', 'J', '7'] else 0

        return val


def read(filename: str) -> tuple[Field, Coord]:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        field_map = {}
        start_x, start_y = None, None
        max_x = 0
        max_y = 0

        for y, line in enumerate(file):
            max_y = max(y, max_y)
            for x, val in enumerate(line.strip()):
                max_x = max(x, max_x)

                if val in ['|', '-', 'L', 'J', '7', 'F']:
                    field_map[x, y] = Connection.from_char(val)
                elif val == 'S':
                    start_x, start_y = x, y

        # figure out the pipe for start
        val = 0

        possibilities = [(Connection.NORTH, (0, 1)),
                         (Connection.EAST, (-1, 0)),
                         (Connection.SOUTH, (0, -1)),
                         (Connection.WEST, (1, 0))]

        for connection, (dx, dy) in possibilities:
            if connection.is_connected_from(field_map.get((start_x + dx, start_y + dy), 0)):
                val |= connection.oposite.value
        field_map[start_x, start_y] = val

        return ((max_x + 1, max_y + 1), field_map), (start_x, start_y)


def draw_field(field: Field, start: Coord):
    """
    Draws the field with the box chars:
    ┌─┐
    │ │
    └─┘
    """
    (width, height), field_map = field
    chars = {Connection.NORTH.value + Connection.SOUTH.value: '│',
             Connection.EAST.value + Connection.WEST.value: '─',
             Connection.NORTH.value + Connection.EAST.value: '└',
             Connection.NORTH.value + Connection.WEST.value: '┘',
             Connection.EAST.value + Connection.SOUTH.value: '┌',
             Connection.WEST.value + Connection.SOUTH.value: '┐'}

    for y in range(height):
        for x in range(width):
            if (x, y) == start:
                print('\033[0;42m', end="")
            print(chars.get(field_map.get((x, y), '0'), '.'), end="")
            if (x, y) == start:
                print('\033[0m', end="")

        print()


def find_loop(field: Field, start: Coord) -> set[Coord]:
    """ Find the loop starting at the specified position """
    done = set()
    todo = [start]

    _, field_map = field

    while todo:
        x, y = todo.pop()

        if (x, y) not in done:
            done.add((x, y))

            moves = Connection.get_moves(field_map[x, y])
            for dx, dy in moves:
                nx, ny = x + dx, y + dy

                if (nx, ny) not in done:
                    todo.append((nx, ny))
    return done


def find_max_distance(field: Field, start: Coord) -> int:
    """ Return the maximum distance in the loop """

    return math.ceil(len(find_loop(field, start)) / 2)


ex1 = read("example1.txt")
assert find_max_distance(*ex1) == 4

ex2 = read("example2.txt")
assert find_max_distance(*ex2) == 4

ex3 = read("example3.txt")
assert find_max_distance(*ex3) == 8

ex4 = read("example4.txt")
assert find_max_distance(*ex4) == 8

inp = read("input.txt")
ANSWER = find_max_distance(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 6956  # check with accepted answer

########
# PART 2


def find_loop_area(field: Field, loop: set[Coord]) -> int:
    """ Find the area inside the loop """
    (width, height), field_map = field

    horizontal_area = set()
    for y in range(height):
        inside_x_north = False
        inside_x_south = False

        for x in range(width):
            val = field_map.get((x, y), 0)
            if (x, y) in loop:
                if Connection.NORTH.is_connected_from(val):
                    inside_x_north = not inside_x_north
                if Connection.SOUTH.is_connected_from(val):
                    inside_x_south = not inside_x_south
            elif inside_x_north and inside_x_south:
                horizontal_area.add((x, y))

    area = 0
    for x in range(width):
        inside_x_east = False
        inside_x_west = False
        for y in range(height):
            val = field_map.get((x, y), 0)
            if (x, y) in loop:
                if Connection.EAST.is_connected_from(val):
                    inside_x_east = not inside_x_east
                if Connection.WEST.is_connected_from(val):
                    inside_x_west = not inside_x_west
            elif inside_x_east and inside_x_west and (x, y) in horizontal_area:
                area += 1

    return area


ex5 = read("example5.txt")
assert find_loop_area(ex5[0], find_loop(*ex5)) == 4

ex6 = read("example6.txt")
assert find_loop_area(ex6[0], find_loop(*ex6)) == 10

inp = read("input.txt")
ANSWER = find_loop_area(inp[0], find_loop(*inp))
print("Part 2 =", ANSWER)
assert ANSWER == 455  # check with accepted answer

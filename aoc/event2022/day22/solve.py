"""
Advent of code 2022 - day 22
Must refactor this to calculate instead of hardcoding the cubemap rotations.
"""
from pathlib import Path
from collections import defaultdict
from typing import TypeAlias
from operator import mul
import re

########
# PART 1

# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
DIRECTIONS=[(1, 0), (0, 1), (-1, 0), (0, -1)]

Position: TypeAlias = tuple[int, int]
Board: TypeAlias = tuple[Position, dict[Position: tuple[str, int, int]]]

def read(filename: str) -> tuple[Board, str]:
    """ Read the board and instructions """
    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        board = {}

        pos_y = 1
        min_y_for_x = defaultdict(lambda : 1e10)
        max_y_for_x = defaultdict(int)
        starting_x = 0
        while True:
            line = file.readline().strip("\r\n")

            if len(line) == 0:
                break

            min_x = 1e10
            max_x = 0
            for pos_x, char in enumerate(line, start = 1):
                if char != ' ':
                    min_x = min(min_x, pos_x)
                    max_x = max(max_x, pos_x)
                    min_y_for_x[pos_x] = min(min_y_for_x[pos_x], pos_y)
                    max_y_for_x[pos_x] = max(max_y_for_x[pos_x], pos_y)

                    board[(pos_x, pos_y)] = (char, None, None)

            if pos_y == 1:
                starting_x = min_x

            board[(min_x, pos_y)] = (board[(min_x, pos_y)][0], max_x, None)
            board[(max_x, pos_y)] = (board[(max_x, pos_y)][0], min_x, None)

            pos_y += 1

        # find vertical wraps
        for pos_x, min_y in min_y_for_x.items():
            max_y = max_y_for_x[pos_x]

            board[(pos_x, min_y)] = board[(pos_x, min_y)][:2] + (max_y,)
            board[(pos_x, max_y)] = board[(pos_x, max_y)][:2] + (min_y,)

        instructions = file.readline().strip()

        return ((starting_x, 1), board), instructions


def follow_instructions(board: Board, instructions: str):
    """ Return the position after following instructions """
    direction = 0

    (start_pos_x, pos_y), board_map = board

    pos_x = start_pos_x
    for match in re.finditer(r"\d+|[LR]", instructions):
        command = match.group()

        if command == 'L':
            direction = (direction - 1) % len(DIRECTIONS)
        elif command == 'R':
            direction = (direction + 1) % len(DIRECTIONS)
        else:
            # advance
            forward = int(command)
            d_x, d_y = DIRECTIONS[direction]

            for _ in range(forward):
                new_x, new_y = pos_x + d_x, pos_y + d_y

                if (new_x, new_y) not in board_map:
                    _, wrap_x, wrap_y = board_map[(pos_x, pos_y)]

                    if d_x != 0:
                        new_x = wrap_x

                    if d_y != 0:
                        new_y = wrap_y

                char, _, _ = board_map[(new_x, new_y)]

                if char == '.':
                    pos_x, pos_y = new_x, new_y

    return pos_x, pos_y, direction


ex1 = read('example1.txt')
assert sum(map(mul, follow_instructions(*ex1), [4, 1000, 1])) == 6032

inp = read('input.txt')
ANSWER = sum(map(mul, follow_instructions(*inp), [4, 1000, 1]))
print("Part 1 =", ANSWER)
assert ANSWER == 11464 # check with accepted answer

########
# PART 2

Cubemap: TypeAlias = tuple[int, Position, dict[Position: tuple[str, int]], list[Position]]

def remap_board(board: Board, region_size = 50) -> Cubemap:
    """ Redefine the board as a cube """
    (start_pos_x, start_pos_y), board_map = board

    piece_map = {}
    region_starts = [None] * 6
    for (pos_x, pos_y), (piece, _, _) in board_map.items():
        region = 0

        zone_x = (pos_x - start_pos_x) // region_size
        zone_y = (pos_y - start_pos_y) // region_size

        if zone_x == zone_y == 0:
            region = 1
        elif zone_y <= 2:
            if zone_x == 0:
                region = zone_y + 1
            elif zone_x == -1 and zone_y <= 2:
                region = 5
            elif zone_x == 1 and zone_y <= 2:
                region = 6
            else:
                region = 4
        else:
            region = 4

        piece_map[(pos_x, pos_y)] = piece, region

        if (pos_x - 1) % region_size == (pos_y - 1) % region_size == 0:
            region_starts[region - 1] = (pos_x, pos_y)

    return region_size, (start_pos_x, start_pos_y), piece_map, region_starts


def draw(cubemap: Cubemap, pawn = (-1, -1, -1)):
    """ draw the cubemap """
    region_size, _, piece_map, _ = cubemap

    print("   ", end="")
    for pos_x in range(1, region_size * 4 + 1):
        print(f"{hex(pos_x)[2:]:2}", end="")
    print()
    for pos_y in range(1, region_size * 4 + 1):
        print(f"{pos_y:2} ", end="")
        for pos_x in range(1, region_size * 4):
            if (pos_x, pos_y) == pawn[:2]:
                print(f"\033[41;1m{['>', 'v', '<', '^'][pawn[2]]}\033[0m", end=" ")
            elif (pos_x, pos_y) not in piece_map:
                print(' ', end=" ")
            else:
                print(f"\033[{31 + piece_map[(pos_x, pos_y)][1]};1m{piece_map[(pos_x, pos_y)][0]}\033[0m", end=" ")
        print()
    print(f"-------------\033[{region_size * 4 + 2}A")


# Facing is 0 for right (>), 1 for down (v), 2 for left (<), and 3 for up (^)
# kill me
def rotate(angle):
    """ Return the function for the new coordinates on rotate """
    if angle == 90:
        return lambda x, y, d : (y, x, (d + 1) % len(DIRECTIONS))
    if angle == -90:
        return lambda x, y, d : (y, x, (d - 1) % len(DIRECTIONS))
    if angle == 180:
        return lambda x, y, d : (x, - y - 1, (d + 2) % len(DIRECTIONS))
    if angle == -180:
        return lambda x, y, d : (x, - y - 1, (d - 2) % len(DIRECTIONS))
    if angle == 0:
        return lambda x, y, d : (x, - y - 1, d)

    raise RuntimeError("Not supported")


FROM_TO = {
    # 4-1
    (4, 2): (1, rotate(-90)),
    (1, 3): (4, rotate(90)),
    # 2-5
    (2, 2): (5, rotate(-90)),
    (5, 3): (2, rotate(90)),
    # 2-6
    (2, 0): (6, rotate(-90)),
    (6, 1): (2, rotate(90)),
    # 4-3
    (4, 0): (3, rotate(-90)),
    (3, 1): (4, rotate(90)),
    # 5-1
    (5, 2): (1, rotate(-180)),
    (1, 2): (5, rotate(180)),
    # 6-3
    (6, 0): (3, rotate(-180)),
    (3, 0): (6, rotate(180)),
    # 4-6
    (4, 1): (6, rotate(0)),
    (6, 3): (4, rotate(0)),
}

def follow_instructions_p2(cubemap: Cubemap, instructions: str):
    """ Return the position after following instructions """
    region_size, (start_pos_x, pos_y), piece_map, region_starts = cubemap
    direction = 0

    pos_x = start_pos_x
    for match in re.finditer(r"\d+|[LR]", instructions):
        command = match.group()

        if command == 'L':
            direction = (direction - 1) % len(DIRECTIONS)
        elif command == 'R':
            direction = (direction + 1) % len(DIRECTIONS)
        else:
            # advance
            forward = int(command)

            for _ in range(forward):
                d_x, d_y = DIRECTIONS[direction]
                new_x, new_y, new_direction = pos_x + d_x, pos_y + d_y, direction

                if (new_x, new_y) not in piece_map:
                    # warp
                    region = piece_map[(pos_x, pos_y)][1]

                    new_region, func = FROM_TO[(region, direction)]

                    region_start_x, region_start_y = region_starts[region - 1]
                    new_x, new_y = pos_x - region_start_x, pos_y - region_start_y
                    new_x, new_y, new_direction = func(new_x, new_y, direction)
                    region_start_x, region_start_y = region_starts[new_region - 1]
                    new_x = region_start_x + (new_x % region_size)
                    new_y = region_start_y + (new_y % region_size)
                    new_direction %= 4

                char, _ = piece_map[(new_x, new_y)]

                if char == '.':
                    pos_x, pos_y = new_x, new_y
                    direction = new_direction

    return pos_x, pos_y, direction


#ex2 = read("example2.txt")
#follow_instructions_p2(remap_board(ex2[0], 5), ex2[1])

#print(sum(map(lambda x, y : x * y, follow_instructions_p2(remap_board(ex1[0], 4), ex1[1]), [4, 1000, 1])))

ANSWER = sum(map(mul, follow_instructions_p2(remap_board(inp[0], 50), inp[1]), [4, 1000, 1]))
print("Part 2 =", ANSWER)
assert ANSWER == 197122 # check with accepted answer

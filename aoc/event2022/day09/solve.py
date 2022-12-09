""" Advent of code 2022 - day 09 """
from pathlib import Path

########
# PART 1

def read(filename):
    """ Reads the instructions """
    instructions = []
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        for line in file:
            direction_key, length = line.strip().split(' ')

            if direction_key == 'R':
                direction = (1, 0)
            elif direction_key == 'L':
                direction = (-1, 0)
            elif direction_key == 'U':
                direction = (0, -1)
            elif direction_key == 'D':
                direction = (0, 1)

            instructions.append((direction, int(length)))

    return instructions


def run(instructions):
    """ run the instructions and calculate the visited places by the tail """
    head_x, head_y = 0, 0
    tail_x, tail_y = 0, 0
    visited = {(0, 0)}

    for direction, length in instructions:
        for _ in range(length):
            head_x += direction[0]
            head_y += direction[1]

            d_x = head_x - tail_x
            d_y = head_y - tail_y

            if abs(d_x) > 1 or abs(d_y) > 1:
                tail_x += (d_x // abs(d_x)) if d_x != 0 else 0
                tail_y += (d_y // abs(d_y)) if d_y != 0 else 0

            visited.add((tail_x, tail_y))

    return visited


ex1 = read("example1.txt")
assert len(run(ex1)) == 13

inp = read("input.txt")
ANSWER = len(run(inp))
print("Part 1 =", ANSWER)
assert ANSWER == 5735 # check with accepted answer

########
# PART 2

def run_p2(instructions, rope_length = 10):
    """ run on a rope with rope_length and return the visited places by the tail """
    rope = [(0,0) for _ in range(rope_length)]
    visited = {(0, 0)}

    for direction, length in instructions:
        for _ in range(length):
            rope[0] = (rope[0][0] + direction[0], rope[0][1] + direction[1])

            for idx in range(1, len(rope)):
                last_knot_x, last_knot_y = rope[idx - 1]
                cur_knot = rope[idx]

                d_x = last_knot_x - cur_knot[0]
                d_y = last_knot_y - cur_knot[1]

                if abs(d_x) > 1 or abs(d_y) > 1:
                    cur_knot = (cur_knot[0] + ((d_x // abs(d_x)) if d_x != 0 else 0),
                        cur_knot[1] + ((d_y // abs(d_y)) if d_y != 0 else 0))

                rope[idx] = cur_knot

                if idx == len(rope) - 1:
                    visited.add(cur_knot)

    return visited


ex2 = read("example2.txt")
assert len(run_p2(ex2)) == 36

ANSWER = len(run_p2(inp))
print("Part 2 =", ANSWER)
assert ANSWER == 2478 # check with accepted answer

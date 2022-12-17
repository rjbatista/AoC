""" Advent of code 2022 - day XX """
from pathlib import Path
from itertools import cycle

########
# PART 1

PLAYFIELD_WIDTH = 7
STARTING_HEIGHT = 3

def read(filename: str) -> list:
    """ Read the commands """
    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [-1 if char == '<' else 1 for char in file.readline().strip()]


def rocks_generator():
    """ Generates de rocks """
    rock1 = (4, 1, { (0, 0), (1, 0), (2, 0), (3, 0) }) # -
    rock2 = (3, 3, { (1, 0), (0, 1), (1, 1), (2, 1), (1, 2) }) # +
    rock3 = (3, 3, { (0, 0), (1, 0), (2, 0), (2, 1), (2, 2) }) # _|
    rock4 = (1, 4, { (0, 0), (0, 1), (0, 2), (0, 3) }) # |
    rock5 = (2, 2, { (0, 0), (1, 0), (0, 1), (1, 1) }) # |_|

    for rock in cycle([rock1, rock2, rock3, rock4, rock5]):
        yield rock


def draw_playfield(playfield, current_top):
    """ Draw the playfield """
    for pos_y in range(current_top, -1, -1):
        print("|", end="")
        for pos_x in range(PLAYFIELD_WIDTH):
            print(playfield.get((pos_x, pos_y), '.'), end="")
        print("|")
    print("+-------+")
    print()


def collision(pos_x, pos_y, rock, playfield):
    """ Check if a rock is colliding """
    _, _, pieces = rock

    for piece_x, piece_y in pieces:
        if ((pos_x + piece_x), (pos_y + piece_y)) in playfield:
            return True

    return pos_y < 0

def line_value(playfield, pos_y):
    """ Return the number representation for the playfield line """
    return int(''.join(['1' if (pos_x, pos_y) in playfield else '0' for pos_x in range(7)]), 2)


def simulate(commands, number_of_rocks = 2022):
    """ Run the simulation """
    rocks = rocks_generator()
    commands_generator = cycle(commands)
    pattern_start = 0
    playfield = {}
    rock_heights = {}
    current_top = 0

    for rock_no in range(number_of_rocks):
        rock = next(rocks)
        rock_width, rock_height, rock_pieces = rock

        pos_x = 2
        pos_y = current_top + STARTING_HEIGHT

        while True:
            d_x = next(commands_generator)

            if pos_x + d_x < 0 or pos_x + rock_width + d_x > PLAYFIELD_WIDTH:
                d_x = 0

            if not collision(pos_x + d_x, pos_y, rock, playfield):
                pos_x += d_x

            if not collision(pos_x, pos_y - 1, rock, playfield):
                pos_y -= 1
            else:
                break

        for (piece_x, piece_y) in rock_pieces:
            playfield[(pos_x + piece_x), (pos_y + piece_y)] = '#'

        current_top = max(current_top, pos_y + rock_height)

        rock_heights[current_top] = rock_no

        if rock_no > len(commands) and pattern_start == 0:
            pattern_start = current_top

    # extra block for part 2 - find repeating pattern and number of rocks for it
    pattern = [line_value(playfield, pattern_start + pattern_y) for pattern_y in range(100)]
    cmp_start = pattern_start + 50
    compare_pos = 0

    loop_size = None
    source_length = None
    while cmp_start < current_top:
        if pattern[compare_pos] == line_value(playfield, cmp_start + compare_pos):
            compare_pos += 1

            if compare_pos == len(pattern):
                loop_size = cmp_start - pattern_start
                source_length = rock_heights[cmp_start + loop_size] - rock_heights[cmp_start]
                break
        else:
            compare_pos = 0
            cmp_start += 1


    #draw_playfield(playfield, current_top + STARTING_HEIGHT)

    return current_top, playfield, loop_size, source_length


ex1 = read("example1.txt")
assert simulate(ex1)[0] == 3068

inp = read("input.txt")
ANSWER = simulate(inp)[0]
print("Part 1 =", ANSWER)
assert ANSWER == 3098 # check with accepted answer


########
# PART 2

def calculate_tower_height(commands, wanted = 1000000000000):
    """ Calculate the tower height for a specific number of pieces """
    # simulate for a while, get pattern_length and source_length
    loop_size, source_length = simulate(commands, 15000)[2:]

    times = (wanted - len(commands)) // source_length
    remaining = (wanted - len(commands)) % source_length

    return simulate(commands, remaining + len(commands))[0] + times * loop_size


assert calculate_tower_height(ex1) == 1514285714288

ANSWER = calculate_tower_height(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 1525364431487 # check with accepted answer

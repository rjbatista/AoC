""" Advent of code 2017 - day 19 """
from pathlib import Path

########
# PART 1

def read(filename):
    """ Read commands from a shell and interpret the output """
    diagram = {}
    start_x = 0
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        for pos_y, line in enumerate(file.readlines()):
            for pos_x, char in enumerate(line[:-1]):
                if char != ' ':
                    diagram[pos_x, pos_y] = char

                    if pos_y == 0:
                        start_x = pos_x

    return diagram, start_x


def transverse(diagram, start_x):
    """ Transverse the diagram """
    current_dir = (0, 1)
    cur_x, cur_y = start_x, 0
    inv = []
    steps = 0
    while True:
        cur_x += current_dir[0]
        cur_y += current_dir[1]

        steps += 1

        if (cur_x, cur_y) not in diagram:
            break

        char = diagram[cur_x, cur_y]
        if char == '+':
            # change direction
            for d_x, d_y in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                if (not (d_x == -current_dir[0] and d_y == -current_dir[1])
                 and (cur_x + d_x, cur_y + d_y) in diagram):
                    # don't turn back
                    current_dir = (d_x, d_y)
                    break

        elif char.isalpha():
            inv.append(char)

    return ''.join(inv), steps


ex1 = read("example1.txt")
assert transverse(*ex1) == ('ABCDEF', 38)

inp = read("input.txt")
answer = transverse(*inp)
print("Part 1 =", answer[0])
assert answer[0] == 'YOHREPXWN' # check with accepted answer

########
# PART 2

print("Part 2 =", answer[1])
assert answer[1] == 16734 # check with accepted answer

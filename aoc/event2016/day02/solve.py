########
# PART 1

def read_input():
    with open("event2016/day02/input.txt") as f:
        ret = []
        for line in f:
            ret += [line[:-1] if line.endswith("\n") else line]

        return ret


digits = [
    [ '1', '2', '3' ],
    [ '4', '5', '6' ],
    [ '7', '8', '9' ]
]

def calc_digit(digitCode, pos):
    for move in digitCode:
        if move == 'U':
            pos[1] = pos[1] - 1 if pos[1] > -1 else pos[1]
        elif move == 'D':
            pos[1] = pos[1] + 1 if pos[1] < 1 else pos[1]
        elif move == 'L':
            pos[0] = pos[0] - 1 if pos[0] > -1 else pos[0]
        elif move == 'R':
            pos[0] = pos[0] + 1 if pos[0] < 1 else pos[0]
        else:
            raise ValueError(move)

    return digits[pos[1] + 1][pos[0] + 1]


def p1_solve_for(input, pos):
    ret = []
    for digit in input:
        ret += [calc_digit(digit, pos)]

    return ret


assert ''.join(p1_solve_for(['ULL', 'RRDDD', 'LURDL', 'UUUUD'], [0, 0])) == "1985"

puzzle_input = read_input()
answer = ''.join(p1_solve_for(puzzle_input, [0, 0]))
print("Part 1 =", answer)
assert answer == "84452" # check with accepted answer


########
# PART 2

digits_2 = [
    [ None, None, '1', None, None ],
    [ None, '2', '3', '4', None ],
    [ '5', '6', '7', '8', '9' ],
    [ None, 'A', 'B', 'C', None ],
    [ None, None, 'D', None, None ],
]


def is_valid_pos(x, y):
    if (y >= 0) and (y < len(digits_2)):
        ly = digits_2[y]
        if (x >= 0) and (x < len(ly)):
            return ly[x] is not None

    return False


def calc_digit_2(digitCode, pos):
    for move in digitCode:
        if move == 'U':
            if (is_valid_pos(pos[0], pos[1] - 1)):
                pos[1] = pos[1] - 1
        elif move == 'D':
            if (is_valid_pos(pos[0], pos[1] + 1)):
                pos[1] = pos[1] + 1
        elif move == 'L':
            if (is_valid_pos(pos[0] - 1, pos[1])):
                pos[0] = pos[0] - 1
        elif move == 'R':
            if (is_valid_pos(pos[0] + 1, pos[1])):
                pos[0] = pos[0] + 1
        else:
            raise ValueError(move)

    return digits_2[pos[1]][pos[0]]


def p2_solve_for(input, pos):
    ret = []
    for digit in input:
        ret += [calc_digit_2(digit, pos)]

    return ret


assert ''.join(p2_solve_for(['ULL', 'RRDDD', 'LURDL', 'UUUUD'], [0, 2])) == "5DB3"

answer = ''.join(p2_solve_for(puzzle_input, [0, 2]))
print("Part 2 =", answer)
assert answer == "D65C3" # check with accepted answer

""" Advent of code 2017 - day 16 """
from pathlib import Path
import re
from itertools import count

########
# PART 1

def create_program(length: int):
    """ creates the default program for the specified length """
    prog = []
    for i in range(length):
        prog.append(chr(ord('a') + i))

    return ''.join(prog)


def read(filename):
    """ read moves """
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        return file.readline()[:-1].split(',')


def spin(lst: list, idx: int) -> list:
    """
    Makes X programs move from the end to the front,
    but maintain their order otherwise.
    (For example, s3 on abcde produces cdeab).
    """
    return lst[-idx:] + lst[:-idx]


def exchange(lst: list, idx1, idx2: int) -> list:
    """ Exchange, written xA/B, makes the programs at positions A and B swap places. """
    temp = lst[idx1]
    lst[idx1] = lst[idx2]
    lst[idx2] = temp

    return lst


def partner(lst: list, prog1, prog2: int) -> list:
    """ Partner, written pA/B, makes the programs named A and B swap places. """
    idx1 = lst.index(prog1)
    idx2 = lst.index(prog2)

    temp = lst[idx1]
    lst[idx1] = lst[idx2]
    lst[idx2] = temp

    return lst


def run_moves(lst: list, moves):
    """ Runs the moves and returns the resulting string """
    pattern = re.compile(r'([sxp])(?:(\d+)[/](\d+)|(\d+)|(\w)[/](\w))')

    for move in moves:
        match = pattern.match(move)

        if match.group(1) == 's':
            lst = spin(lst, int(match.group(4)))
        elif match.group(1) == 'x':
            lst = exchange(lst, int(match.group(2)), int(match.group(3)))
        elif match.group(1) == 'p':
            lst = partner(lst, match.group(5), match.group(6))

    return lst


ex1_moves = read('example1.txt')
assert ''.join(run_moves(list(create_program(5)), ex1_moves)) == 'baedc'

inp_moves = read('input.txt')
answer = ''.join(run_moves(list(create_program(16)), inp_moves))
print("Part 1 =", answer)
assert answer == 'olgejankfhbmpidc' # check with accepted answer

########
# PART 2

def find_cycle(input_str, moves):
    """ runs moves until a cycle is found """

    wanted = list(input_str)
    cur = list(input_str)
    for i in count(1):
        cur = run_moves(cur, moves)
        if cur == wanted:
            return i

    raise "Unreachable"


def run_moves_for(input_str, moves, num: int = 1000000000):
    """ Repeat the moves <num> times """

    # find a cycle?
    cycle = find_cycle(input_str, moves)

    # skip the cycles, just do the remaining times
    remaining = num % cycle

    cur = list(input_str)
    for _ in range(remaining):
        cur = run_moves(cur, moves)

    return ''.join(cur)


answer = run_moves_for(create_program(16), inp_moves)
print("Part 2 =", answer)
assert answer == 'gfabehpdojkcimnl' # check with accepted answer

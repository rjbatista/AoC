import re

########
# PART 1

class Screen:
    """ Class for screen """
    def __init__(self, w, h):
        self._w = w
        self._h = h
        self._screen = [[0 for x in range(w)] for y in range(h)]

    def print_screen(self):
        for y in range(self._h):
            for x in range(self._w):
                print(' ' if self._screen[y][x] == 0 else '#',end="")
            print()
        print()


    def rect(self, x, y):
        for cy in range(y):
            for cx in range(x):
                self._screen[cy][cx] = 1

    def rotate_column(self, col, delta):
        # tilt list 90 degrees
        rotated = list(zip(*self._screen))

        delta = delta % self._h

        # shift
        rotated[col] =  rotated[col][-delta:] + rotated[col][:-delta]

        self._screen = list(map(list, zip(*rotated)))

    def rotate_row(self, row, delta):
        # shift
        self._screen[row] =  self._screen[row][-delta:] + self._screen[row][:-delta]

    def return_lit(self):
        return sum([sum(i) for i in self._screen])


def process_line(line):
    m = re.match(r'(rect) (\d+)x(\d+)', line)

    if (m is not None):
        return m.group(1), (int(m.group(2)), int(m.group(3)))
    else:
        m = re.match(r'(rotate (?:row|column)) (?:y|x)=(\d+) by (\d+)', line)

        return m.group(1), (int(m.group(2)), int(m.group(3)))


def read_input():
    with open("event2016/day08/input.txt") as f:
        ret = []
        for line in f:
            ret += [process_line(line)]

    return ret


def p1_solve_for(screen, input):
    for instr in input:
        if (instr[0] == 'rect'):
            screen.rect(*instr[1])
        elif (instr[0] == 'rotate column'):
            screen.rotate_column(*instr[1])
        elif (instr[0] == 'rotate row'):
            screen.rotate_row(*instr[1])


    return screen.return_lit()


# example
screen = Screen(7, 3)
screen.rect(3, 2)
#screen.print_screen()
screen.rotate_column(1, 1)
#screen.print_screen()
screen.rotate_row(0, 4)
#screen.print_screen()
screen.rotate_column(1, 1)
#screen.print_screen()
assert screen.return_lit() == 6

# Part 1

screen = Screen(50, 6)

answer = p1_solve_for(screen, read_input())
print("Part 1 =", answer)
assert answer == 115 # check with accepted answer

########
# PART 2

print("Part 2 =")
# should read EFEYKFRFIJ
screen.print_screen()

import re

########
# PART 1

_debug = False

class Scrambler:
    def __init__(self, starting):
        self._str = list(starting)
        self._reverse = False

        self._instructions = [
            (re.compile(r'swap position (\d+) with position (\d+)'), self.swap_pos, lambda x : (int(x.group(1)), int(x.group(2)))),
            (re.compile(r'swap letter (\w) with letter (\w)'), self.swap_letter, lambda x : (x.group(1), x.group(2))),
            (re.compile(r'rotate (left|right) (\d+) steps?'), self.rotate, lambda x : (x.group(1), int(x.group(2)))),
            (re.compile(r'rotate based on position of letter (\w)'), self.rotate_based_on, lambda x : x.group(1)),
            (re.compile(r'reverse positions (\d+) through (\d+)'), self.reverse, lambda x : (int(x.group(1)), int(x.group(2)))),
            (re.compile(r'move position (\d+) to position (\d+)'), self.move, lambda x : (int(x.group(1)), int(x.group(2))))
        ]

    def reversed(self):
        self._reverse = True

    def swap_pos(self, x, y):
        """
        swap position X with position Y
            means that the letters at indexes X and Y (counting from 0) should be swapped.
        """
        tmp = self._str[x]
        self._str[x] = self._str[y]
        self._str[y] = tmp

    def swap_letter(self, x, y):
        """
        swap letter X with letter Y
            means that the letters X and Y should be swapped (regardless of where they appear in the string).
        """
        x_index = self._str.index(x)
        y_index = self._str.index(y)

        self.swap_pos(x_index, y_index)

    def rotate(self, direction, steps):
        """
        rotate left/right X steps
            means that the whole string should be rotated; for example, one right rotation would turn abcd into dabc.
        """
        real_steps = steps % len(self._str)
        real_steps = real_steps if direction == 'left' else -real_steps

        if self._reverse: real_steps = -real_steps

        self._str = self._str[real_steps:] + self._str[:real_steps]

    def rotate_based_on(self, x):
        """
        rotate based on position of letter X
            means that the whole string should be rotated to the right based on the index of letter X (counting from 0) as determined before this instruction does any rotations.
            Once the index is determined, rotate the string to the right one time, plus a number of times equal to that index, plus one additional time if the index was at least 4.
        """
        if self._reverse:
            x_index = self._str.index(x)

            assert len(self._str) <= 8

            # calculated inverse
            # for abcdefgh, where does each one land on a rotate_based_on
            # ex: rotate_base_on(a), lands on 1, on f lands on 4, etc.
            reverse = [1, 1, -2, 2, -1, 3, 0, -4]
            self.rotate('right', reverse[x_index])
        else:
            x_index = self._str.index(x)
            self.rotate('right', 1 + x_index + (1 if x_index >= 4 else 0))


    def reverse(self, x, y):
        """
        reverse positions X through Y
            means that the span of letters at indexes X through Y (including the letters at X and Y) should be reversed in order.
        """
        assert x <= y

        self._str = self._str[:x] + list(reversed(self._str[x:y + 1])) + self._str[y + 1:]

    def move(self, x, y):
        """
        move position X to position Y
            means that the letter which is at index X should be removed from the string, then inserted such that it ends up at index Y.
        """

        if self._reverse:
            x, y = y, x

        letter = self._str.pop(x)
        self._str.insert(y, letter)

    def run(self, line):
        if _debug: print(">>", line)

        for exp, method, args_parser in self._instructions:
            match = exp.match(line)

            if match:
                args = args_parser(match)
                method(*args)

                if _debug: print(self)
                return

        raise ValueError("unknown " + line)

    def __str__(self):
        return ''.join(self._str)



def read_input(fn):
    f = open(fn)
    code = []
    for line in f:
        code += [line if line[-1] != '\n' else line[:-1]]

    return code


test = Scrambler("abcd")
test.run("swap position 3 with position 0")
test.run("swap letter c with letter b")
assert str(test) == 'dcba'
test.run("rotate left 1 step")
assert str(test) == 'cbad'
test.run("rotate right 1 steps")
assert str(test) == 'dcba'
test.run("reverse positions 0 through 4")
assert str(test) == 'abcd'
test.run("move position 3 to position 0")
assert str(test) == 'dabc'


example_code = read_input("event2016/day21/example.txt")
example = Scrambler("abcde")
#print(example)
_debug = False
for line in example_code:
    example.run(line)

assert str(example) == "decab"


p1_code = read_input("event2016/day21/input.txt")
p1 = Scrambler("abcdefgh")

_debug = False
for line in p1_code:
    p1.run(line)

answer = str(p1)
print("Part 1 =", answer)
assert answer == "hcdefbag" # check with accepted answer

########
# PART 2

_debug = False
for line in reversed(example_code):
    example.run(line)

p2 = Scrambler("fbgdceah")
p2.reversed()
for line in reversed(p1_code):
    p2.run(line)

answer = str(p2)
print("Part 2 =", answer)
assert answer == "fbhaegdc" # check with accepted answer

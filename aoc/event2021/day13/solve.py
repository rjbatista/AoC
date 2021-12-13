import re

########
# PART 1

class Paper:
    def __init__(self, filename) -> None:
        self.points = set()
        self.width, self.height = 0, 0
        self.folds = []
        self.fill_char = '#'
        self.empty_char = '.'
        self.load(filename)


    def load(self, filename):
        with open("event2021/day13/" + filename, "r") as file:
            pattern = re.compile(r"^(\d+),(\d+)$")

            for line in file:
                if line == "\n":
                    break

                match = pattern.match(line)
                if match:
                    x, y = int(match[1]), int(match[2])

                    self.width = max(self.width, x)
                    self.height = max(self.height, y)

                    self.points.add((x, y))
                else:
                    raise RuntimeError("invalid input " + line)

            pattern = re.compile(r"^fold along (x|y)=(\d+)$")
            for line in file:
                match = pattern.match(line)
                if match:
                    self.folds.append((match[1], int(match[2])))
                else:
                    raise RuntimeError("invalid input " + line)


    def apply_folds(self):
        while self.folds:
            self.apply_next_fold()


    def apply_next_fold(self):
        axis, value = self.folds.pop(0)

        changes = []
        for x, y in self.points:
            if axis == 'x' and x > value:
                changes.append(((x, y), ((value - (x - value)), y)))
            elif axis == 'y' and y > value:
                changes.append(((x, y), (x, value - (y - value))))

        for original, new in changes:
            self.points.remove(original)
            self.points.add(new)

        if axis == 'x':
            self.width = value - 1
        elif axis == 'y':
            self.height = value - 1


    def draw_paper(self):
        for y in range(self.height + 1):
            for x in range(self.width + 1):
                print(self.fill_char if (x, y) in self.points else self.empty_char, end="")
            print()
        print()



ex1 = Paper("example1.txt")
ex1.apply_next_fold()
assert len(ex1.points) == 17
ex1.apply_next_fold()
assert len(ex1.points) == 16

inp = Paper("input.txt")
inp.apply_next_fold()
answer = len(inp.points)
print("Part 1 =", answer)
assert answer == 775 # check with accepted answer


########
# PART 2

inp.apply_folds()

answer = "REUPUPKR"
print("Part 2 = " + answer)
inp.empty_char = ' '
inp.draw_paper()

assert answer == "REUPUPKR" # check with accepted answer

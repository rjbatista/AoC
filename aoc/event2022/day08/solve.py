""" Advent of code 2022 - day 08 """
from pathlib import Path

########
# PART 1

class Tree:
    """ Tree """
    def __init__(self, height) -> None:
        self.height = height
        self._heighest_left = 0
        self._heighest_right = 0
        self._heighest_top = 0
        self._heighest_bottom = 0
        self._view_score = 0

    def set_left(self, height):
        """ Sets the max height from the direction """
        self._heighest_left = height

        return max(height, self.height)

    def set_right(self, height):
        """ Sets the max height from the direction """
        self._heighest_right = height

        return max(height, self.height)

    def set_top(self, height):
        """ Sets the max height from the direction """
        self._heighest_top = height

        return max(height, self.height)

    def set_bottom(self, height):
        """ Sets the max height from the direction """
        self._heighest_bottom = height

        return max(height, self.height)

    def is_visible(self) -> bool:
        """ Checks if the tree is visible """
        return (self.height > self._heighest_left
            or self.height > self._heighest_right
            or self.height > self._heighest_top
            or self.height > self._heighest_bottom)

    def is_visible_left(self) -> bool:
        """ Checks if the tree is visible from a specific direction """
        return self.height > self._heighest_left

    def is_visible_right(self) -> bool:
        """ Checks if the tree is visible from a specific direction """
        return self.height > self._heighest_right

    def is_visible_top(self) -> bool:
        """ Checks if the tree is visible from a specific direction """
        return self.height > self._heighest_top

    def is_visible_bottom(self) -> bool:
        """ Checks if the tree is visible from a specific direction """
        return self.height > self._heighest_bottom

    def set_view_score(self, score):
        """ Sets the view score """
        self._view_score = score

    def __repr__(self) -> str:
        return str(self.height)


def resolve_sides(grid):
    """ Resolve the heighest sides """
    size = len(grid)
    for pos_axis1 in range(size):
        # sides
        left = -1
        right = -1
        top = -1
        bottom = -1
        for pos_axis2 in range(size):
            left = grid[pos_axis1][pos_axis2].set_left(left)
            right = grid[pos_axis1][size - pos_axis2 - 1].set_right(right)
            top = grid[pos_axis2][pos_axis1].set_top(top)
            bottom = grid[size - pos_axis2 - 1][pos_axis1].set_bottom(bottom)


def read(filename):
    """ Reads the tree grid """
    grid = []
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        for line in file:
            row = []
            for height in line.strip():
                row.append(Tree(int(height)))

            grid.append(row)

    resolve_sides(grid)

    return grid


ex1 = read("example1.txt")
assert sum((1 for row in ex1 for tree in row if tree.is_visible())) == 21

inp = read("input.txt")
answer = sum((1 for row in inp for tree in row if tree.is_visible()))
print("Part 1 =", answer)
assert answer == 1805 # check with accepted answer

########
# PART 2

def check_direction(grid, pos_x, pos_y, d_x, d_y) -> int:
    size = len(grid)
    height = grid[pos_y][pos_x].height
    count = 0

    pos_x += d_x
    pos_y += d_y
    while 0 <= pos_x < size and 0 <= pos_y < size:
        count += 1
        if grid[pos_y][pos_x].height >= height:
            break

        pos_x += d_x
        pos_y += d_y

    return count


def resolve_scenic_scores(grid):
    """ Resolve the scenic scores """
    size = len(grid)
    max_score = 0
    for pos_y, row in enumerate(grid[1:-1], start=1):
        for pos_x, tree in enumerate(row[1:-1], start=1):
            score = 1
            if tree.is_visible_top():
                score *= pos_y
            else:
                score *= check_direction(grid, pos_x, pos_y, 0, -1)

            if tree.is_visible_left():
                score *= pos_x
            else:
                score *= check_direction(grid, pos_x, pos_y, -1, 0)

            if tree.is_visible_right():
                score *= size - pos_x - 1
            else:
                score *= check_direction(grid, pos_x, pos_y, 1, 0)

            if tree.is_visible_bottom():
                score *= size - pos_y - 1
            else:
                score *= check_direction(grid, pos_x, pos_y, 0, 1)

            max_score = max(max_score, score)
            tree.set_view_score(score)

    return max_score


assert resolve_scenic_scores(ex1) == 8

answer = resolve_scenic_scores(inp)
print("Part 2 =", answer)
assert answer == 444528 # check with accepted answer

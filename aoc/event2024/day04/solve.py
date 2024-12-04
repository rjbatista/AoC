""" Advent of code 2024 - day 04 """

from pathlib import Path

########
# PART 1

type Puzzle = tuple[int, int, dict[tuple[int, int], str]]

def read(filename: str) -> Puzzle:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        w = h = 0
        puzzle_map = {}
        for y, line in enumerate(file):
            h = y
            for x, ch in enumerate(line.strip()):
                puzzle_map[x, y] = ch
                w = x

        return w, h, puzzle_map


def find_word(puzzle: Puzzle, word: str, x: int, y: int, dx: int, dy: int) -> bool:
    """ find word in specified position and direction """
    w, h, puzzle_map = puzzle

    if 0 <= x <= w and 0 <= y <= h and puzzle_map[x, y] == word[0]:
        rest = word[1:]

        if rest:
            return find_word(puzzle, rest, x + dx, y + dy, dx, dy)

        return True

    return False


def find_words(puzzle: Puzzle, word: str = 'XMAS', only_diags: bool = False) -> list[tuple[int, int, int]]:
    """
    find words in puzzle, returning the top left of the square
    containing the word and diagonal direction
    """
    first, rest = word[0], word[1:]
    starts = [(x, y) for (x, y), ch in puzzle[2].items() if ch == first]

    if only_diags:
        possibilities = [(dx, dy) for dy in [-1, 1] for dx in [-1, 1]]
    else:
        possibilities = [(dx, dy) for dy in [-1, 0, 1] for dx in [-1, 0, 1] if dx != 0 or dy != 0]

    total = []
    while starts:
        x, y = starts.pop()

        for dx, dy in possibilities:
            if find_word(puzzle, rest, x + dx, y + dy, dx, dy):
                total.append((min(x, x + dx * (len(word) - 1)),
                              min(y, y + dy * (len(word) - 1)), dx * dy))

    return total


ex1 = read("example1.txt")
assert len(find_words(ex1)) == 18

inp = read("input.txt")
ANSWER = len(find_words(inp))
print("Part 1 =", ANSWER)
assert ANSWER == 2462  # check with accepted answer

########
# PART 2

def find_crosses(puzzle: Puzzle, word: str = 'MAS') -> list[tuple[int, int]]:
    """ find crosses on puzzle """
    matches = sorted(find_words(puzzle, word, only_diags = True))

    total = []
    for (x0, y0, d0), (x1, y1, d1) in zip(matches, matches[1:]):
        if x0 == x1 and y0 == y1 and d0 * d1 == -1:
            total.append((x0, y0))

    return total


assert len(find_crosses(ex1)) == 9

ANSWER = len(find_crosses(inp))
print("Part 2 =", ANSWER)
assert ANSWER == 1877  # check with accepted answer

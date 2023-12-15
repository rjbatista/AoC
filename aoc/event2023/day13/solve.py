""" Advent of code 2023 - day 13 """
from pathlib import Path

########
# PART 1

type Pattern = list[str]


def read(filename: str) -> list[Pattern]:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        all_patterns = []
        cur = []
        for line in [line.strip() for line in file]:
            if line:
                cur.append(line)
            else:
                all_patterns.append(cur)
                cur = []

        if cur:
            all_patterns.append(cur)

        return all_patterns


def compare_with_faults(s1: str, s2: str, allowed_faults: int) -> tuple[bool, int]:
    """ Compare strings, accepting with faults """

    if not s1 or not s2:
        return False, allowed_faults

    for ch1, ch2 in zip(s1, s2):
        if ch1 != ch2:
            allowed_faults -= 1
            if allowed_faults < 0:
                return False, 0

    return True, allowed_faults


def is_reflection(pattern: Pattern, max_faults: int, x: int = None, y: int = None) -> bool:
    """ Check if the specified reflection exists at the specified points """

    if x:
        x_size = len(pattern[0])
        match_len = min(x, x_size - x)
        allowed_faults = max_faults
        for line in pattern:
            match, allowed_faults = compare_with_faults(line[x - match_len:x],
                                                        line[x: x + match_len][::-1],
                                                        allowed_faults)

            if not match:
                return False

        return True

    if y:
        y_size = len(pattern)
        match_len = min(y, y_size - y)
        allowed_faults = max_faults
        for cy in range(1, match_len + 1):
            match, allowed_faults = compare_with_faults(pattern[y + cy - 1],
                                                        pattern[y - cy], allowed_faults)

            if not match:
                return False

        return True

    return False


def find_possible_reflections(pattern: Pattern, max_faults: int) -> tuple[set[int], set[int]]:
    """ Find possible reflections """

    x_size = len(pattern[0])
    y_size = len(pattern)
    x_possible = set(range(x_size))
    y_possible = set(range(y_size))
    allowed_faults_x = [max_faults] * x_size

    old_line = None
    for y, line in enumerate(pattern):
        match, _ = compare_with_faults(line, old_line, max_faults)
        if not match and y in y_possible:
            y_possible.remove(y)
        old_line = line

        old = None
        for x, ch in enumerate(line):
            match, allowed_faults_x[x] = compare_with_faults(ch, old, allowed_faults_x[x])
            if not match and x in x_possible:
                x_possible.remove(x)

            old = ch

    return x_possible, y_possible


def find_reflection(pattern: Pattern, max_faults: int = 0,
                    exceptions: list[tuple[int, int]] = None):
    """ Find reflections, ignoring the supplied exception list """

    x_possible, y_possible = find_possible_reflections(pattern, max_faults)

    if exceptions:
        x_possible = x_possible.difference([x for (x, _) in exceptions])
        y_possible = y_possible.difference([y for (_, y) in exceptions])

    all_reflections = []
    for x in x_possible:
        if is_reflection(pattern, max_faults, x):
            all_reflections.append((x, 0))

    for y in y_possible:
        if is_reflection(pattern, max_faults, None, y):
            all_reflections.append((0, y))

    if len(all_reflections) == 1:
        return all_reflections[0]

    raise ValueError(f"Wrong # of reflections {all_reflections} on {pattern}")


def summarize1(all_patterns: list[Pattern]) -> int:
    """ Summarize the notes """
    return sum(x + y * 100 for x, y in (find_reflection(pat) for pat in all_patterns))


ex1 = read("example1.txt")
assert summarize1(ex1) == 405

inp = read("input.txt")
ANSWER = summarize1(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 35210  # check with accepted answer

########
# PART 2


def summarize_with_smudge(all_patterns: list[Pattern]) -> int:
    """ Summarize the notes using the smudged pattern """
    return sum(x + y * 100
               for x, y in (find_reflection(pat, 1, [find_reflection(pat, 0)])
                            for pat in all_patterns))


assert summarize_with_smudge(ex1) == 400

ANSWER = summarize_with_smudge(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 31974  # check with accepted answer

import re
from collections import Counter

########
# PART 1

def read(filename):
    towers = {}
    with open("event2017/day07/" + filename, "r") as file:
        pattern = re.compile(r"^(\w+) \((\d+)\)(?: -> ((?:\w+(?:, )?)*))?$")

        for line in file:
            match = pattern.match(line)
            if (match):
                current = match[1]
                current_parent = towers[current][0] if current in towers else None
                weight = int(match[2])
                children = match[3].split(', ') if match[3] else None

                towers[current] = (current_parent, weight, children)

                if (children):
                    for child in children:
                        _, w, c = towers.get(child, (None, None, None))
                        towers[child] = current, w, c
            else:
                raise RuntimeError("invalid input " + line)

    return towers


def get_top(towers):
    return next((name for name, (parent, _, _) in towers.items() if parent == None))


ex1 = read("example1.txt")
assert get_top(ex1) == 'tknk'


inp = read("input.txt")
answer = get_top(inp)
print("Part 1 =", answer)
assert answer == 'eqgvf' # check with accepted answer


########
# PART 2

class WeightError(Exception):
    def __init__(self, name, correct_weight, *args: object) -> None:
        super().__init__(*args)
        self.name = name
        self.correct_weight = correct_weight

    def __str__(self) -> str:
        return "Weight problem on %s: should be %d" % (self.name, self.correct_weight)


def calc_weight(towers, tower):
    _, weight, children = towers[tower]

    if children:
        weights = {child : calc_weight(towers, child) for child in children}
        counts = Counter(weights.values())

        if len(counts) > 1:
            correct_weight = counts.most_common(1)[0][0]
            problem_child = next((child, weight) for child, weight in weights.items() if weight != correct_weight)
            diff = problem_child[1] - correct_weight

            raise WeightError(problem_child[0], towers[problem_child[0]][1] - diff)

        weight += sum(weights.values())

    return weight


def get_weight_error(towers, top_tower):
    try:
        calc_weight(towers, top_tower)
        assert "can't reach here - weights aren't balanced"
    except WeightError as w:
        return w.name, w.correct_weight


assert get_weight_error(ex1, 'tknk') == ('ugml', 60)

answer = get_weight_error(inp, answer)[1]
print("Part 2 =", answer)
assert answer == 757 # check with accepted answer

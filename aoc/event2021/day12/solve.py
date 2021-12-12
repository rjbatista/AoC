import re

########
# PART 1

def read(filename):
    with open("event2021/day12/" + filename, "r") as file:
        pattern = re.compile(r"^(\w+)-(\w+)$")

        caves = {}
        for line in file:
            match = pattern.match(line)
            if match:
                a, b = match[1], match[2] 

                caves[a] = caves.get(a, []) + [ b ]
                caves[b] = caves.get(b, []) + [ a ]
            else:
                raise RuntimeError("invalid input " + line)
    
    return caves


def find_paths(caves, path = ["start"]):
    current_cave = path[-1]

    if current_cave == "end":
        return [ path ]

    possibilites = caves[current_cave]
    completed_paths = []

    for possibility in possibilites:
        if not possibility.islower() or possibility not in path:
            completed_paths += find_paths(caves, path + [ possibility ])
    
    return completed_paths


ex1 = read("example1.txt")
assert len(find_paths(ex1)) == 10
ex2 = read("example2.txt")
assert len(find_paths(ex2)) == 19
ex3 = read("example3.txt")
assert len(find_paths(ex3)) == 226


inp = read("input.txt")
answer = len(find_paths(inp))
print("Part 1 =", answer)
assert answer == 4970 # check with accepted answer


########
# PART 2

def find_paths_p2(caves, path = (["start"], False)):
    current_cave = path[0][-1]
    visited_small = path[1]

    if current_cave == "end":
        return [ path ]

    possibilites = caves[current_cave]
    completed_paths = []

    for possibility in possibilites:
        count = sum([1 for p in path[0] if p == possibility]) if possibility.islower() else 0

        if possibility != "start" and count <= (0 if visited_small else 1):
            completed_paths += find_paths_p2(caves, (path[0] + [ possibility ], visited_small | (count == 1)))
    
    return completed_paths


assert len(find_paths_p2(ex1)) == 36
assert len(find_paths_p2(ex2)) == 103
assert len(find_paths_p2(ex3)) == 3509


answer = len(find_paths_p2(inp))
print("Part 2 =", answer)
assert answer == 137948 # check with accepted answer

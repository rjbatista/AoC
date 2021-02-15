import re
from itertools import permutations


########
# PART 1

def read_graph(fn):
    with open('event2015/day09/' + fn) as f:
        graph = {}

        for line in f:
            #AlphaCentauri to Snowdin = 66
            m = re.search(r"(\w+) to (\w+) = (\d+)", line)

            city1 = m.group(1)
            city2 = m.group(2)
            distance = int(m.group(3))

            graph[city1] = [(city2,distance)] + (graph[city1] if (city1 in graph) else [])
            graph[city2] = [(city1,distance)] + (graph[city2] if (city2 in graph) else [])

    return graph


def all_distances(graph):
    allDist = set()
    for path in permutations(graph):
        current = None
        total = 0
        for p in path:
            if current: total += next(dist for (city,dist) in graph[current] if city == p)

            current = p

            #print("%s -> " % p, end="")

        #print("= %d" % total)
        allDist.add(total)

    return allDist


assert min(all_distances(read_graph("example.txt"))) == 605

all_distances = all_distances(read_graph("input.txt"))

answer = min(all_distances)
print("Part 1 =", answer)
assert answer == 141 # check with accepted answer


########
# PART 2

answer = max(all_distances)
print("Part 2 =", answer)
assert answer == 736 # check with accepted answer

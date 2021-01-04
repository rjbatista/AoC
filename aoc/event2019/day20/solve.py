import heapq

########
# PART 1

def get_donut(fn):
    with open("event2019/day20/" + fn, "r") as f:
        lines = [line[:-1] for line in f.readlines()]

        width = len(lines[0]) - 4
        height = len(lines) - 4
        
        portals = {}
        graph = {}
        for y in range(height):
            for x in range(width):
                if (lines[2 + y][2 + x] == '.'):
                    # check down and front for path
                    down = lines[2 + y + 1][2 + x]
                    if down == '.':
                        graph.setdefault((x, y), []).append((x, y + 1, 0))
                        graph.setdefault((x, y + 1), []).append((x, y, 0))
                    elif down.isalpha():
                        # portal
                        portals.setdefault(down + lines[2 + y + 2][2 + x], []).append((x, y))
                        pass

                    front = lines[2 + y][2 + x + 1]
                    if front == '.':
                        graph.setdefault((x, y), []).append((x + 1, y, 0))
                        graph.setdefault((x + 1, y), []).append((x, y, 0))
                    elif front.isalpha():
                        # portal
                        portals.setdefault(front + lines[2 + y][2 + x + 2], []).append((x, y))
                        pass

                    # check up and back for portals
                    up = lines[2 + y - 1][2 + x]
                    if up.isalpha():
                        portals.setdefault(lines[2 + y - 2][2 + x] + up, []).append((x, y))

                    back = lines[2 + y][2 + x - 1]
                    if back.isalpha():
                        portals.setdefault(lines[2 + y][2 + x - 2] + back, []).append((x, y))

        starting = portals.pop("AA")[0]
        ending = portals.pop("ZZ")[0]

        # join portals
        for (pos1, pos2) in portals.values():
            outer = None
            inner = None

            if pos1[0] == 0 or pos1[0] + 1 == width or pos1[1] == 0 or pos1[1] + 1 == height:
                outer, inner = pos1, pos2
            if pos2[0] == 0 or pos2[0] + 1 == width or pos2[1] == 0 or pos2[1] + 1 == height:
                assert not outer
                outer, inner = pos2, pos1

            graph[inner].append((*outer, 1))
            graph[outer].append((*inner, -1))

        return starting, ending, graph


def find_path(starting, ending, graph):
    todo = []
    heapq.heappush(todo, (1, starting, set()))
    while todo:
        steps, pos, visited = heapq.heappop(todo)
        
        possibilities = graph.get(pos)
        for x, y, _ in possibilities:
            if (x, y) == ending:
                return steps
        
            if (x, y) not in visited:
                heapq.heappush(todo, (steps + 1, (x, y), visited | {pos}))


assert find_path(*get_donut("example1.txt")) == 23
assert find_path(*get_donut("example2.txt")) == 58

answer = find_path(*get_donut("input.txt"))
print("Part 1 =", answer)
assert answer == 580 # check with accepted answer


########
# PART 2

def find_path_p2(starting, ending, graph):
    todo = []
    heapq.heappush(todo, (0, 1, starting))
    visited = {(starting[0], starting[1], 0)}
    while todo:
        level, steps, pos = heapq.heappop(todo)

        for x, y, level_diff in graph.get(pos):
            new_level = level + level_diff

            if level == 0 and (x, y) == ending:
                return steps
        
            if new_level >= 0:
                if (x, y, new_level) not in visited:
                    visited.add((x, y, new_level))
                    heapq.heappush(todo, (new_level, steps + 1, (x, y)))


assert find_path_p2(*get_donut("example1.txt")) == 26
assert find_path_p2(*get_donut("example3.txt")) == 396

answer = find_path_p2(*get_donut("input.txt"))
print("Part 2 =", answer)
assert answer == 6362 # check with accepted answer

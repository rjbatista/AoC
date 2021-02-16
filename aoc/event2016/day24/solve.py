from collections import deque
import itertools

########
# PART 1

def read_input(fn):
    f = open(fn)

    inp_map = []
    for line in f:
        inp_map += [line.strip()]

    f.close()

    return inp_map


def find_all_in_map(inp_map):
    return [(inp_map[y][x], x, y)
            for y in range(len(inp_map))
            for x in range(len(inp_map[y]))
            if inp_map[y][x] in '0123456789']


def print_map(inp_map):
    for y in range(len(inp_map)):
        print(inp_map[y])


def find_shortest_path_bfs(inp_map, start, end):
    queue = deque([])

    starting_node = start + (0,)
    queue.append(starting_node)

    visited = []
    while queue:
        x, y, cost = queue.popleft()

        if (x, y) == end:
            return cost

        for dx, dy in ((-1, 0), (1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in visited:
                if inp_map[y + dy][x + dx] != '#':
                    queue.append((x + dx, y + dy, cost + 1))
                    visited += [(x + dx, y + dy)]


def solve_for(inp_map, ret):
    places = find_all_in_map(inp_map)

    # find distances
    #print_map(inp_map)
    perms = itertools.permutations(places, 2)
    all_dists = {}
    for ((p1, x1, y1), (p2, x2, y2)) in perms:
        dist = find_shortest_path_bfs(inp_map, (x1, y1), (x2, y2))
        all_dists[p1, p2] = dist

    best_dist = 99999999999
    other_places = [p for p, _, _ in places if p != '0']

    for path in itertools.permutations(other_places, len(other_places)):
        if ret:
            path += ('0',)

        dist = 0
        pos = '0'
        for move in path:
            #print("from %s to %s = %d" % (pos, move, all_dists[pos, move]))
            dist += all_dists[pos, move]
            pos = move

        best_dist = min(best_dist, dist)

    return best_dist
    #print(all_dists)


example = read_input("event2016/day24/example.txt")
assert solve_for(example, False) == 14

p1 = read_input("event2016/day24/input.txt")

answer = solve_for(p1, False)
print("Part 1 =", answer)
assert answer == 502 # check with accepted answer

########
# PART 2

#print(solve_for(example, True))
answer = solve_for(p1, True)
print("Part 2 =", answer)
assert answer == 724 # check with accepted answer

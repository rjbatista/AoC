import re
import itertools
from collections import deque
from copy import deepcopy

########
# PART 1

_debug = False

def process_line(line):
    m = re.match(r'/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+\d+%', line)

    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
    else:
        return None


def read_input(fn):
    f = open(fn)

    ret = {}
    for line in f:
        node = process_line(line)

        if node:
            x, y, size, used, avail = node

            ret[(x, y)] = (size, used, avail)

    f.close()

    return ret


def find_all_valid_pairs(graph):
    perm = itertools.combinations(graph.items(), 2)

    valid = []
    for ((x1, y1), (_, u1, a1)), ((x2, y2), (_, u2, a2)) in perm:
        if 0 < u1 <= a2:
            valid += [((x1, y1), (x2, y2))]

        if 0 < u2 <= a1:
            valid += [((x2, y2), (x1, y1))]

    return valid


def find_valid_pairs(graph):
    perm = itertools.combinations(graph.items(), 2)

    valid = []
    for ((x1, y1), (_, u1, a1)), ((x2, y2), (_, u2, a2)) in perm:
        if abs(x1 - x2) + abs(y1 - y2) == 1:
            if 0 < u1 <= a2:
                valid += [((x1, y1), (x2, y2))]

            if 0 < u2 <= a1:
                valid += [((x2, y2), (x1, y1))]

    return valid


def find_bottom_right(graph):
    max_x = 0
    max_y = 0
    for (x, y), _ in graph.items():
        max_x = max(x, max_x)
        max_y = max(y, max_y)

    return max_x, max_y


graph = read_input("event2016/day22/input.txt")

p1 = find_all_valid_pairs(graph)
answer = len(p1)
print("Part 1 =", answer)
assert answer == 888 # check with accepted answer

########
# PART 2

#graph = read_input("example.txt")
graph = read_input("event2016/day22/input.txt")
mx, my = find_bottom_right(graph)
#print(graph[mx, my])

#print("target node-x%d-y%d" % (mx, my))


def draw_graph(graph, target, w, h):
    movable_nodes = [(x,y) for ((x,y), _) in find_all_valid_pairs(graph)]

    for y in range(h):
        for x in range(w):
            size, used, avail = graph[(x, y)]

            if (x, y) == target:
                print(" G", end=" ")
            elif used == 0:
                print(" _", end=" ")
            elif (x,y) in movable_nodes:
                print(" .", end=" ")
            else:
                print(" #", end=" ")
        print()
    print()


def find_shortest_path_bfs(graph, target):
    queue = deque([])
    visited = []

    queue.append((graph, target, 0))

    print(queue)
    while queue:
        node, cur_target, cost = queue.popleft()

        valid_pairs = find_valid_pairs(node)
        if _debug: draw_graph(node, cur_target, 3, 3)
        if _debug: print(len(valid_pairs), "pairs from here (cost %d)" % cost)

        for p1, p2 in valid_pairs:
            new_target = cur_target

            if _debug: print(">", p1, p2)

            if cur_target == p1:
                if p2 == (0, 0):
                    print("DONE in ", cost + 1)
                    return cost + 1
                else:
                    new_target = p2

            new_node = node.copy()
            size1, used1, avail1 = new_node[p1]
            size2, used2, avail2 = new_node[p2]

            new_node[p1] = (size1, 0, size1)
            new_node[p2] = (size2, used2 + used1, size2 - (used2 + used1))

            if (new_node, new_target) not in visited:
                queue.append((new_node, new_target, cost + 1))
                visited += [(new_node, new_target)]


def swap(node, p1, p2):
    graph, target = node

    size1, used1, avail1 = graph[p1]
    size2, used2, avail2 = graph[p2]

    graph[p1] = (size1, 0, size1)
    graph[p2] = (size2, used2 + used1, size2 - (used2 + used1))

    if target == p1:
        target = p2
    elif target == p2:
        target = p1

    return graph, target


def try_this(graph, target, w, h):
    count = 0
    empty = (19, 6)
    assert graph[19, 6][1] == 0

    # go to top left
    node = graph, target
    if _debug: draw_graph(node[0], node[1], mx + 1, my + 1)
    while empty[0] != 0:
        count += 1
        node = swap(node, (empty[0] - 1, empty[1]), empty)
        empty = empty[0] - 1, empty[1]
    if _debug: draw_graph(node[0], node[1], mx + 1, my + 1)
    while empty[1] != 0:
        count += 1
        node = swap(node, (empty[0], empty[1] - 1), empty)
        empty = empty[0], empty[1] - 1
    if _debug: draw_graph(node[0], node[1], mx + 1, my + 1)

    # got to goal
    while empty[0] != 36:
        count += 1
        node = swap(node, (empty[0] + 1, empty[1]), empty)
        empty = empty[0] + 1, empty[1]
    if _debug: draw_graph(node[0], node[1], mx + 1, my + 1)

    while node[1] != (0, 0):
        # down
        count += 1
        node = swap(node, (empty[0], empty[1] + 1), empty)
        empty = empty[0], empty[1] + 1

        # left
        for i in range(2):
            count += 1
            node = swap(node, (empty[0] - 1, empty[1]), empty)
            empty = empty[0] - 1, empty[1]

        # up
        count += 1
        node = swap(node, (empty[0], empty[1] - 1), empty)
        if _debug: draw_graph(node[0], node[1], mx + 1, my + 1)
        empty = empty[0], empty[1] - 1

        # left
        count += 1
        node = swap(node, (empty[0] + 1, empty[1]), empty)
        empty = empty[0] + 1, empty[1]

    return count


#draw_graph(graph, (mx, 0), mx + 1, my + 1)

#print(find_shortest_path_bfs(graph, (mx, 0)))

answer = try_this(graph, (mx, 0), mx + 1, my + 1)
print("Part 2 =", answer)
assert answer == 236 # check with accepted answer



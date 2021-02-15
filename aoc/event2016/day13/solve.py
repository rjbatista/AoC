from collections import deque

########
# PART 1

"""
Find x*x + 3*x + 2*x*y + y + y*y.
Add the office designer's favorite number (your puzzle input).
Find the binary representation of that sum; count the number of bits that are 1.
    If the number of bits that are 1 is even, it's an open space.
    If the number of bits that are 1 is odd, it's a wall.
"""

class Maze:
    def __init__(self, fav):
        self._fav = fav

    def get_pos(self, x, y):
        # wall on edge
        if x < 0:
            return 1
        elif y < 0:
            return 1

        v = x * x + 3 * x + 2 * x * y + y + y * y
        v += self._fav

        return 0 if bin(v).count("1") % 2 == 0 else 1

    def create_map(self, w, h):
        map = []
        for y in range(h):
            map += [[]]
            for x in range(w):
                map[y] += [self.get_pos(x, y)]

        return map

    def print_map(self, w, h):
        print("   0123456789")
        for y in range(h):
            print("%2d" % y, end=" ")
            for x in range(w):
                print('.' if self.get_pos(x, y) == 0 else '#', end="")
            print()

    def find_shortest_path_bfs(self, start, end):
        queue = deque([])

        starting_node = start + (0,)
        queue.append(starting_node)

        print(queue)
        while queue:
            x, y, cost = queue.popleft()

            if (x, y) == end:
                print("DONE in ", cost)
                return

            for dx in (-1, 1):
                if self.get_pos(x + dx, y) == 0:
                    queue.append((x + dx, y, cost + 1))

            for dy in (-1, 1):
                if self.get_pos(x, y + dy) == 0:
                    queue.append((x, y + dy, cost + 1))


def find_shortest_path_depth(maze, start, end, visited, cost=0):
    global best_cost

    if cost > best_cost:
        return best_cost

    if start == end:
        #print("found in cost", cost)
        return cost
    else:
        x, y = start
        for dx in (1, -1):
            if maze.get_pos(x + dx, y) == 0 and (x + dx, y) not in visited:
                new_cost = find_shortest_path_depth(maze, (x + dx, y), end, visited + [start], cost + 1)
                if new_cost < best_cost:
                    best_cost = new_cost

        for dy in (1, -1):
            if maze.get_pos(x, y + dy) == 0 and (x, y + dy) not in visited:
                new_cost = find_shortest_path_depth(maze, (x, y + dy), end, visited + [start], cost + 1)
                if new_cost < best_cost:
                    best_cost = new_cost

        return best_cost


def find_most_visited(maze, start, max_steps, steps):
    global visited

    if steps == max_steps:
        return 0
    else:
        x, y = start
        for dx in (1, -1):
            if maze.get_pos(x + dx, y) == 0:
                if (x + dx, y) in visited:
                    if steps >= visited[(x + dx, y)]:
                        continue

                find_most_visited(maze, (x + dx, y), max_steps, steps + 1)
                visited[(x + dx, y)] = steps + 1

        for dy in (1, -1):
            if maze.get_pos(x, y + dy) == 0:
                if (x, y + dy) in visited:
                    if steps + 1 >= visited[(x, y + dy)]:
                        continue

                find_most_visited(maze, (x, y + dy), max_steps, steps + 1)
                visited[(x, y + dy)] = steps + 1

        return best_cost


example = Maze(10)
#example.print_map(10, 7)
best_cost = 50
#print(find_shortest_path_depth(example, (1,1), (7,4), []))

p1 = Maze(1350)
best_cost = 500

answer = find_shortest_path_depth(p1, (1,1), (31,39), [])
print("Part 1 =", answer)
assert answer == 92 # check with accepted answer

########
# PART 2

visited = dict()
visited[(1,1)] = 0
find_most_visited(p1, (1,1), 50, 0)

answer = len(visited)
print("Part 2 =", answer)
assert answer == 124 # check with accepted answer

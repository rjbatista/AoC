from math import inf
from dataclasses import dataclass, replace
import heapq

########
# PART 1

@dataclass(frozen=True)
class Node:
    cost: int
    pods : tuple[tuple[int, int, int], ...]

    def is_organized(self):
        for type, x, y in self.pods:
            if y < 2 or x != type * 2 + 3:
                return False
        
        return True


    def __lt__(self, __o: object) -> bool:
        return self.cost < __o.cost


class World:
    def __init__(self, filename) -> None:
        self.world = {}
        pods = []
        self.width = 0
        self.height = 0

        with open("event2021/day23/" + filename, "r") as file:
            for y, row in enumerate(file):
                for x, ch in enumerate(row.rstrip()):
                    if ch in ['.', '#']:
                        self.world[x, y] = ch
                    elif ch in ['A', 'B', 'C', 'D']:
                        self.world[x, y] = '.'

                        pods += [(ord(ch) - ord('A'), x, y)]

                    self.width = max(self.width, x + 1)

                self.height = max(self.height, y + 1)

        self.starting_pos = Node(0, tuple(sorted(pods)))


    def str(self, node: Node) -> str:
        rep = []
        for y in range(self.height):
            for x in range(self.width):
                rep.append(self.world.get((x, y), ' '))
            rep.append('\n')

        for amphipod, x, y in node.pods:
            rep[y * (self.width + 1) + x] = chr(ord('A') + amphipod)

        return ''.join(rep[:-1])


    def __str__(self) -> str:
        return self.str(self.starting_pos)


    def is_empty(self, node: Node, x, y):
        return self.world[x, y] == '.' and not any([True for _, px, py in node.pods if px == x and py == y])


    def get_positions(self, node, p0):
        todo = [(0, p0)]
        heapq.heapify(todo)
        visited = set()
        possible = []
        while todo:
            cost, (x, y) = heapq.heappop(todo)

            if (x, y) in visited:
                continue

            visited.add((x, y))
            if cost > 0:
                possible.append((cost, (x, y)))

            for (dx, dy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if dx != 0 or dy != 0:
                    nx, ny = x + dx, y + dy

                    if (self.is_empty(node, nx, ny)):
                        if (nx, ny) not in visited:
                            heapq.heappush(todo, (cost + 1, (nx, ny)))

        return possible

    
    def possible_moves(self, node: Node):
        rooms = [0] * 4
        for t, x, y in node.pods:
            if y > 1:
                room_no = (x - 3) // 2
                # is in room
                if room_no != t:
                    # but the wrong one
                    rooms[room_no] = -100

                rooms[room_no] += 1

        for idx, (t, x, y) in enumerate(node.pods):
            if (y >= self.height - rooms[t] - 1 and x == t * 2 + 3):
                continue

            positions = self.get_positions(node, (x, y))

            for distance, (nx, ny) in positions:
                if ny == 1 and nx in [3, 5, 7, 9]:
                    # never stop on the space immediately outside any room
                    continue
                if ny > 1 and (nx != t * 2 + 3 or rooms[t] < 0):
                    # never move from the hallway into a room unless that room is their destination
                    continue
                if y == 1 and ny == 1:
                    # never move from the hallway except to a room
                    continue

                new_pods = list(node.pods)
                new_pods[idx] = (t, nx, ny)

                yield replace(node, cost = node.cost + distance * (10 ** t), pods = tuple(sorted(new_pods)))


    def calc_min_organization_cost(self):
        known = { self.starting_pos: 0 }

        todo = [self.starting_pos]
        heapq.heapify(todo)

        x = 0
        while todo:
            node = heapq.heappop(todo)

            if node.is_organized():
                return node.cost

            for possible in self.possible_moves(node):
                cost = possible.cost

                if cost < known.get(possible.pods, inf):
                    known[possible.pods] = cost
                    heapq.heappush(todo, possible)



assert World("wanted.txt").starting_pos.is_organized()
assert World("wanted.txt").calc_min_organization_cost() == 0

ex1 = World("example1.txt")
assert not ex1.starting_pos.is_organized()
#assert ex1.calc_min_organization_cost() == 12521

inp = World("input.txt")
answer = inp.calc_min_organization_cost()
print("Part 1 =", answer)
assert answer == 18051 # check with accepted answer

########
# PART 2

ex1 = World("example1_p2.txt")
assert not ex1.starting_pos.is_organized()
#assert ex1.calc_min_organization_cost() == 44169

inp = World("input_p2.txt")
answer = inp.calc_min_organization_cost()
print("Part 2 =", answer)
assert answer == 50245 # check with accepted answer

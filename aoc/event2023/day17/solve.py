""" Advent of code 2023 - day 17 """
import heapq
from math import inf
from pathlib import Path

########
# PART 1

type HeatLossMap = list[list[int]]
type Coord = tuple[int, int]


def read(filename: str) -> HeatLossMap:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [[int(x) for x in line.strip()] for line in file]


def calculate_moves(heat_loss_map: HeatLossMap,
                    pos: Coord, direction: Coord,
                    available_moves: tuple[int, int]) -> tuple[Coord, int]:
    """ return the moves from a specific point in a specific direction """

    height = len(heat_loss_map)
    width = len(heat_loss_map[0])
    x, y = pos
    dx, dy = direction
    min_moves, max_moves = available_moves

    cost = 0
    for i in range(max_moves):
        x += dx
        y += dy
        if 0 <= x < width and 0 <= y < height:
            cost += heat_loss_map[y][x]

            if i + 1 >= min_moves:
                yield (x, y), cost


def calculate_turns(direction):
    """ returns the available directions from a direction """
    dx, dy = direction

    yield (dy, dx)
    yield (-dy, -dx)


def find_best_path(heat_loss_map: HeatLossMap, available_moves: tuple[int, int] = (1, 3)) -> int:
    """ Find the best path with heat_map """

    def calculate_distance(pos) -> int:
        return dimensions[0] - 1 - pos[0] + dimensions[1] - 1 - pos[1]

    todo = []
    heapq.heapify(todo)
    best_for_position = {}
    best = inf

    dimensions = len(heat_loss_map[0]), len(heat_loss_map)

    for direction in [(0, 1), (1, 0)]:
        heapq.heappush(todo, (
            # dist, cost, pos, direction
            calculate_distance((0, 0)), 0, (0, 0), direction
        ))

    while todo:
        _, cost, pos, direction = heapq.heappop(todo)

        if best_for_position.get((pos, direction), inf) < cost:
            continue

        for new_pos, add_cost in calculate_moves(heat_loss_map, pos, direction, available_moves):
            new_dist = calculate_distance(new_pos)
            new_cost = cost + add_cost

            if new_dist == 0:
                best = min(best, new_cost)
                continue

            for new_direction in calculate_turns(direction):
                if best_for_position.get((new_pos, new_direction), inf) <= new_cost:
                    continue

                best_for_position[new_pos, new_direction] = new_cost

                heapq.heappush(todo, (
                    # dist, cost, pos, direction
                    new_dist + new_cost, new_cost, new_pos, new_direction
                ))

    return best


ex1 = read("example1.txt")
assert find_best_path(ex1) == 102

inp = read("input.txt")
ANSWER = find_best_path(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 861  # check with accepted answer

########
# PART 2

assert find_best_path(ex1, (4, 10)) == 94

ANSWER = find_best_path(inp, (4, 10))
print("Part 2 =", ANSWER)
assert ANSWER == 1037  # check with accepted answer

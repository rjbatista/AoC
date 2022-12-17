""" Advent of code 2022 - day 16 """
from pathlib import Path
import re
from math import inf

########
# PART 1

def read(filename):
    """ read sensor information """
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        valve_pattern = re.compile(r"^Valve (\w+) .*=(\d+); .* valves? ((?:\w+(?:, )?)+)$")

        valves = {}
        for line_number, line in enumerate(file):
            match = valve_pattern.match(line)
            if match:
                valves[match[1]] = (int(match[2]), match[3].split(', '))
            else:
                raise RuntimeError(f"Invalid input on line {line_number + 1}: {line}")

        return valves


def _find_paths_from(start, valve, valves : dict, all_costs, cost, visited):
    """ Get all possible paths (and distances) from a specific node """

    if start != valve:
        all_costs[(start, valve)] = min(all_costs.get((start, valve), inf), cost)

    visited.add(valve)

    for path in valves[valve][1]:
        if path not in visited:
            _find_paths_from(start, path, valves, all_costs, cost + 1, visited)
    visited.remove(valve)

    return all_costs


def find_paths(valves : dict):
    """ Calculate distances between all nodes """
    all_costs = {}
    for valve in valves.keys():
        all_costs = _find_paths_from(valve, valve, valves, all_costs, 0, set())

    return all_costs


def _find_most_pressure_from(valve, valves, distances, to_visit, remaining, pressure = 0):
    """ Find the most pressure possible from a specific point """
    max_pressure = pressure

    for possibility in to_visit:
        new_rem = remaining - distances[(valve, possibility)] - 1
        new_pressure = pressure + new_rem * valves[possibility][0]

        if new_rem > 0:
            rem_possible = to_visit.difference([possibility])

            if rem_possible:
                max_pressure = max(max_pressure,
                    _find_most_pressure_from(possibility, valves, distances, 
                        rem_possible, new_rem, new_pressure))
            else:
                max_pressure = new_pressure

    return max_pressure


def find_most_pressure(valves : dict, distances : dict, remaining = 30, start = 'AA'):
    """ Find the most pressure possible """
    relevant_valves = set(name for name, (flow, _) in valves.items() if flow > 0)

    return _find_most_pressure_from(start, valves, distances, relevant_valves, remaining)


ex1 = read("example1.txt")
ex1_paths = find_paths(ex1)
assert find_most_pressure(ex1, ex1_paths) == 1651

inp = read("input.txt")
inp_paths = find_paths(inp)
ANSWER = find_most_pressure(inp, inp_paths)
print("Part 1 =", ANSWER)
assert ANSWER == 1647 # check with accepted answer

########
# PART 2

def _find_all_paths(path, remaining, cost, to_visit, all_paths, valves, distances, max_length):
    """ find all possible best paths """

    # could use this for part one too

    for possibility in to_visit:
        new_rem = remaining - distances[(path[-1], possibility)] - 1

        if new_rem > 0 and len(path) < max_length:
            new_cost = cost + new_rem * valves[possibility][0]

            _find_all_paths(path + [possibility], new_rem, new_cost,
                to_visit.difference([possibility]), all_paths, valves, distances, max_length)
        else:
            all_paths.add((cost, tuple(path[1:])))

    return all_paths


def _find_most_pressure_from_p2(start, remaining, to_visit, valves, distances):
    """ Find the most pressure possible from a specific point """

    all_paths = _find_all_paths([start], remaining, 0, to_visit, set(), 
        valves, distances, len(to_visit) // 2 + 1)
    all_paths = sorted(all_paths, reverse = True) # best first

    best = 0
    for best_cost, best_path in all_paths[:200]: # just check with the top 200
        best_path = set(best_path)
        for cost, path in all_paths:
            if path != best_path:
                if best_path.isdisjoint(set(path)):
                    best = max(best, best_cost + cost)

    return best


def find_most_pressure_p2(valves : dict, distances : dict, remaining = 26, start = 'AA'):
    """ Find the most pressure possible """
    relevant_valves = set(name for name, (flow, _) in valves.items() if flow > 0)

    return _find_most_pressure_from_p2(start, remaining, relevant_valves, valves, distances)


assert find_most_pressure_p2(ex1, find_paths(ex1)) == 1707

ANSWER = find_most_pressure_p2(inp, inp_paths)
print("Part 2 =", ANSWER)
assert ANSWER == 2169 # check with accepted answer

""" Advent of code 2022 - day 19 """
from pathlib import Path
from dataclasses import dataclass, replace
from typing import Tuple
import heapq
import re
from math import inf, ceil, prod

########
# PART 1

DEBUG=False

@dataclass(frozen=True)
class FactoryStatus:
    """ An ore operation status """
    time_remaining: int
    ores: int = 0
    ore_robots: int = 1
    clay: int = 0
    clay_robots: int = 0
    obsidian: int = 0
    obsidian_robots: int = 0
    geode: int = 0
    geode_robots: int = 0

    @property
    def resources(self) -> Tuple[int, int, int]:
        """ Get the available resources """
        return (self.ores, self.clay, self.obsidian)

    @property
    def builders(self) -> Tuple[int, int, int]:
        """ Get the available resources """
        return (self.ore_robots, self.clay_robots, self.obsidian_robots)

    @property
    def potential(self) -> int:
        """ Get the potential """
        return (self.geode + self.geode_robots * self.time_remaining
            + self.time_remaining * (self.time_remaining - 1) // 2)

    def __lt__(self, __o: 'FactoryStatus') -> bool:
        return self.potential > __o.potential

    def step(self, minutes = 1, spend = (0, 0, 0), **changes):
        """ Simulate step """
        return replace(self,
            time_remaining = self.time_remaining - minutes,
            ores = self.ores + self.ore_robots * minutes - spend[0],
            clay = self.clay + self.clay_robots * minutes - spend[1],
            obsidian = self.obsidian + self.obsidian_robots * minutes - spend[2],
            geode = self.geode + self.geode_robots * minutes,
            **changes)


@dataclass(frozen=True)
class Factory:
    """ An ore mining robot factory """
    ore_robot_cost: Tuple[int, int, int]
    clay_robot_cost: Tuple[int, int, int]
    obsidian_robot_cost: Tuple[int, int, int]
    geode_robot_cost: Tuple[int, int, int]

    @staticmethod
    def time_to_build(cost, status: FactoryStatus):
        """ Calculate the required time to build """
        have = status.resources
        builders = status.builders

        return max(map(lambda n, b : 0 if n == 0 else (inf if b == 0 else ceil(n / b)),
            map(lambda c, h : max(0, c - h), cost, have), builders)) + 1

    def find_max_geodes(self, time_remaining: int = 24):
        """ Find the max number of geodes in the specified time """

        max_costs = tuple(map(max,
            zip(self.ore_robot_cost, self.clay_robot_cost,
                self.obsidian_robot_cost, self.geode_robot_cost)))

        todo = [FactoryStatus(time_remaining)]
        best = 0
        best_potential = 0
        visited = set()
        heapq.heapify(todo)
        while todo:
            status = heapq.heappop(todo)

            if best_potential > status.potential:
                continue

            # current max geodes
            best_potential = status.geode + status.geode_robots * status.time_remaining

            time_req = Factory.time_to_build(self.geode_robot_cost, status)
            if time_req < status.time_remaining:
                new_status = status.step(time_req, self.geode_robot_cost,
                    geode_robots = status.geode_robots + 1)

                if new_status not in visited:
                    visited.add(new_status)
                    heapq.heappush(todo, new_status)

            time_req = Factory.time_to_build(self.obsidian_robot_cost, status)
            if time_req < status.time_remaining and max_costs[2] > status.obsidian_robots:
                new_status = status.step(time_req, self.obsidian_robot_cost,
                    obsidian_robots = status.obsidian_robots + 1)

                if new_status not in visited:
                    visited.add(new_status)
                    heapq.heappush(todo, new_status)

            time_req = Factory.time_to_build(self.clay_robot_cost, status)
            if time_req < status.time_remaining and max_costs[1] > status.clay_robots:
                new_status = status.step(time_req, self.clay_robot_cost,
                    clay_robots = status.clay_robots + 1)

                if new_status not in visited:
                    visited.add(new_status)
                    heapq.heappush(todo, new_status)

            time_req = Factory.time_to_build(self.ore_robot_cost, status)
            if time_req < status.time_remaining and max_costs[0] > status.ore_robots:
                new_status = status.step(time_req, self.ore_robot_cost,
                    ore_robots = status.ore_robots + 1)

                if new_status not in visited:
                    visited.add(new_status)
                    heapq.heappush(todo, new_status)

            status = status.step(status.time_remaining)

            best = max(best, status.geode)

        return best

    @staticmethod
    def read(filename):
        """ Read blueprints from file. """
        factories = []
        pattern = re.compile(r"^.* (\d+).* (\d+).* (\d+).* (\d+).* (\d+).* (\d+).* (\d+).*$")
        with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
            for line in file:
                match = pattern.match(line)
                values = tuple(map(int, match.groups()[1:7]))

                ore_robot_cost = (values[0], 0, 0)
                clay_robot_cost = (values[1], 0, 0)
                obsidian_robot_cost = (values[2], values[3], 0)
                geode_robot_cost = (values[4], 0, values[5])

                factories.append(
                    Factory(ore_robot_cost, clay_robot_cost, obsidian_robot_cost, geode_robot_cost))

        return factories


def find_quality_levels(factories):
    """ Find the quality levels """
    return sum((factory.find_max_geodes() * idx for idx, factory in enumerate(factories, 1)))


ex1 = Factory.read("example1.txt")
assert find_quality_levels(ex1) == 33

inp = Factory.read("input.txt")
ANSWER = find_quality_levels(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 1294 # check with accepted answer

########
# PART 2

ANSWER = prod([factory.find_max_geodes(32) for factory in inp[:3]])
print("Part 2 =", ANSWER)
assert ANSWER == 13640 # check with accepted answer

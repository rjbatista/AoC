""" Advent of code 2023 - day 05 """
from dataclasses import dataclass, field
from pathlib import Path
import re

########
# PART 1


@dataclass
class Transformer:
    """ Transformer from source """

    type Mapping = tuple[int, int, int]

    source: str
    name: str
    _mappings: list[Mapping] = field(default_factory=list)

    def add_mapping(self, source_idx: int, dest_idx: int, length: int):
        """ Add a mapping range to the transformer """
        self._mappings.append((source_idx, dest_idx, length))

    def transform(self, value: int) -> int:
        """ Transform a value """

        # could sort this and cull searches but are few ranges to bother
        for mapping in self._mappings:
            source_idx, dest_idx, length = mapping

            if source_idx <= value < source_idx + length:
                return value - source_idx + dest_idx

        return value

    def find_applicable_mapping(self, range_start: int, range_len: int) -> list[Mapping]:
        """ find the first mapping applicable to the range """

        for mapping in self._mappings:
            source_idx, _, map_len = mapping

            if range_start < source_idx + map_len and source_idx < range_start + range_len:
                return mapping

        return None


type TransformerMap = dict[str, Transformer]


def read(filename: str) -> tuple[list[int], TransformerMap]:
    """ Read the file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        transformers = {}
        seeds = list(map(int, file.readline().split(' ')[1:]))
        file.readline()
        map_expr = re.compile(r'^(\w+)-to-(\w+) map:$')

        while True:
            map_text = file.readline()

            if map_text:
                source, dest = map_expr.match(map_text).groups()
                transformer = Transformer(source, dest)

                while True:
                    map_range = file.readline().strip()

                    if map_range:
                        dest_idx, source_idx, length = map(int, map_range.split(' '))

                        transformer.add_mapping(source_idx, dest_idx, length)
                    else:
                        break

                transformers[transformer.source] = transformer
            else:
                break

        return seeds, transformers


def get_locations(seeds: list[int], transformers: TransformerMap) -> list[int]:
    """ Get the location for the specified seeds, using the transformers """
    current = "seed"

    values = seeds
    while current != 'location':
        current_transformer = transformers[current]

        values = map(current_transformer.transform, values)

        current = current_transformer.name

    return list(values)


ex1 = read("example1.txt")
assert min(get_locations(*ex1)) == 35

inp = read("input.txt")
ANSWER = min(get_locations(*inp))
print("Part 1 =", ANSWER)
assert ANSWER == 650599855  # check with accepted answer

########
# PART 2

type SeedRange = tuple[int, int]


def get_seed_ranges(seeds: list[int]) -> list[SeedRange]:
    """ Returns the seed ranges from the seeds list """
    return list(zip(seeds[::2], seeds[1::2]))


def get_locations_for_ranges(ranges: list[SeedRange], transformers: TransformerMap) -> list[int]:
    """ Get the location for the specified seed ranges, using the transformers """
    current = "seed"

    while current != 'location':
        current_transformer = transformers[current]

        todo = ranges[:]
        ranges = []
        while todo:
            range_start, range_len = todo.pop()

            mapping = current_transformer.find_applicable_mapping(range_start, range_len)

            if mapping:
                source_idx, dest_idx, mapping_len = mapping
                mapping_op = dest_idx - source_idx

                # has non applicable before
                if range_start < source_idx:
                    new_range_start = range_start
                    new_range_length = source_idx - range_start

                    todo.append((new_range_start, new_range_length))

                    # process only the rest
                    range_start = source_idx
                    range_len -= new_range_length

                # has non applicable after
                if range_start + range_len > source_idx + mapping_len:
                    new_range_start = source_idx + mapping_len
                    new_range_length = range_start + range_len - (source_idx + mapping_len)

                    todo.append((new_range_start, new_range_length))

                    # process only the rest
                    range_len -= new_range_length

                ranges.append((range_start + mapping_op, range_len))
            else:
                ranges.append((range_start, range_len))

        current = current_transformer.name

    return ranges


ex1_seed_ranges = get_seed_ranges(ex1[0])
assert min(get_locations_for_ranges(ex1_seed_ranges, ex1[1]))[0] == 46

inp_seed_ranges = get_seed_ranges(inp[0])

ANSWER = min(get_locations_for_ranges(inp_seed_ranges, inp[1]))[0]
print("Part 2 =", ANSWER)
assert ANSWER == 1240035  # check with accepted answer

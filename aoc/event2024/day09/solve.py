""" Advent of code 2024 - day 09 """

from dataclasses import dataclass
from itertools import count
from pathlib import Path
from typing import Self

########
# PART 1

type Diskmap = list[tuple[int, int]]


def read(filename: str) -> Diskmap:
    """ Read from a file """

    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        line = file.readline().strip()
        bid = count(0)
        diskmap = []

        is_file = True
        for ch in line:
            if is_file:
                diskmap.append((next(bid), int(ch)))
            else:
                diskmap.append((None, int(ch)))

            is_file = not is_file

        return diskmap


def compact_block(diskmap: Diskmap) -> Diskmap:
    """ Compact HD moving one block """
    diskmap = diskmap[:]

    free_idx = 0
    block_idx = len(diskmap) - 1
    while True:
        while diskmap[free_idx][0] is not None:
            free_idx += 1

        while not diskmap[block_idx][0]:
            block_idx -= 1

        if free_idx > block_idx:
            break

        prev_block = free_idx - 1 if free_idx > 0 else None
        next_block = block_idx + 1 if block_idx < len(diskmap) - 1 else None
        block_id = diskmap[block_idx][0]

        # how much can I move?
        move_size = min(diskmap[free_idx][1], diskmap[block_idx][1])

        # move blocks
        diskmap[free_idx] = None, diskmap[free_idx][1] - move_size
        diskmap[block_idx] = block_id, diskmap[block_idx][1] - move_size

        # add to previous?
        if prev_block and diskmap[prev_block][0] == block_id:
            diskmap[prev_block] = block_id, diskmap[prev_block][1] + move_size
        else:
            diskmap.insert(free_idx, (block_id, move_size))
            free_idx += 1

        # add free space to next?
        if next_block and diskmap[next_block][0] is None:
            diskmap[next_block] = None, diskmap[next_block][1] + move_size
        else:
            diskmap.append((None, move_size))

        if diskmap[free_idx][1] == 0:
            del diskmap[free_idx]

    return diskmap


def print_blocks(diskmap: Diskmap, idx: int = None):
    """ print diskmap blocks """
    alternate = False
    for bid, size in diskmap:
        ch = str(bid) if bid is not None else '.'

        if alternate:
            print("\033[32;1m", end="")

        print((size * ch), end="")

        if alternate:
            print("\033[0m", end="")

        alternate = not alternate

    print()

    if idx is not None:
        for i in range(idx):
            print(diskmap[i][1] * " ", end="")
        print("^")


def checksum(diskmap: Diskmap) -> int:
    """ calculate the diskmap checksum """

    pos = 0
    total = 0
    for bid, length in diskmap:
        if bid is None:
            pos += length
            continue

        for _ in range(length):
            total += pos * bid
            pos += 1

    return total


ex1 = read("example1.txt")
assert checksum(compact_block(ex1)) == 1928

inp = read("input.txt")
ANSWER = checksum(compact_block(inp))
print("Part 1 =", ANSWER)
assert ANSWER == 6344673854800  # check with accepted answer

########
# PART 2


@dataclass
class BlockNode():
    """ Class representing block linked list node """
    bid: int
    length: int
    prev: Self
    next: Self = None

    def __post_init__(self):
        if self.prev:
            self.prev.next = self

    def to_diskmap(self) -> Diskmap:
        """ List to diskmap """
        current = self
        diskmap = []
        while current:
            diskmap.append((current.bid, current.length))
            current = current.next

        return diskmap

    @property
    def is_free_space(self) -> bool:
        """ Indicator for freespace """
        return self.bid is None

    @staticmethod
    def find_free_space(start: Self, before: Self, min_length: int) -> Self:
        """ Return the first free space node of at least the specified length """
        current = start
        while current:
            if current == before:
                return None

            if current.is_free_space and current.length >= min_length:
                return current

            current = current.next

        return None


# this can be better, searching the linked list is not perfect
# free spaces can be stored more eficiently - maybe if I get time to revisit this
def compact_file(diskmap: Diskmap) -> Diskmap:
    """ Compact HD moving one file """

    disklinked = None
    current = None
    last_block = None
    for bid, length in diskmap:
        node = BlockNode(bid, length, current)

        if not disklinked:
            disklinked = node

        if not node.is_free_space:
            last_block = node

        current = node

    current = last_block
    while current:
        current_block_id = current.bid
        free = BlockNode.find_free_space(disklinked, current, current.length)

        if free:
            next_block = current.prev

            # remove from current position
            if current.next and current.next.is_free_space:
                current.next.length += current.length
                current.next.prev = current.prev

            else:
                new_free = BlockNode(None, current.length, current.prev, current.next)
                current.next = new_free

            if current.prev:
                if current.prev.is_free_space:
                    current.prev.length += current.next.length
                    current.prev.next = current.next.next

                    del current.next
                else:
                    current.prev.next = current.next

            # insert into new position
            free.length -= current.length

            current.prev = free.prev
            current.prev.next = current
            free.prev = current

            if free.length:
                current.next = free
            else:
                current.next = free.next
                free.next.prev = current

                del free

            current = next_block
        else:
            # no space available
            current = current.prev

        while current and (current.is_free_space or current.bid > current_block_id):
            current = current.prev

    return disklinked.to_diskmap()


assert checksum(compact_file(ex1)) == 2858


ANSWER = checksum(compact_file(inp))
print("Part 2 =", ANSWER)
assert ANSWER == 6360363199987  # check with accepted answer

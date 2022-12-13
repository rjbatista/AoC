""" Advent of code 2022 - day 13 """
from pathlib import Path
from typing import List, Tuple
from functools import total_ordering
from ast import literal_eval


########
# PART 1

def read(filename) -> Tuple[List, List]:
    """ read signal lists """
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        left = []
        right = []
        while True:
            line = file.readline()
            if line:
                left.append(literal_eval(line))
                right.append(literal_eval(file.readline()))
                file.readline()
            else:
                break

        return left, right


def compare_signal(left_value, right_value) -> int:
    """
    Compare the two signal values.
    Return:
        0 if equal
        <0 if left is lower
        >0 if right is lower
    """

    #print("Comparing", left_value, "to", right_value)

    if isinstance(left_value, int) and isinstance(right_value, int):
        return left_value - right_value

    if isinstance(left_value, list) and isinstance(right_value, list):
        for idx in range(min(len(left_value), len(right_value))):
            cmp = compare_signal(left_value[idx], right_value[idx])

            if cmp != 0:
                return cmp

        return len(left_value) - len(right_value)

    left_value = left_value if isinstance(left_value, list) else [left_value]
    right_value = right_value if isinstance(right_value, list) else [right_value]

    return compare_signal(left_value, right_value)


def right_order_sum(left, right):
    """ return the sum of indexes (1 based) with the right order """

    return sum((idx + 1 for idx in range(len(left)) if compare_signal(left[idx], right[idx]) < 0))


ex1 = read("example1.txt")
assert right_order_sum(*ex1) == 13

inp = read("input.txt")
ANSWER = right_order_sum(*inp)
print("Part 1 =", ANSWER)
assert ANSWER == 5938 # check with accepted answer

########
# PART 2

@total_ordering
class Signal:
    """ Special list class (for sorting and index of elements) """
    def __init__(self, value_list) -> None:
        self.list = value_list

    def __lt__(self, __o: object) -> bool:
        return compare_signal(self.list, __o.list) < 0

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, list):
            return compare_signal(self.list, __o) == 0

        return compare_signal(self.list, __o.list) == 0

    def __repr__(self) -> str:
        return str(self.list)


def get_decoder_key(left, right):
    """ Calculate the decoder key for the distress signal  """
    marker_left = [[2]]
    marker_right = [[6]]

    sorted_list = sorted([Signal(lst) for lst in left + right + [marker_left] + [marker_right]])

    return (sorted_list.index(marker_left) + 1) * (sorted_list.index(marker_right) + 1)


assert get_decoder_key(*ex1) == 140

ANSWER = get_decoder_key(*inp)
print("Part 2 =", ANSWER)
assert ANSWER == 29025 # check with accepted answer

""" Advent of code 2022 - day 06 """
from pathlib import Path

########
# PART 1

def read(filename):
    """ Read input """
    with Path(__file__).parent.joinpath(filename).open("r") as file:
        return file.readline().strip()


def find_marker(datastream, size = 4):
    """ Find marker (<size> different chars) on the data stream """

    for idx in range(len(datastream) - size):
        # could just add and remove as we move along the stream,
        # but it's cleaner this way and still works quickly for day 6
        if len(set(datastream[idx:idx + size])) == size:
            return idx + size

    return None


assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb") == 7

# bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 5
assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
# nppdvjthqldpwncqszvftbrmjlhg: first marker after character 6
assert find_marker("nppdvjthqldpwncqszvftbrmjlhg") == 6
# nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 10
assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
# zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 11
assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

inp = read("input.txt")
answer = find_marker(inp)
print("Part 1 =", answer)
assert answer == 1896 # check with accepted answer

########
# PART 2

# mjqjpqmgbljsphdztnvjfqwrcgsmlb: first marker after character 19
assert find_marker("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14) == 19
# bvwbjplbgvbhsrlpgdmjqwftvncz: first marker after character 23
assert find_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 14) == 23
# nppdvjthqldpwncqszvftbrmjlhg: first marker after character 23
assert find_marker("nppdvjthqldpwncqszvftbrmjlhg", 14) == 23
# nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg: first marker after character 29
assert find_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14) == 29
# zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw: first marker after character 26
assert find_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14) == 26

answer = find_marker(inp, 14)
print("Part 2 =", answer)
assert answer == 3452 # check with accepted answer

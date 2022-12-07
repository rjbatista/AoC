"""
Advent of code 2022 - day 17

Again, runs instantly in pypy
"""

########
# PART 1

def spinlock_get_after_last(step = 3, num = 2017):
    """ Runs the spinlock for num times and returns the value inserted after the last """
    lst = [0]
    pos = 0
    for i in range(num):
        pos = (pos + step) % len(lst) + 1

        lst.insert(pos, i + 1)

    return lst[pos + 1]


PUZZLE_INPUT = 314

assert spinlock_get_after_last() == 638

answer = spinlock_get_after_last(PUZZLE_INPUT)
print("Part 1 =", answer)
assert answer == 355 # check with accepted answer

########
# PART 2

def spinlock_get_first(step = 3, num = 50000000):
    """ Runs the spinlock for num times and returns the value inserted after the last """
    pos = 0
    size = 1
    for i in range(num):
        pos = (pos + step) % size + 1
        size += 1

        if pos == 1:
            relevant_value = i + 1

    return relevant_value

answer = spinlock_get_first(PUZZLE_INPUT)
print("Part 2 =", answer)
assert answer == 6154117 # check with accepted answer

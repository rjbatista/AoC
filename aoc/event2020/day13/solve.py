from math import ceil

########
# PART 1

def get_buses(fn):
    with open("event2020/day13/" + fn) as file:
        return int(file.readline()), [(int(x), t) for t, x in enumerate(file.readline().split(',')) if x != 'x']


def get_earliest(timestamp, buses):
    return min([(bus * ceil(timestamp / bus) - timestamp, bus) for bus, _ in buses])


min_wait = get_earliest(*get_buses("example1.txt"))
assert min_wait[0] * min_wait[1] == 295


earliest, buses = get_buses("input.txt")
min_wait = get_earliest(earliest, buses)
answer = min_wait[0] * min_wait[1]
print("Part 1 =", answer)
assert answer == 2545 # check with accepted answer

########
# PART 2

def get_first_in_sequence(buses):
    period = 1
    min_for_all = 0
    for bus, ts in buses:
        while ((min_for_all + ts) % bus) != 0:
            min_for_all += period
        period *= bus

    return min_for_all


assert get_first_in_sequence(get_buses("example1.txt")[1]) == 1068781


answer = get_first_in_sequence(get_buses("input.txt")[1])
print("Part 2 =", answer)
assert answer == 266204454441577 # check with accepted answer

import math

########
# PART 1

def read(filename):
    """ parse the input """
    with open("event2021/day03/" + filename, "r") as file:
        return [x.strip() for x in file.readlines()]


def get_rates(report):
    mcb = [0] * len(report[0])
    for line in report:
        for index, pos in enumerate(line):
            mcb[index] += 1 if pos == '1' else -1

    gamma_rate = int("".join(['1' if p >= 0 else '0' for p in mcb]), 2)
    epsilon_rate = int("".join(['1' if p < 0 else '0' for p in mcb]), 2)

    return gamma_rate, epsilon_rate


ex1 = read("example1.txt")
assert math.prod(get_rates(ex1)) == 198

inp = read("input.txt")
answer = math.prod(get_rates(inp))
print("Part 1 =", answer)
assert answer == 4160394 # check with accepted answer


########
# PART 2

def get_rate(report, check):
    mcb = [0] * len(report[0])
    for line in report:
        for index, pos in enumerate(line):
            mcb[index] += 1 if pos == '1' else -1

    rate = int("".join(['1' if check(p) else '0' for p in mcb]), 2)

    return rate


def get_rating(report):
    valid_reports_for_o2 = report[:]
    valid_reports_for_co2 = report[:]
    l = len(report[0])

    for i in range(l):
        # could be simplified to get just a specific bit...
        o2_rate = get_rate(valid_reports_for_o2, lambda x : x >= 0)
        co2_rate = get_rate(valid_reports_for_co2, lambda x : x < 0)

        o2_bit = o2_rate >> (l - i - 1) & 1
        co2_bit = co2_rate >> (l - i - 1) & 1

        if len(valid_reports_for_o2) > 1:
            valid_reports_for_o2 = [x for x in valid_reports_for_o2 if int(x[i]) == o2_bit]

        if len(valid_reports_for_co2) > 1:
            valid_reports_for_co2 = [x for x in valid_reports_for_co2 if int(x[i]) == co2_bit]

    return int(valid_reports_for_o2[0], 2), int(valid_reports_for_co2[0], 2)


assert math.prod(get_rating(ex1)) == 230


answer = math.prod(get_rating(inp))
print("Part 2 =", answer)
assert answer == 4125600 # check with accepted answer

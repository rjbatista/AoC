########
# PART 1

def read(filename):
    with open("event2017/day06/" + filename, "r") as file:
        banks = [int(x) for x in file.readline().strip().split()]

    return banks


def redistribute(banks):
    max_value = max(banks)
    p = banks.index(max_value)
    size = len(banks)

    adder = int(max_value / size)
    banks[p] = 0
    if (adder > 0):
        banks = [x + adder for x in banks]

    for i in range(max_value % size):
        banks[(1 + p + i) % size] += 1


def find_cycles(starting_banks):
    banks = starting_banks[:]
    cycles = 0

    known_configurations = set()

    while str(banks) not in known_configurations:
        cycles += 1
        known_configurations.add(str(banks))
        redistribute(banks)

    return cycles, banks


ex1 = [0, 2, 7, 0]
ex1_cycles, ex1_banks = find_cycles(ex1)
assert ex1_cycles == 5

inp = read("input.txt")
answer, inp_banks = find_cycles(inp)
print("Part 1 =", answer)
assert answer == 5042 # check with accepted answer


########
# PART 2

def find_loop(starting_banks):
    banks = starting_banks[:]
    cycles = 1

    wanted_key = str(starting_banks)
    redistribute(banks)
    while str(banks) != wanted_key:
        cycles += 1
        redistribute(banks)

    return cycles


assert find_loop(ex1_banks) == 4

answer = find_loop(inp_banks)
print("Part 2 =", answer)
assert answer == 1086 # check with accepted answer

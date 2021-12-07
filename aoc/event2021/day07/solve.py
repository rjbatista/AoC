########
# PART 1

def read(filename):
    with open("event2021/day07/" + filename, "r") as file:
        positions = [int(x) for x in file.readline().strip().split(",")]
        
    return positions


def calculate_cost_to_align(positions, desired_pos):
    return sum([abs(x - desired_pos) for x in positions])


def min_cost_to_align(positions, calculate_cost = calculate_cost_to_align):
    return min([calculate_cost(positions, desired) for desired in range(len(positions))])


ex1 = read("example1.txt")
assert min_cost_to_align(ex1) == 37

inp = read("input.txt")
answer = min_cost_to_align(inp)
print("Part 1 =", answer)
assert answer == 356922 # check with accepted answer


########
# PART 2

def calculate_cost_to_align_p2(positions, desired_pos):
    return sum([sum(range(abs(x - desired_pos) + 1)) for x in positions])


assert min_cost_to_align(ex1, calculate_cost_to_align_p2) == 168

answer = min_cost_to_align(inp, calculate_cost_to_align_p2)
print("Part 2 =", answer)
assert answer == 100347031 # check with accepted answer

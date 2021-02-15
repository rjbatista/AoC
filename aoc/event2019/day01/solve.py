from math import floor

########
# PART 1

def process_input(input):
    return [x for x in [floor(int(fuel) / 3) - 2 for fuel in input] if x > 0]

with open("event2019/day01/input.txt", "r") as input:
    answer = sum(process_input(input))
    print("Part 1 =", answer)
    assert answer == 3275518 # check with accepted answer

########
# PART 2

with open("event2019/day01/input.txt", "r") as first_input:
    total = 0
    input = first_input

    while input:
        new_input = process_input(input)
        total += sum(input)
        input = new_input

print("Part 2 =", total)
assert total == 4910404 # check with accepted answer

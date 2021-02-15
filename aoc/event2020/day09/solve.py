from itertools import combinations

########
# PART 1

def get_numbers(fn):
    with open("event2020/day09/" + fn, "r") as file:
        for line in file:
            yield int(line[:-1])

def is_valid(number, list):
    return len([(a, b) for a, b in combinations(list, 2) if a + b == number]) > 0

def get_invalid(fn, preamble = 25):
    numbers = get_numbers(fn)
    list = []
    for _ in range(preamble):
        list.append(next(numbers))
    
    while True:
        test_value = next(numbers)
        if not is_valid(test_value, list):
            return test_value
        else:
            list.pop(0)
            list.append(test_value)

assert get_invalid("example1.txt", 5) == 127

answer = get_invalid("input.txt")
print("Part 1 =", answer)
assert answer == 22477624 # check with accepted answer

########
# PART 2

def get_contiguous_set(fn, wanted):
    list = []

    current = 0
    numbers = get_numbers(fn)
    while current != wanted:
        if current < wanted:
            list.append(next(numbers))
        elif current > wanted:
            list.pop(0)

        current = sum(list)

    return list

answer = get_contiguous_set("example1.txt", 127)
assert min(answer) + max(answer) == 62

answer = get_contiguous_set("input.txt", 22477624)
answer = min(answer) + max(answer)
print("Part 2 =", answer)
assert answer == 2980044 # check with accepted answer

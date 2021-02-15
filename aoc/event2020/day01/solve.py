from functools import reduce
from itertools import combinations
from operator import mul

########
# PART 1
def select_combinations(list, wanted, elements = 2):
    for v in combinations(list, elements):
        if sum(v) == wanted: return v
    
    return None

def get_answer(answer):
    return reduce(mul, answer)

assert get_answer(select_combinations([1721,979,366,299,675,1456], 2020)) == 514579

with open("event2020/day01/input.txt", "r") as input:
    list = [int(x) for x in input]

combination = select_combinations(list, 2020)
answer = get_answer(combination)
print("Part 1 =", combination, "=", answer)
assert answer == 956091 # check with accepted answer

########
# PART 2

combination = select_combinations(list, 2020, 3)
answer = get_answer(combination)
print("Part 2 =", combination, "=", answer)
assert answer == 79734368 # check with accepted answer

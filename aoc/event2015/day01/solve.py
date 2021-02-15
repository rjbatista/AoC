from functools import reduce

########
# PART 1

def find_difference():
    floor = 0
    with open("event2015/day01/input.txt") as f:
        for ch in f.readline():
            if ch == '(':
                floor += 1
            elif ch == ')':
                floor -= 1
    
    return floor

answer = find_difference()
print("Part 1 =", answer)
assert answer == 232 # check with accepted answer

########
# PART 2

def find_first():
    floor = 0
    with open("event2015/day01/input.txt") as f:
        for idx, ch in enumerate(f.readline()):
            if ch == '(':
                floor += 1
            elif ch == ')':
                floor -= 1
            
            if floor < 0:
                return idx + 1

answer = find_first()
print("Part 2 =", answer)
assert answer == 1783 # check with accepted answer

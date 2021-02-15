import re

########
# PART 1

def has_three_vowels(s):
    return re.search(r"(?i)(.*[aeiou]){3}", s) != None


def has_double_letter(s):
    return re.search(r"(\w)\1", s) != None


def has_disallowed(s):
    return re.search(r"ab|cd|pq|xy", s) != None


def is_nice(s):
    return has_three_vowels(s) and has_double_letter(s) and not has_disallowed(s)


########
# PART 2

def has_two_pairs(s):
    return re.search(r"(\w{2}).*\1", s) != None


def has_one_repeat(s):
    return re.search(r"(\w)\w\1", s) != None


def is_new_nice(s):
    return has_two_pairs(s) and has_one_repeat(s)


with open('event2015/day05/input.txt', 'r') as f:
    nice = 0
    newNice = 0

    for line in f:
        if is_nice(line): nice += 1
        if is_new_nice(line): newNice += 1


answer = nice
print("Part 1 =", answer)
assert answer == 258 # check with accepted answer

answer = newNice
print("Part 2 =", answer)
assert answer == 53 # check with accepted answer

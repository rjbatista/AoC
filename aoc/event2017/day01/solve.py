from itertools import cycle

########
# PART 1

def read(filename):
    """ parse the input """
    with open("event2017/day01/" + filename, "r") as file:
        digits = file.readline()[:-1]

    return digits


def sum_significant_digits(digits):
    """ calculate the sum of the digits that match the next """
    return sum([int(x) for x, y in zip(digits, cycle(digits[1:] + digits[0])) if x == y])


#1122 produces a sum of 3 (1 + 2) because the first digit (1) matches the second digit and the third digit (2) matches the fourth digit.
assert sum_significant_digits("1122") == 3
#1111 produces 4 because each digit (all 1) matches the next.
assert sum_significant_digits("1111") == 4
#1234 produces 0 because no digit matches the next.
assert sum_significant_digits("1234") == 0
#91212129 produces 9 because the only digit that matches the next one is the last digit, 9.
assert sum_significant_digits("91212129") == 9

inp = read("input.txt")
answer = sum_significant_digits(inp)
print("Part 1 =", answer)
assert answer == 1044 # check with accepted answer


########
# PART 2

def sum_significant_digits_halfway(digits):
    """ calculate the sum of the digits that match the halfway around """
    halfway = int(len(digits) / 2)
    return sum([int(x) for x, y in zip(digits, cycle(digits[halfway:] + digits[:halfway])) if x == y])


#1212 produces 6: the list contains 4 items, and all four digits match the digit 2 items ahead.
assert sum_significant_digits_halfway("1212") == 6
#1221 produces 0, because every comparison is between a 1 and a 2.
assert sum_significant_digits_halfway("1221") == 0
#123425 produces 4, because both 2s match each other, but no other digit has a match.
assert sum_significant_digits_halfway("123425") == 4
#123123 produces 12.
assert sum_significant_digits_halfway("123123") == 12
#12131415 produces 4.
assert sum_significant_digits_halfway("12131415") == 4

answer = sum_significant_digits_halfway(inp)
print("Part 2 =", answer)
#assert answer == 1054 # check with accepted answer

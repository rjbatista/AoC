########
# PART 1

def read(filename):
    with open("event2017/day04/" + filename, "r") as file:
        return [passphrase.strip() for passphrase in file.readlines()]


def is_valid(passphrase):
    used = set()

    for word in passphrase.split():
        if word in used:
            return False
        used.add(word)
    
    return True


# aa bb cc dd ee is valid.
assert is_valid("aa bb cc dd ee")
# aa bb cc dd aa is not valid - the word aa appears more than once.
assert not is_valid("aa bb cc dd aa")
# aa bb cc dd aaa is valid - aa and aaa count as different words.
assert is_valid("aa bb cc dd aaa")


inp = read("input.txt")
answer = sum([1 for passphrase in inp if is_valid(passphrase)])
print("Part 1 =", answer)
assert answer == 455 # check with accepted answer


########
# PART 2

def is_valid_p2(passphrase):
    used = set()

    for word in passphrase.split():
        key = "".join(sorted(list(word)))
        if key in used:
            return False
        used.add(key)
    
    return True


# abcde fghij is a valid passphrase.
assert is_valid_p2("abcde fghij")
# abcde xyz ecdab is not valid - the letters from the third word can be rearranged to form the first word.
assert not is_valid_p2("abcde xyz ecdab")
# a ab abc abd abf abj is a valid passphrase, because all letters need to be used when forming another word.
assert is_valid_p2("a ab abc abd abf abj")
# iiii oiii ooii oooi oooo is valid.
assert is_valid_p2("iiii oiii ooii oooi oooo")
# oiii ioii iioi iiio is not valid - any of these words can be rearranged to form any other word.
assert not is_valid_p2("oiii ioii iioi iiio")

answer = sum([1 for passphrase in inp if is_valid_p2(passphrase)])
print("Part 2 =", answer)
assert answer == 186 # check with accepted answer

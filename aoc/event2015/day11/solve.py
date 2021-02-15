'''
Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz.
    They cannot skip letters; abd doesn't count.
Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.
'''
import re

########
# PART 1

forbidden_letters_pattern = re.compile(r"i|o|l")
pairs_pattern = re.compile(r"([a-z])\1.*([a-z])\2")

def decode_password(s):
    value = 0;

    for val in [ord(c) - ord('a') for c in s]: value = val + value * 26

    return value


def encode_password(val, length = 8):
    l = []
    while (val > 0):
        l += [val % 26]
        val = val // 26

    return ''.join(reversed([chr(c + ord('a')) for c in l])).rjust(length, 'a')


def is_sequence(s):
    return ord(s[0]) - ord(s[1]) == ord(s[1]) - ord(s[2]) == -1


def has_sequence(s):
    for i in range(0, len(s) - 2):
        if (is_sequence(s[i:i+3])):
            return True

    return False


def is_valid_password(s):
    return forbidden_letters_pattern.search(s) == None and pairs_pattern.search(s) != None and has_sequence(s)


def find_next_valid(s):
    val = decode_password(s)
    val += 1
    while True:
        s = encode_password(val)

        if is_valid_password(s):
            return s

        val += 1


inp = 'hxbxwxba'

answer = find_next_valid(inp)
print("Part 1 =", answer)
assert answer == "hxbxxyzz" # check with accepted answer

########
# PART 2

answer = answer = find_next_valid(answer)
print("Part 2 =", answer)
assert answer == "hxcaabcc" # check with accepted answer

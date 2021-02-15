import re

########
# PART 1

def process_line(line):
    m = re.match(r"(.*)-(\d+)\[(.*)\]", line)

    return int(m.group(2)), m.group(1), m.group(3)


def read_input():
    with open("event2016/day04/input.txt") as f:
        ret = []
        for line in f:
            ret += [ process_line(line) ]

    return ret


def count_letters(name):
    dict = {}

    for letter in name:
        if letter in dict:
            dict[letter] += 1
        else:
            dict[letter] = 1

    return sorted(dict.items(), key=lambda x : (-x[1], x[0])) # reverse on first, order on second


def calc_checksum(name):
    counts = count_letters(name.replace('-', ''))
    return ''.join([x[0] for x in counts[:5]])


def is_valid_room(room):
    return calc_checksum(room[1]) == room[2]


# is a real room because the most common letters are a (5), b (3), and then a tie between x, y, and z, which are listed alphabetically.
assert is_valid_room(process_line("aaaaa-bbb-z-y-x-123[abxyz]")) == True

# is a real room because although the letters are all tied (1 of each), the first five are listed alphabetically.
assert is_valid_room(process_line("a-b-c-d-e-f-g-h-987[abcde]")) == True

# is a real room.
assert is_valid_room(process_line("not-a-real-room-404[oarel]")) == True

# is not.
assert is_valid_room(process_line("totally-real-room-200[decoy]")) == False

rooms = read_input()
answer = sum([room[0] for room in rooms if is_valid_room(room)])
print("Part 1 =", answer)
assert answer == 137896 # check with accepted answer

########
# PART 2

def decode_name(name, value):
    plaintext = ''
    for letter in name:
        if (letter == '-'):
            plaintext += ' '
        else:
            pos = ord(letter) - ord('a')
            pos = (pos + value) % 26
            plaintext += chr(ord('a') + pos)

    return plaintext


def decode_names(rooms):
    return [(room[0], decode_name(room[1], room[0])) for room in rooms if is_valid_room(room)]


assert decode_name("qzmt-zixmtkozy-ivhz", 343) == "very encrypted name"

possible = [(id, room) for id, room in decode_names(rooms) if room.lower().find("north") >= 0]
assert len(possible) == 1
answer = possible[0]
print("Part 2 =", answer)
assert answer[0] == 501 # check with accepted answer

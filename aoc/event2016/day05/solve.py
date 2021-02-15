import hashlib

########
# PART 1

def find_hash(door, index):
    base = door.encode('ascii')
    while True:
        hash = hashlib.md5(base + str(index).encode('ascii')).digest()

        # starts with 00000
        if (hash[0] == hash[1] == hash[2] >> 4 == 0):
            break

        index += 1

    return hashlib.md5(base + str(index).encode('ascii')).hexdigest(), index


def find_next(door, index):
    hash, index = find_hash(door, index)

    next = hash[5]

    return next, index


def find_password(door, size = 8):
    pw = ""

    index = 0
    for _ in range(size):
        next, index = find_next(door, index)
        pw += next
        index += 1

    return pw


#print(find_password("abc", 8))

puzzle_input = "ojvtpuvg"

answer = find_password(puzzle_input)
print("Part 1 =", answer)
assert answer == "4543c154" # check with accepted answer


########
# PART 2

def find_password_p2(door, size = 8):
    pw = [ None ] * 8

    index = 0
    found = 0
    while True:
        hash, index = find_hash(door, index)
        index += 1

        pos = ord(hash[5]) - ord('0')
        if pos < 8:
            if pw[pos] is None:
                pw[pos] = hash[6]
                found += 1

                print("found one ", ''.join([ch if ch is not None else '_' for ch in pw]), end="\r")

                if found == 8:
                    break
    
    print()

    return ''.join(pw)


#print(find_password_p2("abc", 8))

#reusing the already calculated hashes would be better :)
answer = find_password_p2(puzzle_input)
print("Part 2 =", answer)
assert answer == "1050cbbd" # check with accepted answer

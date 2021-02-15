import re

########
# PART 1

def decompress(s):
    p = re.compile(r'\((\d+)x(\d+)\)')

    pos = 0

    todo = s
    done = ''
    while True:
        m = re.search(p, todo)

        if (m):
            dataSize = int(m.group(1))
            reps = int(m.group(2))

            data = todo[m.end():m.end() + dataSize]

            done += todo[:m.start()] + (data * reps)
            todo = todo[m.end() + dataSize:]

        else:
            done += todo
            break

    return done


# ADVENT contains no markers and decompresses to itself with no changes, resulting in a decompressed length of 6.
assert decompress('ADVENT') == 'ADVENT'
# A(1x5)BC repeats only the B a total of 5 times, becoming ABBBBBC for a decompressed length of 7.
assert decompress('A(1x5)BC') == 'ABBBBBC'
# (3x3)XYZ becomes XYZXYZXYZ for a decompressed length of 9.
assert decompress('(3x3)XYZ') == 'XYZXYZXYZ'
# A(2x2)BCD(2x2)EFG doubles the BC and EF, becoming ABCBCDEFEFG for a decompressed length of 11.
assert decompress('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG'
# (6x1)(1x3)A simply becomes (1x3)A - the (1x3) looks like a marker, but because it's within a data section of another marker, it is not treated any differently from the A that comes after it. It has a decompressed length of 6.
assert decompress('(6x1)(1x3)A') == '(1x3)A'
# X(8x2)(3x3)ABCY becomes X(3x3)ABC(3x3)ABCY (for a decompressed length of 18), because the decompressed data from the (8x2) marker (the (3x3)ABC) is skipped and not processed further.
assert decompress('X(8x2)(3x3)ABCY') == 'X(3x3)ABC(3x3)ABCY'


def read_input():
    with open("event2016/day09/input.txt") as f:
        ret = re.sub(r'\s+', '', f.read())

    return ret


answer = len(decompress(read_input()))
print("Part 1 =", answer)
assert answer == 99145 # check with accepted answer

########
# PART 2

def decompress_2(s):
    p = re.compile(r'\((\d+)x(\d+)\)')

    pos = 0

    todo = s
    done = 0
    while True:
        m = re.search(p, todo)

        if (m):
            dataSize = int(m.group(1))
            reps = int(m.group(2))

            data = todo[m.end():m.end() + dataSize]

            done += len(todo[:m.start()]) + (decompress_2(data) * reps)
            todo = todo[m.end() + dataSize:]

        else:
            done += len(todo)
            break

    return done

# (3x3)XYZ still becomes XYZXYZXYZ, as the decompressed section contains no markers.
assert decompress_2('(3x3)XYZ') == 9
# X(8x2)(3x3)ABCY becomes XABCABCABCABCABCABCY, because the decompressed data from the (8x2) marker is then further decompressed, thus triggering the (3x3) marker twice for a total of six ABC sequences.
assert decompress_2('X(8x2)(3x3)ABCY') == len('XABCABCABCABCABCABCY')
# (27x12)(20x12)(13x14)(7x10)(1x12)A decompresses into a string of A repeated 241920 times.
assert decompress_2('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 241920
# (25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN becomes 445 characters long.
assert decompress_2('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN') == 445

answer = decompress_2(read_input())
print("Part 2 =", answer)
assert answer == 10943094568 # check with accepted answer


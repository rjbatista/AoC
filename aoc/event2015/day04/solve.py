import hashlib

########
# PART 1

def find_md5_with_leading_zeros(pw, expected = 6, padding = 1):
    pwbytes = pw.encode('ascii')

    expectedBytes = "0" * expected
    

    while True:
        m = hashlib.md5(pwbytes + str(padding).encode('ascii'))

        if m.hexdigest()[:expected] == expectedBytes:
            break

        padding += 1

    return padding


inp = 'yzbqklnj'

answer_p1 = find_md5_with_leading_zeros(inp, 5)
print("Part 1 =", answer_p1)
assert answer_p1 == 282749 # check with accepted answer

########
# PART 2

answer = find_md5_with_leading_zeros(inp, 6, answer_p1)
print("Part 2 =", answer)
assert answer == 9962624 # check with accepted answer

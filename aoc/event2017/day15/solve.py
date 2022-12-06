""" Advent of code 2017 - day 15 """
""" implemented it first using generator, but it was slower than the iteractive version """

########
# PART 1

FACTOR_GEN_A = 16807
FACTOR_GEN_B = 48271
DIVISOR = 2147483647 # 0x7fffffff


def find_matches(v_a: int, v_b: int, rounds: int):
    """ find matches """

    total_count = 0
    for _ in range(rounds):
        v_a = (v_a * FACTOR_GEN_A) % DIVISOR
        v_b = (v_b * FACTOR_GEN_B) % DIVISOR

        if v_a & 0xFFFF == v_b & 0xFFFF:
            total_count += 1

    return total_count


assert find_matches(65, 8921, 5) == 1
#assert find_matches(65, 8921, 40000000) == 588

answer = find_matches(703, 516, 40000000)
print("Part 1 =", answer)
assert answer == 594 # check with accepted answer

########
# PART 2

def find_matches_p2(v_a: int, v_b: int, rounds: int):
    """ Find matches with multiples of 4 and 8 respectively """

    total_count = 0
    for _ in range(rounds):
        while True:
            v_a = (v_a * FACTOR_GEN_A) % DIVISOR

            if v_a & 0b11 == 0:
                break

        while True:
            v_b = (v_b * FACTOR_GEN_B) % DIVISOR

            if v_b & 0b111 == 0:
                break

        if v_a & 0xFFFF == v_b & 0xFFFF:
            total_count += 1

    return total_count


#assert find_matches_p2(65, 8921, 5000000) == 309

answer = find_matches_p2(703, 516, 5000000)
print("Part 2 =", answer)
assert answer == 328 # check with accepted answer

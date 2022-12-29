""" Advent of code 2022 - day 25 """
from pathlib import Path

########
# PART 1


SNAFU_SYMBOLS = '=-012'


def snafu2dec(snafu: str) -> int:
    """ Convert a number from snafu to decimal """
    number = 0
    for order, char in enumerate(reversed(snafu)):
        v = SNAFU_SYMBOLS.index(char) - 2

        number += v * (5 ** order)

    return number


def dec2snafu(number: int) -> str:
    """ Convert a number from decimal to snafu """
    snafu = []

    while number > 0:
        rem = (number % 5)
        number //= 5

        if rem <= 2:
            snafu += SNAFU_SYMBOLS[rem + 2]
        else:
            snafu += SNAFU_SYMBOLS[(rem - 5) + 2]
            number += 1

    return ''.join(reversed(snafu))


def read(filename: str) -> set:
    """ Read and sum a list of snafu numbers from file """
    path = Path(__file__).parent.joinpath(filename)
    with path.open("r", encoding="ascii") as file:
        return sum(snafu2dec(line.strip()) for line in file)


assert snafu2dec("1=-0-2") == 1747
assert snafu2dec("12111") == 906
assert snafu2dec("2=0=") == 198
assert snafu2dec("21") == 11
assert snafu2dec("2=01") == 201
assert snafu2dec("111") == 31
assert snafu2dec("20012") == 1257
assert snafu2dec("112") == 32
assert snafu2dec("1=-1=") == 353
assert snafu2dec("1-12") == 107
assert snafu2dec("12") == 7
assert snafu2dec("1=") == 3
assert snafu2dec("122") == 37

ex1 = read("example1.txt")
assert ex1 == 4890
assert dec2snafu(4890) == '2=-1=0'

ANSWER = dec2snafu(read("input.txt"))
print("Part 1 =", ANSWER)
assert ANSWER == '2=0=02-0----2-=02-10'  # check with accepted answer

""" Advent of code 2022 - day 20 """
from pathlib import Path

########
# PART 1

def read(filename: str) -> list:
    """ Read the file """
    with Path(__file__).parent.joinpath(filename).open("r", encoding="ascii") as file:
        return [int(line.strip()) for line in file]


def decrypt(number_list: list):
    """ Decrypt the number list """
    idx = 0
    number_list_state = [(number, False) for number in number_list]

    while idx < len(number_list):
        number, done = number_list_state[idx]

        end_idx = (idx + number) % (len(number_list) - 1)

        if not done:
            if idx != end_idx:
                number_list_state.insert(end_idx, (number_list_state.pop(idx)[0], True))
            else:
                number_list_state[idx] = (number, True)
                idx += 1
        else:
            idx += 1

    return [number for number, _ in number_list_state]


def find_grove_coordinates(number_list):
    """ Find the groove coordinates and sum them """

    decrypted_list = decrypt(number_list)
    idx = decrypted_list.index(0)
    list_len = len(decrypted_list)

    return sum((decrypted_list[(idx + n * 1000) % list_len] for n in range(1, 4)))


ex1 = read("example1.txt")
assert find_grove_coordinates(ex1) == 3

inp = read("input.txt")
ANSWER = find_grove_coordinates(inp)
print("Part 1 =", ANSWER)
assert ANSWER == 5904 # check with accepted answer

########
# PART 2

def decrypt_p2(number_list: list, decryption_key = 811589153, rounds = 10):
    """
    Decrypt the number list
    For one round wasn't necessary to keep the order, for more it is
    """
    number_list_order = [(idx, number * decryption_key) for idx, number in enumerate(number_list)]

    for _ in range(rounds):
        for cur_idx in range(len(number_list_order)):
            for pos, (elem_idx, elem_number) in enumerate(number_list_order):
                if cur_idx == elem_idx:
                    number = elem_number
                    idx = pos
                    break

            end_idx = (idx + number) % (len(number_list) - 1)

            if idx != end_idx:
                number_list_order.insert(end_idx, number_list_order.pop(idx))

    return [number for _, number in number_list_order]


def find_grove_coordinates_with_key(number_list):
    """ Find the groove coordinates and sum them """
    decrypted_list = decrypt_p2(number_list)
    idx = decrypted_list.index(0)
    list_len = len(decrypted_list)

    return sum((decrypted_list[(idx + n * 1000) % list_len] for n in range(1, 4)))


assert find_grove_coordinates_with_key(ex1) == 1623178306

ANSWER = find_grove_coordinates_with_key(inp)
print("Part 2 =", ANSWER)
assert ANSWER == 8332585833851 # check with accepted answer

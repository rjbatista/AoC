########
# PART 1

def get_numbers(initial_list):
    turn = 1
    last_number = None
    stored = {}
    while True:
        if turn <= len(initial_list):
            if last_number != None:
                stored[last_number] = turn - 1

            last_number = initial_list[turn - 1]
            yield last_number
        elif last_number in stored:
            next_number = turn - stored[last_number] - 1
            yield next_number

            stored[last_number] = turn - 1

            last_number = next_number
        else:
            stored[last_number] = turn - 1
            yield 0
            last_number = 0

        turn += 1


def get_after_rounds(list, rounds):
    numbers = get_numbers(list)
    for _ in range(rounds - 1):
        next(numbers)

    return next(numbers)


# example 1
numbers = get_numbers([0,3,6])
assert next(numbers) == 0
assert next(numbers) == 3
assert next(numbers) == 6
assert next(numbers) == 0
assert next(numbers) == 3
assert next(numbers) == 3
assert next(numbers) == 1
assert next(numbers) == 0
assert next(numbers) == 4
assert next(numbers) == 0
assert get_after_rounds([0,3,6], 2020) == 436 

# example 2
assert get_after_rounds([1,3,2], 2020) == 1
assert get_after_rounds([2,1,3], 2020) == 10
assert get_after_rounds([3,1,2], 2020) == 1836


answer = get_after_rounds([9,12,1,4,17,0,18], 2020)
print("Part 1 =", answer)
assert answer == 610 # check with accepted answer

########
# PART 2

answer = get_after_rounds([9,12,1,4,17,0,18], 30000000)
print("Part 2 =", answer)
assert answer == 1407

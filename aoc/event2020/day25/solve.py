def transform(subject_number = 7, times = 1):
    value = 1
    for _ in range(times):
        value = (value * subject_number) % 20201227

    return value


def figure_loop_size(public_key):
    value = 1
    loop_size = 1
    while True:
        value = (value * 7) % 20201227

        if value == public_key:
            break

        loop_size += 1
    
    return loop_size


public_keys = [5764801, 17807724]
loop_sizes = [figure_loop_size(key) for key in public_keys]
enc_key = [transform(*x) for x in zip(public_keys, reversed(loop_sizes))]
assert enc_key == [14897079, 14897079]


with open("event2020/day25/input.txt", "r") as file:
    public_keys = [int(x[:-1]) for x in file.readlines()]

loop_sizes = [figure_loop_size(key) for key in public_keys]
enc_key = [transform(*x) for x in zip(public_keys, reversed(loop_sizes))]
assert enc_key[0] == enc_key[1]
answer = enc_key[0]
print("Part 1 =", answer)
assert answer == 6421487 # check with accepted answer

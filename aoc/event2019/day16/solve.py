########
# PART 1
def get_numbers():
    numbers = None
    with open("event2019/day16/input.txt", "r") as file:
        for line in file:
            numbers = list(map(int, line[:-1]))
            #numbers = [int(x) for x in line[:-1]]
    
    return numbers

def fft(inp):
    ''' TODO: optimize with part 2 '''
    pattern = [0, 1, 0, -1]
    out = inp[:]
    for offset in range(len(inp)):
        out[offset] = abs(sum([digit * pattern[(1 + inner_offset) // (offset + 1) % 4] for inner_offset, digit in enumerate(inp)])) % 10
    
    return out

def repeat_fft(inp, count):
    for _ in range(count):
        inp = fft(inp)

    return inp

def get_answer(inp):
    return ''.join([str(x) for x in inp])[:8]

inp = [int(x) for x in "12345678"]
inp = fft(inp)
assert get_answer(inp) == "48226158"
inp = fft(inp)
assert get_answer(inp) == "34040438"
inp = fft(inp)
assert get_answer(inp) == "03415518"
inp = fft(inp)
assert get_answer(inp) == "01029498"

assert get_answer(repeat_fft(list(map(int, "80871224585914546619083218645595")), 100)) == "24176176"
assert get_answer(repeat_fft(list(map(int, "19617804207202209144916044189917")), 100)) == "73745418"
assert get_answer(repeat_fft(list(map(int, "69317163492948606335995924319873")), 100)) == "52432133"

numbers = get_numbers()
answer = get_answer(repeat_fft(numbers, 100)[:8])
print("Part 1 =", answer)
assert answer == "42945143" # check with accepted answer

########
# PART 2
def repeat_fft_p2(inp, count):
    offset = int(get_answer(inp)[:7])
    inp = inp * 10000
    inp_len = len(inp)

    for _ in range(count):
        acc = 0
        for j in range(inp_len - 1, offset - 1, -1):
            acc += inp[j]
            inp[j] = acc % 10
    
    return inp[offset : offset + 8]

assert get_answer(repeat_fft_p2(list(map(int, "03036732577212944063491565474664")), 100)) == "84462026"
assert get_answer(repeat_fft_p2(list(map(int, "02935109699940807407585447034323")), 100)) == "78725270"
assert get_answer(repeat_fft_p2(list(map(int, "03081770884921959731165446850517")), 100)) == "53553731"

answer = get_answer(repeat_fft_p2(numbers, 100))
print("Part 2 =", answer)
assert get_answer(answer) == "99974970" # check with accepted answer

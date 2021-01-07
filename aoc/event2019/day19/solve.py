from event2019.day13.computer_v4 import Computer_v4

########
# PART 1

computer = Computer_v4([])
computer.load_code("event2019/day19/input.txt")


def get_value(x, y):
    out = []
    computer.reload_code()
    computer.run([x, y], out)

    return out[0]


def get_area(side = 50):
    area = []
    min_x, width = 0, 0
    for y in range(side):
        row_min_x = None

        x = min_x
        # first '#'
        while True:
            val = get_value(x, y)
            
            if val != 1:
                x += 1
            else:
                row_min_x = x
                min_x = x
                break

            if x == side:
                break

        if row_min_x != None:
            # last '#'
            if width > 0:
                x += width - 1
            while True:
                val = get_value(x, y)
                
                if val == 1:
                    x += 1
                else:
                    width = x - row_min_x
                    break

                assert x != side

        area += [(row_min_x, width)]
    
    return area


answer = sum([width for x, width in get_area() if x != None])
print("Part 1 =", answer)
assert answer == 203 # check with accepted answer

########
# PART 2

def get_top_right_in_beam(square_size = 100):
    # skip ahead depending on square size
    x, y = (square_size * 5, square_size * 10)
    while True:
        if get_value(x, y) == 1:
            if get_value(x + square_size - 1, y - square_size + 1) == 1:  # True implies top_left and bottom_right
                return x, y - square_size + 1

            y += 1
        else:
            x += 1


x, y = get_top_right_in_beam()
answer = 10000 * x + y
print("Part 2 =", 10000 * x + y)
assert answer == 8771057 # check with accepted answer

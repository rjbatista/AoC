########
# PART 1
def get_layers(data, width = 25, height = 6):
    layers = []
    while data:
        layer = []
        for _ in range(width * height):
            layer.append(data.pop(0))
        layers.append(layer)
    return layers

def count_digit_on_layer(layer, digit):
    return sum([1 for val in layer if val == digit])

def get_layer_with_less_digit(layers, digit):
    totals = [count_digit_on_layer(layer, digit) for layer in layers]
    return layers[totals.index(min(totals))]

def get_check_digit(layer):
    return count_digit_on_layer(layer, 1) * count_digit_on_layer(layer, 2)

layers = get_layers([int(ch) for ch in "123456789012"], 3, 2)
assert get_check_digit(get_layer_with_less_digit(layers, 0)) == 1

layers = get_layers([int(ch) for ch in "123256789012"], 3, 2)
assert get_check_digit(get_layer_with_less_digit(layers, 0)) == 2

with open("event2019/day8/input.txt", "r") as input:
    data = [int(ch) for line in input for ch in line[:-1]]

layers = get_layers(data)
picked_layer = get_layer_with_less_digit(layers, 0)
answer = get_check_digit(get_layer_with_less_digit(layers, 0))

print("Part 1 =", answer)
assert answer == 1548 # check with accepted answer

########
# PART 2
def decode_image(layers, width = 25, height = 6):
    image = layers[0]
    for layer in layers[1:]:
        for i in range(width * height):
            image[i] = layer[i] if image[i] == 2 else image[i]

    for _ in range(height):
        for _ in range(width):
            ch = image.pop(0)
            print(' ' if ch == 0 else 'X', end = "")
        print()

layers = get_layers([int(ch) for ch in "0222112222120000"], 2, 2)
#decode_image(layers, 2, 2)

with open("event2019/day8/input.txt", "r") as input:
    data = [int(ch) for line in input for ch in line[:-1]]

layers = get_layers(data)
print("Part 2 =")
decode_image(layers)

#assert answer == 77500 # check with accepted answer

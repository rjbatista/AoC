import enum
from operator import mul
from functools import reduce
from event2020.day20.tiles import TileMap

########
# PART 1

tileMap = TileMap()
tileMap.read()

corner_ids = tileMap.corner_ids
answer = reduce(mul, map(int, corner_ids))
print("Part 1 =", answer)
assert answer == 29125888761511

########
# PART 2

def remove_monsters(data):
    mask = [
                            # 
        0b00000000000000000010,
          #    ##    ##    ###
        0b10000110000110000111,
           #  #  #  #  #  #   
        0b01001001001001001000
    ]
    found = False
    new_data = [0 for _ in data]
    for idx, row in enumerate(data[:-2]):
        val = row
        for col in range(96 - 20):
            if (val & mask[0]) == mask[0]:
                val2 = data[idx + 1] >> col
                if (val2 & mask[1]) == mask[1]:
                    val3 = data[idx + 2] >> col
                    if (val3 & mask[2]) == mask[2]:
                        found = True
                        new_data[idx] = new_data[idx] + (mask[0] << col)
                        new_data[idx + 1] = new_data[idx + 1] + (mask[1] << col)
                        new_data[idx + 2] = new_data[idx + 2] + (mask[2] << col)
            val >>= 1

    if found:
        for idx in range(len(data)):
            data[idx] ^= new_data[idx]

        return data
    else:
        return None


def remove_monsters_with_flips(data):
    data_without_monsters = remove_monsters(data)
    if not data_without_monsters:
        # try again flipping vertically
        data_without_monsters = remove_monsters(data[::-1])

        if not data_without_monsters:
            # try again flipping horizontally
            for idx, value in enumerate(data):
                data[idx] = sum([1 << idx for idx in range(96) if value & (1 << 95 - idx) > 0])

            data_without_monsters = remove_monsters(data)

            if not data_without_monsters:
                # try again flipping vertically
                data_without_monsters = remove_monsters(data[::-1])
    
    return data_without_monsters


data = remove_monsters_with_flips(tileMap.data)
answer = 0
for row in data:
    while row > 0:
        answer += row & 1
        row >>= 1

print("Part 2 =", answer)
assert answer == 2219


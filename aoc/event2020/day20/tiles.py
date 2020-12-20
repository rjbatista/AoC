import re

class Tile():
    """
    Tile class
    """
    def __init__(self, id, data):
        self.id = id
        self._data = data
        self._neighbours_by_key = {}
        self.neighbours = [None] * 4

        # get sides
        leftmost_bit = len(data) - 1
        top = data[0]
        bottom = data[-1]

        left = 0
        right = 0
        for x, y in [((x >> leftmost_bit) & 1, x & 1) for x in data]:
            left = (left << 1) + x
            right = (right << 1) + y

        self.sides = (top, right, bottom, left)


    def set_neighbour(self, side_key, neighbour):
        self._neighbours_by_key[side_key] = neighbour


    def get_neighbour(self, side):
        return self._neighbours_by_key.get(Tile.side_as_key(side), None)


    def is_corner(self):
        return len(self._neighbours_by_key.keys()) == 2


    def rotate(self):
        cols = len(self._data)
        new_data = [0] * cols
        for row in reversed(self._data):
            for idx in range(cols):
                new_data[idx] = (new_data[idx] << 1) + ((row >> (cols - 1 - idx)) & 1)

        self._data = new_data
        top, right, bottom, left = self.sides
        self.sides = Tile.flip_bits(left), top, Tile.flip_bits(right), bottom


    def flip_y(self):
        self._data = self._data[::-1]

        top, right, bottom, left = self.sides
        self.sides = bottom, Tile.flip_bits(right), top, Tile.flip_bits(left)


    def flip_x(self):
        for idx in range(len(self._data)):
            self._data[idx] = Tile.flip_bits(self._data[idx])

        top, right, bottom, left = self.sides
        self.sides = Tile.flip_bits(top), left, Tile.flip_bits(bottom), right


    def flip_bits(val):
        return sum([1 << idx for idx in range(10) if val & (1 << 9 - idx) > 0])


    def side_as_key(side):
        return tuple(sorted([side, Tile.flip_bits(side)]))


class TileMap:
    def __init__(self):
        self._tiles = {}
        self._corners = None


    def read(self):
        with open("event2020/day20/input.txt", "r") as file:
            pattern = re.compile(r"^Tile (\d+):$")

            # read "Tile XXXX:"
            for line in file:
                m = pattern.match(line)

                if not m:
                    raise RuntimeError("invalid input:" + line)

                tile_data = []
                for row in file:
                    row = row[:-1]

                    if not row:
                        break

                    tile_data.append(int(row.replace('.', '0').replace('#', '1'), 2))
                
                name = m.group(1)
                self._tiles[name] = Tile(name, tile_data)
        
        self.assemble()


    def assemble(self):
        tiles_by_side = {}
        for tile in self._tiles.values():
            for side in tile.sides:
                key = Tile.side_as_key(side)
                tiles_by_side[key] = tiles_by_side.get(key, []) + [tile]

        for side_key, tiles in tiles_by_side.items():
            assert len(tiles) <= 2

            if len(tiles) == 2:
                tiles[0].set_neighbour(side_key, tiles[1])
                tiles[1].set_neighbour(side_key, tiles[0])

        self._corners = [tile for tile in self._tiles.values() if tile.is_corner()]

        top_left = self._corners[0]
        if top_left.get_neighbour(top_left.sides[0]):
            top_left.flip_y()
        
        if top_left.get_neighbour(top_left.sides[-1]):
            top_left.flip_x()

        # fill rows
        cur = top_left
        while cur != None:
            left = cur
            while cur != None:
                right_side = cur.sides[1]
                right_neighbour = cur.get_neighbour(right_side)

                if not right_neighbour:
                    break

                while True:
                    left_side = right_neighbour.sides[-1]

                    if left_side == right_side:
                        break

                    if Tile.flip_bits(left_side) == right_side:
                        right_neighbour.flip_y()
                        break

                    right_neighbour.rotate()

                cur.neighbours[1] = right_neighbour
                right_neighbour.neighbours[-1] = cur
                cur = right_neighbour
            
            # get next line
            bottom_side = left.sides[2]
            bottom_neighbour = left.get_neighbour(bottom_side)

            if not bottom_neighbour:
                break

            while True:
                top_side = bottom_neighbour.sides[0]

                if top_side == bottom_side:
                    break

                if Tile.flip_bits(top_side) == bottom_side:
                    bottom_neighbour.flip_x()
                    break

                bottom_neighbour.rotate()

            left.neighbours[2] = bottom_neighbour
            bottom_neighbour.neighbours[0] = left
            cur = bottom_neighbour

    @property
    def corner_ids(self):
        return [tile.id for tile in self._corners]


    def print(self):
        cur = self._corners[0]

        while cur != None:
            left = cur

            rows = [""] * 10
            while cur != None:
                print(f"{cur.id:^10}", end=" ")
                for idx, line in enumerate(cur._data):
                    rows[idx] = rows[idx] + ''.join(['#' if line >> i & 1 == 1 else '.' for i in range(9, -1, -1)]) + " "

                cur = cur.neighbours[1]

            print()
            for row in rows:
                print(row)
            
            cur = left.neighbours[2]


    @property
    def data(self):
        cur = self._corners[0]

        total_rows = []
        while cur != None:
            left = cur

            rows = [0] * 8
            while cur != None:
                for idx, line in enumerate(cur._data[1:-1]):
                    rows[idx] = (rows[idx] << 8) + ((line >> 1) & 0xFF)

                cur = cur.neighbours[1]

            total_rows += rows

            cur = left.neighbours[2]
        
        return total_rows

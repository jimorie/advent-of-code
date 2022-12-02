import re

import util


class TileA:
    def __init__(self, data):
        self.tile_id = int(re.search("\\d+", data.pop(0)).group())
        self.borders = [
            data[0],
            "".join(line[-1] for line in data),
            data[-1],
            "".join(line[0] for line in data),
        ]
        self.neighbours = [None, None, None, None]

    def match_neighbour(self, other):
        for direction, b1 in enumerate(self.borders):
            for b2 in other.borders:
                if b1 == b2 or b1 == b2[::-1]:
                    self.neighbours[direction] = other
                    return True
        return False


def find_neighbours(tiles):
    for t1 in tiles:
        for t2 in tiles:
            if t1 is t2:
                continue
            t1.match_neighbour(t2)


def find_corners(tiles):
    return [tile for tile in tiles if sum(bool(n) for n in tile.neighbours) == 2]


def read_tiles(tile):
    return [tile(chunk.splitlines()) for chunk in util.readchunks()]


def day20a():
    tiles = read_tiles(TileA)
    find_neighbours(tiles)
    corners = find_corners(tiles)
    return util.prod(corner.tile_id for corner in corners)


if __name__ == "__main__":
    print(day20a())

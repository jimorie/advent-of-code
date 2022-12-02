import collections
import itertools
import re

from day20a import *


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3
MONSTER_PATTERNS = [
    re.compile("^..................#."),
    re.compile("^#....##....##....###"),
    re.compile("^.#..#..#..#..#..#..."),
]


class Image:
    def __init__(self, data):
        self.data = data

    def rotate(self):
        self.data = [
            "".join(line[i] for line in reversed(self.data))
            for i in range(len(self.data))
        ]

    def flipx(self):
        self.data = self.data[::-1]

    def flipy(self):
        self.data = [line[::-1] for line in self.data]

    def count_squares(self):
        return collections.Counter(itertools.chain.from_iterable(self.data))["#"]

    def count_monsters(self):
        monsters = 0
        for y in range(len(self.data) - len(MONSTER_PATTERNS) + 1):
            for x in range(len(self.data[y])):
                if all(
                    pattern.search(self.data[y + i][x:])
                    for i, pattern in enumerate(MONSTER_PATTERNS)
                ):
                    monsters += 1
        return monsters

    def count_most_monsters(self):
        monsters = 0
        for _ in range(3):
            monsters = max(monsters, self.count_monsters())
            self.flipy()
            monsters = max(monsters, self.count_monsters())
            self.flipx()
            monsters = max(monsters, self.count_monsters())
            self.flipy()
            monsters = max(monsters, self.count_monsters())
            self.flipx()  # Reset
            self.rotate()
        return monsters

    @classmethod
    def from_tiles(cls, tiles):
        dimension = int(len(tiles) ** 0.5)
        tile_dimension = len(tiles[0].image.data)
        data = [""] * dimension * tile_dimension
        for tile in sorted(tiles, key=lambda tile: tile.position):
            x, y = tile.position
            for i in range(tile_dimension):
                data[y * tile_dimension + i] += tile.image.data[i]
        return cls(data)


class TileB(TileA):
    def __init__(self, data):
        super().__init__(data)
        self.image = Image([line[1:-1] for line in data[1:-1]])
        self.position = None

    def rotate(self):
        # Rotate 90 degrees clockwise
        self.borders = [
            self.borders[WEST][::-1],
            self.borders[NORTH],
            self.borders[EAST][::-1],
            self.borders[SOUTH],
        ]
        self.neighbours = [
            self.neighbours[WEST],
            self.neighbours[NORTH],
            self.neighbours[EAST],
            self.neighbours[SOUTH],
        ]
        self.image.rotate()

    def flipx(self):
        # Flip along the x-axis
        self.borders = [
            self.borders[SOUTH],
            self.borders[EAST][::-1],
            self.borders[NORTH],
            self.borders[WEST][::-1],
        ]
        self.neighbours = [
            self.neighbours[SOUTH],
            self.neighbours[EAST],
            self.neighbours[NORTH],
            self.neighbours[WEST],
        ]
        self.image.flipx()

    def flipy(self):
        # Flip along the y-axis
        self.borders = [
            self.borders[NORTH][::-1],
            self.borders[WEST],
            self.borders[SOUTH][::-1],
            self.borders[EAST],
        ]
        self.neighbours = [
            self.neighbours[NORTH],
            self.neighbours[WEST],
            self.neighbours[SOUTH],
            self.neighbours[EAST],
        ]
        self.image.flipy()

    def align(self, neighbour, direction):
        border = neighbour.borders[direction]
        opposite_direction = (direction + 2) % 4
        for _ in range(3):
            if border == self.borders[opposite_direction]:
                return
            self.flipy()
            if border == self.borders[opposite_direction]:
                return
            self.flipx()
            if border == self.borders[opposite_direction]:
                return
            self.flipy()
            if border == self.borders[opposite_direction]:
                return
            self.flipx()  # Reset
            self.rotate()
        raise RuntimeError("Could not align")


def next_position(position, direction):
    x, y = position
    if direction == NORTH:
        y -= 1
    elif direction == EAST:
        x += 1
    elif direction == SOUTH:
        y += 1
    elif direction == WEST:
        x -= 1
    return (x, y)


def position_neighbours(tile):
    for direction, neighbour in enumerate(tile.neighbours):
        if neighbour and not neighbour.position:
            neighbour.position = next_position(tile.position, direction)
            neighbour.align(tile, direction)
            position_neighbours(neighbour)


def position_tiles(tiles):
    find_neighbours(tiles)
    # Pick any corner as our start tile
    start_tile = find_corners(tiles)[0]
    start_tile.position = (0, 0)
    while start_tile.neighbours[EAST] is None or start_tile.neighbours[SOUTH] is None:
        start_tile.rotate()
    position_neighbours(start_tile)


def day20b():
    tiles = read_tiles(TileB)
    position_tiles(tiles)
    image = Image.from_tiles(tiles)
    monsters = image.count_most_monsters()
    squares = image.count_squares()
    squars_per_monster = Image([p.pattern for p in MONSTER_PATTERNS]).count_squares()
    return squares - monsters * squars_per_monster


if __name__ == "__main__":
    print(day20b())

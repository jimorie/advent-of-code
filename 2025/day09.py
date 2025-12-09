from __future__ import annotations

import itertools

import util


def read_tiles() -> util.Generator[util.Position]:
    """Yield all red tile positions from the input."""
    for line in util.readlines():
        yield util.Position(*map(int, line.split(",")))


def square_area(a: util.Position, b: util.Position):
    """
    Return the area formed by drawing a square between `a` and `b` as opposing
    corners.
    """
    return (abs(a.x - b.x) + 1) * (abs(a.y - b.y) + 1)


def find_largest_square(tiles: list[util.Position]):
    """
    Return the largest square formed by using any pair of the red `tiles` as
    opposing corners.
    """
    return max(square_area(a, b) for a, b in itertools.combinations(tiles, 2))


def find_largest_red_green_square(tiles: list[util.Position]):
    """
    Return the largest square formed by using any pair of the red `tiles` as
    opposing corners, such that the square does not cross the polygon formed by
    the red `tiles`.
    """
    edges = [
        (min(a, b), max(a, b))
        for a, b in itertools.pairwise(itertools.chain(tiles, tiles[:1]))
    ]
    max_area = 0
    for a, b in itertools.combinations(tiles, 2):
        area = square_area(a, b)
        if area > max_area:
            # Check that this square does not cross any of the edges
            x1, x2 = min(a.x, b.x), max(a.x, b.x)
            y1, y2 = min(a.y, b.y), max(a.y, b.y)
            if not any(
                d.x > x1 and c.x < x2 and d.y > y1 and c.y < y2 for c, d in edges
            ):
                max_area = area
    return max_area


if __name__ == "__main__":
    tiles = list(read_tiles())
    print(find_largest_square(tiles))
    print(find_largest_red_green_square(tiles))

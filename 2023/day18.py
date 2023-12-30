from __future__ import annotations

import util


DIRS = {
    "R": util.Direction.EAST,
    "D": util.Direction.SOUTH,
    "L": util.Direction.WEST,
    "U": util.Direction.NORTH,
    "0": util.Direction.EAST,
    "1": util.Direction.SOUTH,
    "2": util.Direction.WEST,
    "3": util.Direction.NORTH,
}


def read_plan() -> util.Generator[tuple[util.Direction, int]]:
    """
    Yield a tuple with the direction and distance for each line in
    the input.
    """
    for line in util.readlines():
        dir, distance, _ = line.split()
        yield DIRS[dir], int(distance)


def read_plan_b() -> util.Generator[tuple[util.Direction, int]]:
    """
    Yield a tuple with the direction and distance for each line in
    the input.
    """
    for line in util.readlines():
        _, _, hex = line.split()
        yield DIRS[hex[7]], int(hex[2:7], 16)


def dig(
    plan: util.Generator[tuple[util.Direction, int]]
) -> util.Generator[util.Position]:
    """Yield all corner positions of the `plan`."""
    pos = util.Position(0, 0)
    yield pos
    for dir, distance in plan:
        pos += dir * distance
        yield pos


def area(corners: util.Generator[util.Position]) -> int:
    """
    Return the area enclosed by `corners`. Google Shoelace formula
    and Pick's theorem. :)
    """
    return (
        sum(
            a.x * b.y - a.y * b.x + abs(b.x - a.x + b.y - a.y)
            for a, b in util.pairwise(corners)
        )
        // 2
        + 1
    )


if __name__ == "__main__":
    print(area(dig(read_plan())))
    print(area(dig(read_plan_b())))

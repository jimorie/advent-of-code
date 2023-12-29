from __future__ import annotations

import collections
import itertools
import util


INTERACTIONS = {
    "/": {
        util.Direction.EAST: [util.Direction.NORTH],
        util.Direction.SOUTH: [util.Direction.WEST],
        util.Direction.WEST: [util.Direction.SOUTH],
        util.Direction.NORTH: [util.Direction.EAST],
    },
    "\\": {
        util.Direction.EAST: [util.Direction.SOUTH],
        util.Direction.SOUTH: [util.Direction.EAST],
        util.Direction.WEST: [util.Direction.NORTH],
        util.Direction.NORTH: [util.Direction.WEST],
    },
    "-": {
        util.Direction.EAST: [util.Direction.EAST],
        util.Direction.SOUTH: [util.Direction.EAST, util.Direction.WEST],
        util.Direction.WEST: [util.Direction.WEST],
        util.Direction.NORTH: [util.Direction.EAST, util.Direction.WEST],
    },
    "|": {
        util.Direction.EAST: [util.Direction.SOUTH, util.Direction.NORTH],
        util.Direction.SOUTH: [util.Direction.SOUTH],
        util.Direction.WEST: [util.Direction.SOUTH, util.Direction.NORTH],
        util.Direction.NORTH: [util.Direction.NORTH],
    },
}


def trace(grid: util.Grid, beam: tuple[util.Position, util.Direction]) -> int:
    """
    Trace a `beam` through the `grid` and return the number all
    positions it passes through.
    """
    beams: collections.deque[tuple[util.Position, util.Direction]] = collections.deque(
        [beam]
    )
    seen: dict[tuple[util.Position, util.Direction]] = collections.defaultdict(set)
    while beams:
        pos, dir = beams.popleft()
        if not grid.is_inside(pos):
            continue
        if pos in seen and dir in seen[pos]:
            continue
        seen[pos].add(dir)
        if pos in grid:
            for newdir in INTERACTIONS[grid[pos]][dir]:
                beams.append((pos + newdir, newdir))
        else:
            beams.append((pos + dir, dir))
    return len(seen)


def tracemax(grid: util.Grid) -> int:
    """
    Trace all possible beams starting from the edges of the `grid`
    and return the maximum number of positions passed through by any
    one beam.
    """
    beams = itertools.chain(
        ((util.Position(0, y), util.Direction.EAST) for y in range(grid.height)),
        ((util.Position(x, 0), util.Direction.SOUTH) for x in range(grid.width)),
        (
            (util.Position(grid.width - 1, y), util.Direction.WEST)
            for y in range(grid.height)
        ),
        (
            (util.Position(x, grid.height - 1), util.Direction.NORTH)
            for x in range(grid.width)
        ),
    )
    return max(trace(grid, beam) for beam in beams)


if __name__ == "__main__":
    grid = util.Grid.from_iterable(util.readlines(), ignore=".")
    beam = (util.Position(0, 0), util.Direction.EAST)
    print(trace(grid, beam))
    print(tracemax(grid))

from __future__ import annotations

import util


Pipes = dict[util.Position, tuple[util.Direction, util.Direction]]


PIPES: Pipes = {
    "|": (util.Direction.NORTH, util.Direction.SOUTH),
    "-": (util.Direction.EAST, util.Direction.WEST),
    "L": (util.Direction.NORTH, util.Direction.EAST),
    "J": (util.Direction.NORTH, util.Direction.WEST),
    "7": (util.Direction.SOUTH, util.Direction.WEST),
    "F": (util.Direction.SOUTH, util.Direction.EAST),
}


def read_pipes() -> tuple[Pipes, util.Position]:
    """
    Return a tuple with a dict of the positions of all pipes in the input,
    mapped to the direction of the exits they represent, and the starting
    position.
    """
    pipes = {}
    start = None
    for y, line in enumerate(util.readlines()):
        for x, c in enumerate(line):
            pos = util.Position(x, y)
            pipes[pos] = PIPES.get(c)
            if c == "S":
                start = pos
    # Fill in the exits for the start position
    start_exits = tuple()
    for dir in util.Direction.CARDINALS:
        exits = pipes.get(start + dir)
        if exits and dir.rotate(2) in exits:
            start_exits = start_exits + (dir,)
    pipes[start] = start_exits
    return pipes, start


def walk(pipes: Pipes, start: util.Position) -> set[util.Position]:
    """
    Walk the `pipes` from the `start` position and return the set of all
    positions included in the loop.
    """
    pos = start
    dir = None
    visited = {start}
    while True:
        for ex in pipes[pos]:
            if ex.rotate(2) != dir:  # don't go back
                pos += ex
                dir = ex
                visited.add(pos)
                break
        if pos == start:
            break
    return visited


def scan_inside(pipes: Pipes, visited: set[util.Position]) -> int:
    """
    Return the number of positions that is inside the `visited` loop. Do this
    by scanning the area row by row (the `pipes` insertion order) and note when
    we cross the `visited` loop (look for north and south exits, since we're
    heading east). An odd number of crossings means we're currently inside the
    loop.
    """
    pipes = iter(pipes.items())
    count = 0
    inside = False
    crossing = {
        util.Direction.NORTH,
        util.Direction.SOUTH,
    }
    for pos, exits in pipes:
        if pos in visited:
            if util.Direction.EAST in exits:
                combined = set(exits)
                for pos, exits in pipes:
                    if util.Direction.EAST not in exits:
                        combined.update(exits)
                        break
                if crossing.issubset(combined):
                    inside = not inside
            else:
                inside = not inside
        else:
            count += inside
    return count


if __name__ == "__main__":
    pipes, start = read_pipes()
    visited = walk(pipes, start)

    # The farthest distance is the middle of the loop.
    print(len(visited) // 2)

    # Scan the area for positions inside the loop.
    print(scan_inside(pipes, visited))

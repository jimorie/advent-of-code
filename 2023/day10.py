from __future__ import annotations

import collections
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
            if c == "S":
                start = util.Position(x, y)
            elif c in PIPES:
                pipes[util.Position(x, y)] = PIPES[c]
    # Fill in the exits for the start position
    start_exits = tuple()
    for dir in util.Direction.CARDINALS:
        exits = pipes.get(start + dir)
        if exits and dir.rotate(2) in exits:
            start_exits = start_exits + (dir,)
    pipes[start] = start_exits
    return pipes, start


def walk(pipes: Pipes, start: util.Position) -> list[util.Position]:
    """
    Walk the `pipes` from the `start` position and return a list of all
    positions included in the loop.
    """
    pos = start
    dir = None
    visited = [start]
    while True:
        for ex in pipes[pos]:
            if ex.rotate(2) != dir:  # don't go back
                pos += ex
                dir = ex
                visited.append(pos)
                break
        if pos == start:
            break
    return visited


def count_turns(visited: list[util.Position]) -> int:
    """
    Return the sum of all the turns in the `visited` loop, where a right turn
    equals +1 and a left turn -1.
    """
    return sum(
        dir_a.rotation(dir_b)
        for dir_a, dir_b in util.pairwise(
            pos_b - pos_a for pos_a, pos_b in util.pairwise(visited)
        )
    )


def spot_inner(visited: list[util.Position], inside: int) -> set[util.Position]:
    """
    Return a set of all the positions passed on the `inside` of the `visited`
    loop, expanded to include *all* inner position and not just those directly
    adjactent to the `visited` loop.
    """
    seen = set(visited)
    for pos_a, pos_b in util.pairwise(visited):
        dir = pos_b - pos_a
        dir = dir.rotate(inside)
        for pos in (pos_a + dir, pos_b + dir):
            floodfill(pos, seen)
    return seen.difference(visited)


def floodfill(pos: util.Position, seen: set[util.Position]):
    """
    Expand the set of `seen` position to include all positions accessible from
    `pos` without revisiting any `seen` positions (thus not breaking out of the
    inside of the loop).
    """
    queue = collections.deque()
    queue.append(pos)
    while queue:
        pos = queue.popleft()
        if pos not in seen:
            seen.add(pos)
            queue.extend(pos.neighbours)


if __name__ == "__main__":
    pipes, start = read_pipes()
    visited = walk(pipes, start)

    # The farthest distance is the middle of the loop.
    print(len(visited) // 2)

    # Figure out whether the inside of the loop is on the right or left side
    # when walking it.
    inside = 1 if count_turns(visited) > 0 else -1

    # Then walk the loop again and add up all positions accessible on the
    # inside of the loop.
    print(len(spot_inner(visited, inside)))

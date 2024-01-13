from __future__ import annotations

import heapq
import itertools
import util


def read_map() -> tuple[set[util.Position], util.Position]:
    """Return the map of garden plot positions and the start position."""
    map = set()
    for y, line in enumerate(util.readlines()):
        for x, c in enumerate(line):
            pos = util.Position(x, y)
            if c == ".":
                map.add(pos)
            if c == "S":
                map.add(pos)
                start = pos
    return map, start


def walk(
    map: set[util.Position], start: util.Position, size: int, yieldcheck: util.Callable
) -> util.Generator[int]:
    """
    Walk the `map` from `start` and yield the number of possible positions at
    certain points, as indicated by `yieldcheck`.
    """
    even, odd, seen = set(), set(), set()
    prev_step = 0
    queue = [(prev_step, start)]
    while queue:
        step, pos = heapq.heappop(queue)
        if pos in seen:
            continue
        seen.add(pos)
        if step != prev_step and yieldcheck(prev_step):
            yield len(odd if prev_step % 2 else even)
        prev_step, step = step, step + 1
        for neighbour in pos.cardinals:
            if (neighbour.x % size, neighbour.y % size) in map:
                if step % 2:
                    odd.add(neighbour)
                else:
                    even.add(neighbour)
                heapq.heappush(queue, (step, neighbour))


if __name__ == "__main__":
    map, start = read_map()
    size = max(pos.x for pos in map) + 1

    # Part 1
    print(next(walk(map, start, size, lambda step: step == 64)))

    # Part 2
    # Turns out that the problem input has some special properties that allow
    # us to interpolate the answer from three points. (Turns out is
    # circumbendus for I stole the idea from someone on Reddit.)
    steps = 26501365
    sizex2 = size * 2
    stepsmod = steps % sizex2
    a, b, c = itertools.islice(
        walk(map, start, size, lambda step: (step % sizex2) == stepsmod),
        3,
    )
    offset = b - a
    increment = (c - b) - (b - a)
    for _ in range(steps // sizex2):
        a += offset
        offset += increment
    print(a)

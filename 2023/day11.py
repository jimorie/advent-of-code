from __future__ import annotations

import itertools
import util


def read_universe(expansion: int = 2) -> set[util.Position]:
    """
    Return the set of galaxy positions in the expanded
    universe, as read from the input.
    """
    universe = {
        util.Position(x, y)
        for y, line in enumerate(util.readlines())
        for x, c in enumerate(line)
        if c == "#"
    }
    xs = {pos.x for pos in universe}
    ys = {pos.y for pos in universe}
    expanded = set()
    expansion -= 1
    for pos in universe:
        x_exp = sum(x not in xs for x in range(pos.x))
        y_exp = sum(y not in ys for y in range(pos.y))
        expanded.add(pos + (expansion * x_exp, expansion * y_exp))
    return expanded


def sum_distances(universe: set[util.Position]) -> int:
    """
    Return the sum of the distances between each galaxy in
    the expanded `universe`.
    """
    return sum(a.manhattan_distance(b) for a, b in itertools.combinations(universe, 2))


if __name__ == "__main__":
    print(sum_distances(read_universe(expansion=2)))
    print(sum_distances(read_universe(expansion=1000000)))

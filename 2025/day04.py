from __future__ import annotations

import collections

import util


def read_grid() -> util.Grid:
    """
    Return the input as a `Grid` (with the positions of the `@` characters).
    """
    return util.Grid.from_iterable(util.readlines(), ignore=".")


def get_adjacent_counts(grid: util.Grid) -> collections.Counter:
    """
    Return a counter with the number of adjacent `@` characters for each
    position in `Grid`.
    """
    counter = collections.Counter()
    for pos in grid:
        counter.update(pos.neighbours)
    return counter


def find_accessible(
    grid: util.Grid,
    max_adjacent: int,
    adjacent: collections.Counter | None = None,
) -> Generator[util.Position]:
    """
    Yield each `Position` in `Grid` that has fewer than `max_adjacent` `@`
    characters adjacent to it.
    """
    adjacent = adjacent or get_adjacent_counts(grid)
    for pos in grid:
        if adjacent[pos] < max_adjacent:
            yield pos


def remove_accessible(grid: util.Grid, max_adjacent: int) -> Generator[util.Position]:
    """
    Yield and remove each `Position` in `Grid` that has fewer than
    `max_adjacent` `@` characters adjacent to it. This is repeated until no
    more positions are accessible.
    """
    adjacent = get_adjacent_counts(grid)
    while True:
        found = list(find_accessible(grid, max_adjacent, adjacent=adjacent))
        if found:
            for pos in found:
                del grid[pos]
                adjacent.subtract(pos.neighbours)
                yield pos
        else:
            break


if __name__ == "__main__":
    grid = read_grid()
    print(sum(1 for _ in find_accessible(grid, 4)))
    print(sum(1 for _ in remove_accessible(grid, 4)))

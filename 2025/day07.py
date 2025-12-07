from __future__ import annotations

import collections

import util


def read_splitters() -> util.Grid:
    """Return a Grid with the positions of each splitter in the input."""
    return util.Grid.from_iterable(util.readlines(), ignore=".")


def trace_beams(splitters) -> tuple[int, int]:
    """
    Find the starting position and `S` and trace its progress while counting
    each split and timeline taken by the beam(s).
    """
    split_count = 0
    beams = {}
    # Find the start
    for pos, mark in splitters.items():
        if mark == "S":
            beams[pos.south] = 1
            break
    # Trace beams
    while beams:
        next = collections.defaultdict(int)
        for pos, count in beams.items():
            new = pos.south
            if new in splitters:  # Hit a splitter!
                # Increment the split count
                split_count += 1
                # Add up the number of paths (timelines) that arrive at the
                # split points
                next[new.west] += count
                next[new.east] += count
            elif splitters.is_inside(new):
                # Add up the number of paths (timelines) that arrive here
                next[new] += count
        if not next:
            return split_count, sum(beams.values())
        beams = next


if __name__ == "__main__":
    splitters = read_splitters()
    splits, timelines = trace_beams(splitters)
    print(splits)
    print(timelines)

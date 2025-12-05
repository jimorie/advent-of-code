from __future__ import annotations

import util


def read_input() -> tuple[list[range], Generator[int]]:
    """
    Return the input as a tuple with the parsed ranges and a generator for the
    ingredient IDs.
    """
    lines = util.readlines()
    ranges = []
    for line in lines:
        if not line:
            break
        start, end = line.split("-")
        ranges.append(range(int(start), int(end) + 1))
    return ranges, (int(line) for line in lines)


def normalize_ranges(ranges: list[range]) -> list[range]:
    """
    Normalize the `ranges` so that they cover the same ingredient IDs but
    without any overlap.
    """
    normalized = []
    next = None
    for r in sorted(ranges, key=lambda r: r.start):
        if next:
            if r.start > next.stop:
                normalized.append(next)
                next = r
            elif r.stop > next.stop:
                next = range(next.start, r.stop)
        else:
            next = r
    if next:
        normalized.append(next)
    return normalized


if __name__ == "__main__":
    ranges, ingredients = read_input()
    print(sum(1 for ingredient in ingredients if any(ingredient in r for r in ranges)))
    print(sum(len(r) for r in normalize_ranges(ranges)))

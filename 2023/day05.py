from __future__ import annotations

import collections
import itertools
import util


def read_input() -> util.Generator[tuple[list[int], dict]]:
    """
    Yield a list of seeds and a mapping of all category range translations from
    the input.
    """
    chunks = util.readchunks()
    seeds = [int(seed) for seed in next(chunks).removeprefix("seeds: ").split()]
    maps = collections.defaultdict(lambda: collections.defaultdict(dict))
    for chunk in chunks:
        header, *chunk = chunk.strip().split("\n")
        src_category, dst_category = header.removesuffix(" map:").split("-to-")
        for data in chunk:
            dst_number, src_number, size = (int(n) for n in data.split())
            src_range = range(src_number, src_number + size)
            dst_range = range(dst_number, dst_number + size)
            maps[src_category][dst_category][src_range] = dst_range
    return seeds, maps


def trace(
    maps: dict, current_category: str, current_range: range, find_category: str
) -> util.Generator[int]:
    """
    Yield the minimum value in all corresponding ranges after translating the
    `current_range` in the `current_category` to the `find_category`, according
    to the range translations in `maps`.
    """
    for next_category, map in maps[current_category].items():
        for src_range, dst_range in map.items():
            if current_range.start in src_range:
                next_start = current_range.start - src_range.start + dst_range.start
                if current_range.stop > src_range.stop:
                    # If the range we're tracing overshoot the matching range,
                    # we trace the remaining range as well.
                    yield from trace(
                        maps,
                        current_category,
                        range(src_range.stop, current_range.stop),
                        find_category,
                    )
                    next_range = range(next_start, dst_range.stop)
                else:
                    next_range = range(
                        next_start,
                        next_start + current_range.stop - current_range.start,
                    )
                break  # assuming no overlapping ranges
        else:
            next_range = current_range
        if next_category == find_category:
            yield next_range.start
        else:
            yield from trace(maps, next_category, next_range, find_category)


def tracemin(
    maps: dict, start_category: str, ranges: list[range], find_category: str
) -> int:
    """
    Return the minimum value in `ranges` after translating them from
    `start_category` to `find_category`.
    """
    return min(
        itertools.chain.from_iterable(
            trace(maps, start_category, r, find_category) for r in ranges
        )
    )


if __name__ == "__main__":
    seeds, maps = read_input()
    ranges = [range(seed, seed + 1) for seed in seeds]
    print(tracemin(maps, "seed", ranges, "location"))
    ranges = [range(start, start + size) for start, size in util.batched(seeds, 2)]
    print(tracemin(maps, "seed", ranges, "location"))

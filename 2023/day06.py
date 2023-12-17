from __future__ import annotations

import util


def read_races() -> util.Generator[tuple[int, int]]:
    """Yield each race as a tuple with the time and distance."""
    times, distances = util.read().strip().split("\n")
    times = (int(t) for t in times.split()[1:])
    distances = (int(d) for d in distances.split()[1:])
    yield from zip(times, distances)


def read_races_2() -> util.Generator[tuple[int, int]]:
    """Yield the only race as a tuple with the time and distance."""
    times, distances = util.read().strip().split("\n")
    time = int("".join(times.split()[1:]))
    distance = int("".join(distances.split()[1:]))
    yield time, distance


def to_beat(time: int, distance: int) -> int:
    """
    Return the difference between the lower and upper bound in the `time`
    range, where the winning `distance` is beat.
    """
    for start in range(1, time):
        if start * (time - start) > distance:
            break
    for stop in range(time - 1, start, -1):
        if stop * (time - stop) > distance:
            break
    return stop - start + 1


if __name__ == "__main__":
    print(util.prod(to_beat(time, distance) for time, distance in read_races()))
    print(util.prod(to_beat(time, distance) for time, distance in read_races_2()))

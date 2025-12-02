from __future__ import annotations

import util


DIALS = 100


def read_rotations() -> Generator[int]:
    """Yield all rotations in the input."""
    for line in util.readlines():
        yield (1 if line[0] == "R" else -1, int(line[1:]))


def turn_dial(pos: int) -> tuple[int, int]:
    """Turn the dial and count the zeroes."""
    stop_zero = 0
    pass_zero = 0
    for direction, count in read_rotations():
        # Flipping lets us avoid all the edge cases with going left!
        pos = (pos * direction) % DIALS
        # Turn the dial
        pos += count
        # Add up the number of times we pass 0
        pass_zero += pos // DIALS
        # Flip back to the correct position
        pos = (pos * direction) % DIALS
        # Add up the number of times we end on 0
        stop_zero += pos == 0
    return stop_zero, pass_zero


if __name__ == "__main__":
    setting = 50
    part_1, part_2 = turn_dial(setting)
    print(part_1)
    print(part_2)

from __future__ import annotations

import util


def trace_beams() -> tuple[int, int]:
    """
    Find the starting position and `S` and trace its progress while counting
    each split and timeline taken by the beam(s) in the input.
    """
    lines = util.readlines()
    line = next(lines)
    split_count = 0
    beams = [0] * len(line)
    beams[line.index("S")] = 1
    for line in lines:
        for i, c in enumerate(line):
            if beams[i] and c == "^":
                # Part 1
                split_count += 1

                # Part 2
                beams[i - 1] += beams[i]
                beams[i + 1] += beams[i]
                beams[i] = 0
    return split_count, sum(beams)


if __name__ == "__main__":
    split_count, timelines = trace_beams()
    print(split_count)
    print(timelines)

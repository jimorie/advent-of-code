import math
import itertools
import util


def read_input():
    return {
        util.Position(x, y)
        for y, line in enumerate(util.readlines())
        for x, c in enumerate(line)
        if c == "#"
    }


def spreadout(elves, start=0, end=None):
    viewfields = (
        (util.Direction.NORTH, util.Direction.NORTHEAST, util.Direction.NORTHWEST),
        (util.Direction.SOUTH, util.Direction.SOUTHEAST, util.Direction.SOUTHWEST),
        (util.Direction.WEST, util.Direction.NORTHWEST, util.Direction.SOUTHWEST),
        (util.Direction.EAST, util.Direction.NORTHEAST, util.Direction.SOUTHEAST),
    )
    for i in itertools.count(start):
        if end and i == end:
            break
        proposed = {}
        remain = set()
        for pos in elves:
            if not any(neighbour in elves for neighbour in pos.neighbours):
                remain.add(pos)
                continue
            for j in range(len(viewfields)):
                viewfield = viewfields[(i + j) % len(viewfields)]
                if not any(pos + direction in elves for direction in viewfield):
                    next_pos = pos + viewfield[0]
                    if next_pos in proposed:
                        remain.add(pos)
                        remain.add(proposed[next_pos])
                    else:
                        proposed[next_pos] = pos
                    break
            else:
                remain.add(pos)
        if not proposed:
            break
        elves = {next_pos for next_pos, pos in proposed.items() if pos not in remain}
        elves.update(remain)
    return elves, i + 1


def count_empty(elves):
    x_max = -math.inf
    y_max = -math.inf
    x_min = math.inf
    y_min = math.inf
    for x, y in elves:
        x_max = max(x_max, x)
        y_max = max(y_max, y)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
    return (x_max - x_min + 1) * (y_max - y_min + 1) - len(elves)


if __name__ == "__main__":
    elves = read_input()
    elves, _ = spreadout(elves, start=0, end=10)
    print(count_empty(elves))
    _, rounds = spreadout(elves, start=10, end=None)
    print(rounds)

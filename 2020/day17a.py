import collections
import itertools
import util


def parse(lines, *zw):
    return {
        (x, y, *zw)
        for y, line in enumerate(lines)
        for x, state in enumerate(line)
        if state == "#"
    }


def neighbours(crd):
    return (
        neighbour
        for neighbour in itertools.product(*((x - 1, x, x + 1) for x in crd))
        if neighbour != crd
    )


def cycle(blueprint):
    space = set()
    counts = collections.defaultdict(int)
    for crd in blueprint:
        for neighbour in neighbours(crd):
            counts[neighbour] += 1
    for crd in blueprint:
        if counts[crd] in (2, 3):
            space.add(crd)
        for neighbour in neighbours(crd):
            if neighbour not in blueprint and counts[neighbour] == 3:
                space.add(neighbour)
    return space


def cycles(lines, n, *zw):
    space = parse(lines, *zw)
    for _ in range(n):
        space = cycle(space)
    return len(space)


if __name__ == "__main__":
    print(cycles(util.readlines(), 6, 0))

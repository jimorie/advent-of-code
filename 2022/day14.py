import itertools
import util


def parse_rocks():
    grid = util.Grid()
    for line in util.readlines():
        p2 = None
        for p1 in parse_points(line):
            if p2:
                for pos in trace_line(p1, p2):
                    grid[pos] = "#"
            p2 = p1
    return grid


def parse_points(line):
    for point in line.split(" -> "):
        x, y = point.split(",")
        yield util.Position(int(x), int(y))


def trace_line(p1, p2):
    diff = p2 - p1
    direction = (
        diff.x // abs(diff.x) if diff.x else 0,
        diff.y // abs(diff.y) if diff.y else 0,
    )
    while p1 != p2:
        yield p1
        p1 += direction
    yield p2


def sandslide(grid, start):
    last_rock = max(y for _, y in grid)
    bottom = last_rock + 1
    part_1_done = False
    for sand_count in itertools.count(1):
        sand_pos = start
        while sand_pos.y < bottom:
            for direction in ((0, 1), (-1, 1), (1, 1)):
                next_pos = sand_pos + direction
                if next_pos not in grid:
                    sand_pos = next_pos
                    if sand_pos.y == last_rock and not part_1_done:  # Part 1 done
                        yield sand_count - 1
                        part_1_done = True
                    break
            else:
                break
        grid[sand_pos] = "o"
        if sand_pos == start:  # Part 2 done
            break
    yield sand_count


if __name__ == "__main__":
    grid = parse_rocks()
    start = util.Position(500, 0)
    for solution in sandslide(grid, start):
        print(solution)

import util


def read_grid():
    sensors = {}
    beacons = set()
    for line in util.readlines():
        sensor, beacon = parse_line(line)
        sensors[sensor] = sensor.manhattan_distance(beacon)
        beacons.add(beacon)
    return sensors, beacons


def parse_line(line):
    words = line.split()
    return (
        util.Position(int(words[2][2:-1]), int(words[3][2:-1])),
        util.Position(int(words[8][2:-1]), int(words[9][2:])),
    )


def y_coverage(y, sensors):
    for sensor, distance in sensors.items():
        y_diff = distance - abs(y - sensor.y)
        if y_diff >= 0:
            yield (sensor.x - y_diff, sensor.x + y_diff + 1)


def merged_y_coverage(y, sensors):
    coverage = sorted(y_coverage(y, sensors))
    if coverage:
        last_x1, last_x2 = coverage.pop(0)
        for x1, x2 in coverage:
            if x1 > last_x2:
                yield (last_x1, last_x2)
                last_x1 = x1
                last_x2 = x2
            last_x2 = max(x2, last_x2)
        yield (last_x1, last_x2)


def part_1(sensors, beacons, y):
    return sum(x2 - x1 for x1, x2 in merged_y_coverage(y, sensors)) - sum(
        beacon.y == y for beacon in beacons
    )


def part_2(sensors, beacons, min_xy, max_xy):
    for y in range(max_xy + 1):
        last_x2 = min_xy
        for x1, x2 in merged_y_coverage(y, sensors):
            if last_x2 < x1 and (x1 - 1, y) not in beacons:
                return (x1 - 1) * max_xy + y
            last_x2 = max(x2, last_x2)
    raise RuntimeError("No solution found")


if __name__ == "__main__":
    sensors, beacons = read_grid()
    print(part_1(sensors, beacons, 2000000))
    print(part_2(sensors, beacons, 0, 4000000))

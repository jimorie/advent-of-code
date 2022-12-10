import util

DIRECTIONS = {
    "U": (0, -1),
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
}


def parse_move(line):
    direction, steps = line.split()
    return (DIRECTIONS[direction], int(steps))


def follow(head, tail):
    diff = head - tail
    if abs(diff.x) > 1 or abs(diff.y) > 1:
        move = (
            diff.x // abs(diff.x) if diff.x else 0,
            diff.y // abs(diff.y) if diff.y else 0,
        )
        return tail + move
    return tail


def track_tail(knots=2):
    positions = [util.Position(0, 0)] * knots
    visits = set()
    for line in util.readlines():
        direction, steps = parse_move(line)
        for _ in range(steps):
            positions[0] += direction
            for i in range(1, len(positions)):
                positions[i] = follow(positions[i - 1], positions[i])
            visits.add(positions[i])
    return visits


if __name__ == "__main__":
    print(len(track_tail()))
    print(len(track_tail(10)))

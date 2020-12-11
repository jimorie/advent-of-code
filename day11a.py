import util


directions = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]


def count_adjacent(grid, x, y):
    return sum(grid.get((x + dx, y + dy)) == "#" for dx, dy in directions)


def change_seats(grid, copy, count_adjacent, occupied_threshold):
    changes = 0
    for crd, state in grid.items():
        adjacent = count_adjacent(grid, *crd)
        if state == "L" and adjacent == 0:
            copy[crd] = "#"
            changes += 1
        elif state == "#" and adjacent >= occupied_threshold:
            copy[crd] = "L"
            changes += 1
        else:
            copy[crd] = state
    return changes


def settle_seats(lines, count_adjacent=count_adjacent, occupied_threshold=4):
    grid = {
        (x, y): state
        for y, line in enumerate(lines)
        for x, state in enumerate(line)
        if state == "L"
    }
    copy = {}
    while change_seats(grid, copy, count_adjacent, occupied_threshold):
        grid, copy = copy, grid
    return sum(state == "#" for state in grid.values())


if __name__ == "__main__":
    print(settle_seats(util.readlines()))

import day11a
import util


def count_adjacent(grid, x, y):
    adjacent = 0
    for dx, dy in day11a.directions:
        length = 1
        while 0 <= x + dx * length < 100 and 0 <= y + dy * length < 100:
            state = grid.get((x + dx * length, y + dy * length))
            if state:
                adjacent += state == "#"
                break
            length += 1
    return adjacent


if __name__ == "__main__":
    print(
        day11a.settle_seats(
            util.readlines(), count_adjacent=count_adjacent, occupied_threshold=5
        )
    )

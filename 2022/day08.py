import util

ALL_DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def read_forest():
    return util.Grid([[int(c) for c in line] for line in util.readlines()])


def treeview(forest, position, direction):
    height = forest[position]
    count = 0
    while True:
        position += direction
        if not forest.is_inside(position):
            return count, True
        count += 1
        if height <= forest[position]:
            return count, False


def is_visible(forest, position):
    for direction in ALL_DIRECTIONS:
        _, edge = treeview(forest, position, direction)
        if edge:
            return True
    return False


def find_visible():
    forest = read_forest()
    return sum(is_visible(forest, position) for position in forest)


def find_scores():
    forest = read_forest()
    for position in forest.inner:
        score = 1
        for direction in ALL_DIRECTIONS:
            treecount, _ = treeview(forest, position, direction)
            score *= treecount
        yield score


if __name__ == "__main__":
    print(find_visible())
    print(max(find_scores()))
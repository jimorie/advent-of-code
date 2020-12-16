import util


def crd(grid, x, y):
    row = grid[y]
    return row[x % len(row)]


def treecount(grid, move_x, move_y):
    x = y = counter = 0
    while y < len(grid):
        if crd(grid, x, y) == "#":
            counter += 1
        x += move_x
        y += move_y
    return counter


if __name__ == "__main__":
    print(treecount(list(util.readlines()), 3, 1))

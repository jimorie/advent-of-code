import day03a
import util


def treecount_prod(grid, moves):
    return util.prod(day03a.treecount(grid, move_x, move_y) for move_x, move_y in moves)


if __name__ == "__main__":
    print(
        treecount_prod(
            list(util.readlines()),
            [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)],
        )
    )

import itertools
import util


class Rock(set):
    def __init__(self, chunk):
        self.update(
            (x, y)
            for y, line in enumerate(reversed(chunk.splitlines()))
            for x, c in enumerate(line)
            if c == "#"
        )
        self.width = max(x for x, _ in self) + 1 if self else 0

    def coverage(self, rock_pos):
        for pos in self:
            yield rock_pos + pos


ROCKS = [
    Rock(chunk)
    for chunk in """
####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##
""".split(
        "\n\n"
    )
]


def tetris(target_count=2022):
    grid = set()
    jetpattern = util.read().strip()
    rock_index = 0
    rock = ROCKS[rock_index]
    rock_pos = util.Position(2, 4)
    rock_count = 0
    rock_height = 0
    seen = {}  # Optimization for part 2
    for i in itertools.count():
        if jetpattern[i % len(jetpattern)] == "<":
            new_pos = rock_pos - (1, 0)
        if jetpattern[i % len(jetpattern)] == ">":
            new_pos = rock_pos + (1, 0)
        if all(
            pos.x >= 0 and pos.x < 7 and pos not in grid
            for pos in rock.coverage(new_pos)
        ):
            rock_pos = new_pos
        rock_pos -= (0, 1)
        if any(pos.y == 0 or pos in grid for pos in rock.coverage(rock_pos)):
            rock_pos += (0, 1)
            grid.update(rock.coverage(rock_pos))
            rock_height = max(rock_height, max(y for _, y in rock.coverage(rock_pos)))
            rock_count += 1
            if rock_count == target_count:
                break
            # For part 2, start looking for repetitions
            if rock_count > 2022:
                window = grid_window(grid, rock_height)
                key = (i % len(jetpattern), rock_index, window)
                if key in seen:
                    old_count, old_height = seen[key]
                    diff_count = rock_count - old_count
                    diff_height = rock_height - old_height
                    mult = (target_count - rock_count) // diff_count
                    rock_count += mult * diff_count
                    grid = {
                        (x, y + rock_height + mult * diff_height) for x, y in window
                    }
                    rock_height = max(y for _, y in grid)
                else:
                    seen[key] = rock_count, rock_height
            rock_index = (rock_index + 1) % len(ROCKS)
            rock = ROCKS[rock_index]
            rock_pos = util.Position(2, rock_height + 4)
    return rock_height


def grid_window(grid, top_y, size=25):  # Arbitrarily chosen size
    return frozenset((pos[0], pos[1] - top_y) for pos in grid if pos[1] >= top_y - size)


if __name__ == "__main__":
    print(tetris(2022))
    print(tetris(1000000000000))

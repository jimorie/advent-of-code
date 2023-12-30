from __future__ import annotations

import heapq
import util


def find_path(grid, start, stop, min_steps, max_steps):
    """
    Return the path from `start` to `stop` in `grid` that induces the least
    heat loss.
    """
    queue = [(0, 0, start, util.Direction.SOUTH), (0, 0, start, util.Direction.EAST)]
    seen = set()
    cycle = 0

    while queue:
        heatloss, _, pos, dir = heapq.heappop(queue)
        if pos == stop:
            return heatloss
        if (pos, dir) in seen:
            continue
        seen.add((pos, dir))
        for newdir in [dir.rotate(1), dir.rotate(-1)]:
            newheatloss = heatloss
            newpos = pos
            for step in range(1, max_steps + 1):
                newpos += newdir
                if newpos not in grid:
                    break
                newheatloss += grid[newpos]
                if step < min_steps:
                    continue
                cycle += 1
                heapq.heappush(queue, (newheatloss, cycle, newpos, newdir))


if __name__ == "__main__":
    grid = util.Grid.from_iterable(util.readlines(), cast=int)
    start = min(grid)
    stop = max(grid)
    print(find_path(grid, start, stop, 1, 3))
    print(find_path(grid, start, stop, 4, 10))

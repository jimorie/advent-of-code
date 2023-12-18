from __future__ import annotations

import math
import itertools
import util


def read_maps() -> tuple[util.Iterable[int], dict[str, tuple[str, str]]]:
    """
    Return a tuple with the directions and map from the input. The directions
    are returned as a cyclic loop of integers with 0 for left and 1 for right
    (to be used as indexes on the map values).
    """
    lines = util.readlines()
    directions = itertools.cycle(int(direction == "R") for direction in next(lines))
    next(lines)  # skip blank line
    map = {}
    for line in lines:
        node, _, left, right = (item.strip("(),") for item in line.split())
        map[node] = (left, right)
    return directions, map


def count_steps(
    directions: util.Iterable[int],
    map: dict[str, tuple[str, str]],
    node: str,
    goalcheck: util.Callable[[str], bool],
) -> int:
    """
    Walk the `map`, starting from `node` and following the `directions` until
    the `goalcheck` is satisfied. Return the number of steps taken.
    """
    for count, direction in enumerate(directions, 1):
        node = map[node][direction]
        if goalcheck(node):
            return count


if __name__ == "__main__":
    directions, map = read_maps()

    # For part 1 just count the number of steps from "AAA" to "ZZZ".
    goalcheck = lambda node: node == "ZZZ"
    print(count_steps(directions, map, "AAA", goalcheck))

    # For part 2 we observe that it is enough to count the number of steps of
    # each path individually, and that the number of steps needed to satisfy
    # all the scenarios simultaneously is their least common multiple.
    nodes = [node for node in map if node.endswith("A")]
    goalcheck = lambda node: node.endswith("Z")
    steps = [count_steps(directions, map, node, goalcheck) for node in nodes]
    print(math.lcm(*steps))

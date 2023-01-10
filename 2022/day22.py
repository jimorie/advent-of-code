import functools
import math
import re
import util


DIRS = util.Direction.CARDINALS
EAST, SOUTH, WEST, NORTH = DIRS

# CORNERS represent the 8 corners of a cube as a tuple of integers. First
# integer (0) represent the north-west-upper corner, second (1) the
# north-east-upper, third (2) the south-east-upper, fourth (3) the
# south-west-upper, and then repeated for the four lower corners.
CORNERS = tuple(range(8))
NWU, NEU, SEU, SWU, NWD, NED, SED, SWD = CORNERS

# ROTATIONS describe how a corner tuple change when we rotate the cube to
# bring another face to the top. E.g. EAST means rotating the cube left, to
# bring the east face to the top.
ROTATIONS = {
    EAST: (NEU, NED, SED, SEU, NWU, NWD, SWD, SWU),
    SOUTH: (SWU, SEU, SED, SWD, NWU, NEU, NED, NWD),
    WEST: (NWD, NWU, SWU, SWD, NED, NEU, SEU, SED),
    NORTH: (NWD, NED, NEU, NWU, SWD, SED, SEU, SWU),
}


def read_input():
    grid, path = util.readchunks()
    grid = {
        util.Position(x, y): c
        for y, line in enumerate(grid.splitlines())
        for x, c in enumerate(line)
        if c != " "
    }
    path = [x if x in "RL" else int(x) for x in re.split(r"([RL])", path)]
    return grid, path


def walk(grid, path, start, wrapper):
    pos = start
    direction = EAST
    for action in path:
        if action == "L":
            direction = direction.rotate(-1)
        elif action == "R":
            direction = direction.rotate(1)
        else:
            for _ in range(action):
                next_pos = pos + direction
                next_direction = direction
                c = grid.get(next_pos)
                if c is None:
                    next_pos, next_direction = wrapper(pos, direction)
                    c = grid.get(next_pos)
                if c == "#":
                    break
                pos = next_pos
                direction = next_direction
    return (pos.y + 1) * 1000 + (pos.x + 1) * 4 + DIRS.index(direction)


def wrapper_p1(pos, direction):
    if direction == EAST:
        return min(p for p in grid if p.y == pos.y), direction
    if direction == SOUTH:
        return min(p for p in grid if p.x == pos.x), direction
    if direction == WEST:
        return max(p for p in grid if p.y == pos.y), direction
    if direction == NORTH:
        return max(p for p in grid if p.x == pos.x), direction


def wrapper_p2(grid, size, pos, direction):
    # Find the four corners of the face we want to go to, as if the map had
    # extended in that direction.
    target_corners = rotate_corners(CORNERS, direction)[:4]
    # Explore the given map using BFS and rotate our corners to keep the
    # current face on "top" as we go.
    seen = set()
    explore = [(pos, CORNERS)]
    while explore:
        pos, corners = explore.pop(0)
        # The four first corners are those of the current "top" face, if the
        # set of them match the ones we are looking for we've found the
        # correct section of the map.
        if all(corners.index(corner) < 4 for corner in target_corners):
            break
        # Don't go in circles.
        if pos in seen:
            continue
        seen.add(pos)
        # Explore every direction from here that is present on the map.
        for explore_dir in DIRS:
            next_pos = pos + explore_dir * size
            if next_pos in grid:
                explore.append((next_pos, rotate_corners(corners, explore_dir)))
    # Calculate the relative x, y co-ordinate for this section of the map.
    x = pos.x % size
    y = pos.y % size
    topleft_pos = pos - (x, y)
    # Find the rotation of the top four corners that exactly matches the
    # order of the corners as found when rotating directly to the face.
    for rotation in range(4):
        top_corners = corners[rotation:4] + corners[:rotation]
        if top_corners == target_corners:
            break
        # Rotate the x, y co-ordinates.
        x, y = size - y - 1, x
    # Rotate the new direction to match.
    next_direction = direction.rotate(rotation)
    # Mirror x or y co-ordinate to the correct edge.
    if next_direction == EAST:
        x = 0
    elif next_direction == SOUTH:
        y = 0
    elif next_direction == WEST:
        x = size - 1
    else:
        y = size - 1
    # We're done!
    return topleft_pos + (x, y), next_direction


def rotate_corners(corners, direction):
    return tuple(corners[i] for i in ROTATIONS[direction])


if __name__ == "__main__":
    grid, path = read_input()
    start = min(p for p in grid if p.y == 0)
    # Part 1
    print(walk(grid, path, start, wrapper_p1))
    # Part 2
    size = int(math.sqrt(len(grid) // 6))
    print(walk(grid, path, start, functools.partial(wrapper_p2, grid, size)))

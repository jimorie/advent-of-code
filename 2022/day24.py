import collections
import heapq
import math
import util


def read_input():
    blizzards_x = collections.defaultdict(list)
    blizzards_y = collections.defaultdict(list)
    start = goal = None
    for y, line in enumerate(util.readlines(), -1):
        for x, c in enumerate(line, -1):
            pos = util.Position(x, y)
            if c == ">":
                blizzards_x[pos.y].append((pos, util.Direction.EAST))
            elif c == "v":
                blizzards_y[pos.x].append((pos, util.Direction.SOUTH))
            elif c == "<":
                blizzards_x[pos.y].append((pos, util.Direction.WEST))
            elif c == "^":
                blizzards_y[pos.x].append((pos, util.Direction.NORTH))
            elif c == "." and y < 0:
                start = pos
            elif c == ".":
                goal = pos
    return x, y, start, goal, (blizzards_x, blizzards_y)


def snowjog(width, height, start, goal, blizzards, minute=0):
    # Find the shortest path from start to goal using a prioritized queue,
    # exploring the most promising paths first and cutting of hopeless paths.
    explore = [(start.manhattan_distance(goal), minute, start)]
    heapq.heapify(explore)
    seen = set()
    best = math.inf
    while explore:
        distance, minute, pos = heapq.heappop(explore)
        # Abort if we can't beat the best time
        if distance + minute >= best:
            continue
        # Abort if we've been in this situation before
        key = (pos, minute % width, minute % height)
        if key in seen:
            continue
        else:
            seen.add(key)
        # Abort if we find ourselves in a blizzard
        if in_blizzard(pos, minute, blizzards):
            continue
        # Let time pass
        minute += 1
        # Can we reach the goal from here?
        if distance == 1:
            best = min(best, minute)
            continue
        # Otherwise keep on moving!
        for next_pos in pos.cardinals:
            if 0 <= next_pos.x < width and 0 <= next_pos.y < height:
                heapq.heappush(
                    explore,
                    (next_pos.manhattan_distance(goal), minute, next_pos),
                )
        # Or wait a minute...
        heapq.heappush(explore, (pos.manhattan_distance(goal), minute, pos))
    return best


def in_blizzard(pos, minute, blizzards):
    blizzards_x, blizzards_y = blizzards
    for blizzard_pos, blizzard_dir in blizzards_x[pos.y]:
        if (blizzard_pos.x + blizzard_dir.x * minute) % width == pos.x:
            return True
    for blizzard_pos, blizzard_dir in blizzards_y[pos.x]:
        if (blizzard_pos.y + blizzard_dir.y * minute) % height == pos.y:
            return True
    return False


if __name__ == "__main__":
    width, height, start, goal, blizzards = read_input()
    trip_1 = snowjog(width, height, start, goal, blizzards, minute=0)
    print(trip_1)
    trip_2 = snowjog(width, height, goal, start, blizzards, minute=trip_1)
    trip_3 = snowjog(width, height, start, goal, blizzards, minute=trip_2)
    print(trip_3)

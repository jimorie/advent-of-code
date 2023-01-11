import collections
import util


def read_input():
    blizzards = []
    start = None
    for y, line in enumerate(util.readlines(), -1):
        for x, c in enumerate(line, -1):
            pos = util.Position(x, y)
            if c == ">":
                blizzards.append((pos, util.Direction.EAST))
            elif c == "v":
                blizzards.append((pos, util.Direction.SOUTH))
            elif c == "<":
                blizzards.append((pos, util.Direction.WEST))
            elif c == "^":
                blizzards.append((pos, util.Direction.NORTH))
            elif c == "." and y < 0:
                start = pos
            elif c == ".":
                goal = pos
    return x, y, start, goal, blizzards


def snowjog(width, height, start, goal, blizzards, minute=0):
    # Simple BFS for the first path found
    explore = collections.deque([(minute, start)])
    seen = set()
    while explore:
        minute, pos = explore.popleft()
        # Abort if we've been in this situation before
        key = (pos, minute % width, minute % height)
        if key in seen:
            continue
        seen.add(key)
        # Abort if we find ourselves in a blizzard
        for blizzard_pos, blizzard_dir in blizzards:
            if blizzard_dir.x:
                if blizzard_pos.y != pos.y:
                    continue
                if (blizzard_pos.x + blizzard_dir.x * minute) % width == pos.x:
                    break
            elif blizzard_dir.y:
                if blizzard_pos.x != pos.x:
                    continue
                if (blizzard_pos.y + blizzard_dir.y * minute) % height == pos.y:
                    break
        else:
            # Let time pass
            minute += 1
            # Can we reach the goal from here?
            if abs(pos.x - goal.x) + abs(pos.y - goal.y) == 1:
                return minute
            # Otherwise keep on moving!
            for next_pos in pos.cardinals:
                if 0 <= next_pos.x < width and 0 <= next_pos.y < height:
                    explore.append((minute, next_pos))
            # Or wait a minute...
            explore.append((minute, pos))


if __name__ == "__main__":
    width, height, start, goal, blizzards = read_input()
    trip_1 = snowjog(width, height, start, goal, blizzards, minute=0)
    print(trip_1)
    trip_2 = snowjog(width, height, goal, start, blizzards, minute=trip_1)
    trip_3 = snowjog(width, height, start, goal, blizzards, minute=trip_2)
    print(trip_3)

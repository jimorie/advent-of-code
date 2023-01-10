import util


def read_heightmap():
    heightmap = util.Grid.from_iterable(util.readlines(), ord)
    start = heightmap.index(ord("S"))
    end = heightmap.index(ord("E"))
    heightmap[start] = ord("a")
    heightmap[end] = ord("z")
    return heightmap, start, end


def explore_distances(heightmap, start):
    explore = [start]
    distances = {start: 0}
    while explore:
        pos = explore.pop(0)
        distance = distances[pos] + 1
        for next_pos in pos.cardinals:
            if next_pos not in heightmap:
                # Outside the map
                continue
            if heightmap[pos] - heightmap[next_pos] > 1:
                # Too steep to climb
                continue
            if next_pos in distances:
                # Been there (shorter or equal distance implied)
                continue
            # Mark distance and continue exploration later
            distances[next_pos] = distance
            explore.append(next_pos)
    return distances


if __name__ == "__main__":
    heightmap, start, end = read_heightmap()
    distances = explore_distances(heightmap, end)
    print(distances[start])
    print(
        min(
            distances[pos]
            for pos, height in heightmap.items()
            if height == ord("a") and pos in distances
        )
    )

import util


def read_heightmap():
    heightmap = util.Grid([[ord(c) for c in line] for line in util.readlines()])
    start = end = None
    # Find and replace start and positions
    for pos, height in heightmap.items():
        if height == ord("S"):
            heightmap[pos] = ord("a")
            start = pos
            if end:
                break
        if height == ord("E"):
            heightmap[pos] = ord("z")
            end = pos
            if start:
                break
    return heightmap, start, end


def trek_to_the_end(heightmap, start, end):
    explore = [(start, 0)]
    seen = {start}
    while explore:
        pos, steps = explore.pop(0)
        steps += 1
        for next_pos in pos.cardinals:
            if next_pos not in heightmap:
                # Outside the map
                continue
            if heightmap[next_pos] - heightmap[pos] > 1:
                # Too high to climb
                continue
            if next_pos == end:
                # We found it!
                return steps
            if next_pos in seen:
                # Been there
                continue
            # Explore it later
            seen.add(next_pos)
            explore.append((next_pos, steps))
    raise RuntimeError("No path found")


def best_trek_to_the_end(heightmap, end):
    # TODO: Cache the successful paths to speed up repeated searches
    best_trek = None
    for pos, height in heightmap.items():
        if height == ord("a"):
            try:
                this_trek = trek_to_the_end(heightmap, pos, end)
                best_trek = min(best_trek, this_trek) if best_trek else this_trek
            except RuntimeError:
                pass
    return best_trek


if __name__ == "__main__":
    heightmap, start, end = read_heightmap()
    print(trek_to_the_end(heightmap, start, end))
    print(best_trek_to_the_end(heightmap, end))

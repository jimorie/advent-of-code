import util


def read_cubes():
    return {util.Position(*map(int, line.split(","))) for line in util.readlines()}


def can_escape(start, cubes, known):
    mins = [min(pos[i] for pos in cubes) for i in range(len(start))]
    maxs = [max(pos[i] for pos in cubes) for i in range(len(start))]
    queue = [start]
    seen = {start}
    verdict = False
    while queue:
        pos = queue.pop()
        if pos in known:
            verdict = known[pos]
            break
        if any(a1 <= a2 for a1, a2 in zip(pos, mins)) or any(
            a1 >= a2 for a1, a2 in zip(pos, maxs)
        ):
            verdict = True
            break
        seen.add(pos)
        queue.extend(
            next_pos
            for next_pos in pos.neighbours_3d
            if next_pos not in seen and next_pos not in cubes
        )
    known.update((pos, verdict) for pos in seen)
    return verdict


if __name__ == "__main__":
    cubes = read_cubes()
    print(
        sum(
            sum(neighbour not in cubes for neighbour in cube.neighbours_3d)
            for cube in cubes
        )
    )
    known = {}
    print(
        sum(
            sum(
                neighbour not in cubes and can_escape(neighbour, cubes, known)
                for neighbour in cube.neighbours_3d
            )
            for cube in cubes
        )
    )

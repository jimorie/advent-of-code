import functools
import itertools
import re
import util

LINE_PATTERN = re.compile(
    r"^Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (.*)$"
)


def read_valves():
    valves = {}
    for line in util.readlines():
        match = LINE_PATTERN.match(line)
        valves[match.group(1)] = (
            int(match.group(2)),
            match.group(3).split(", "),
        )
    return valves


@functools.cache
def find_path(positions, time, opened):
    if time <= 0:
        return 0
    flow = 0
    all_moves = []
    for position, previous_position in positions:
        flowrate, tunnels = valves[position]
        pos_moves = [
            (tunnel, position)
            for tunnel in tunnels
            # Optimization: Don't go back unless it's the only path
            if len(tunnels) == 1 or tunnel != previous_position
        ]
        if flowrate and position not in opened:
            if position == previous_position:
                flow += flowrate * time
                opened |= {position}
            else:
                pos_moves.append((position, position))
        all_moves.append(pos_moves)
    time -= 1
    # Optimization: End early if all valves are opened
    if len(opened) == valvecount:
        return flow
    # Optimization: Split moves if both positions are the same
    if len(positions) == 2 and positions[0] == positions[1]:
        all_moves[1] = all_moves[0][len(all_moves[0]) // 2 :]
        all_moves[0] = all_moves[0][: len(all_moves[0]) // 2]
    return flow + max(
        (
            find_path(tuple(sorted(move)), time, opened)
            for move in itertools.product(*all_moves)
        ),
        default=0,
    )


if __name__ == "__main__":
    global valves, valvecount
    valves = read_valves()
    valvecount = sum(flowrate > 0 for flowrate, _ in valves.values())
    start = "AA"
    print(find_path(((start, False),), 30, frozenset()))
    print(find_path(((start, False), (start, False)), 26, frozenset()))

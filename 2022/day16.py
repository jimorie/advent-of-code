import collections
import heapq
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


def open_valves(time, positions, valves):
    valvecount = sum(flowrate > 0 for flowrate, _ in valves.values())
    queue = [(0, (0, time, positions, frozenset()))]
    heapq.heapify(queue)
    seen = collections.defaultdict(dict)
    best = 0
    while queue:
        _, state = heapq.heappop(queue)
        flow, time, positions, opened = state
        # Optimization: End early if we've seen better flow at comparable state before
        if has_seen_better(seen, flow, time, positions):
            continue
        else:
            seen[positions][time] = flow
        # Find all available moves for each of our positions
        all_moves = []
        for position, previous_position in positions:
            flowrate, tunnels = valves[position]
            # Add all tunnels out of here as possible moves
            pos_moves = [
                (tunnel, position)
                for tunnel in tunnels
                # Optimization: Don't go back unless it's the only path
                if len(tunnels) == 1 or tunnel != previous_position
            ]
            # Is this a valve we want to open?
            if flowrate and position not in opened:
                if position == previous_position:
                    # If we didn't move, we open it now
                    flow += flowrate * time
                    opened |= {position}
                    best = max(best, flow)
                else:
                    # Otherwise consider not moving so we can open it later
                    pos_moves.append((position, position))
            all_moves.append(pos_moves)
        time -= 1
        if time <= 1:
            continue
        # Optimization: End early if all valves are opened
        if len(opened) == valvecount:
            continue
        # Optimization: End early if we can't beat the best flow
        max_flow = flow + sum(
            flowrate * time
            for position, (flowrate, _) in valves.items()
            if position not in opened
        )
        if max_flow <= best:
            continue
        # Optimization (part 2): Split moves if both positions are the same
        if len(positions) == 2 and positions[0] == positions[1]:
            all_moves[1] = all_moves[0][len(all_moves[0]) // 2 :]
            all_moves[0] = all_moves[0][: len(all_moves[0]) // 2]
        # Push all combinations of moves to be explored
        for move in itertools.product(*all_moves):
            # Calculate a prio based on how promising our state is. (The sooner
            # we can find a good result, the sooner we can start pruning off
            # poor paths.)
            prio = time * 100 + flow
            heapq.heappush(queue, (-prio, (flow, time, tuple(sorted(move)), opened)))
    return best


def has_seen_better(seen, flow, time, positions):
    if positions in seen:
        for seen_time, seen_flow in seen[positions].items():
            if seen_flow >= flow and seen_time >= time:
                return True
    return False


if __name__ == "__main__":
    valves = read_valves()
    start = "AA"
    print(open_valves(30, ((start, None),), valves))
    print(
        open_valves(
            26,
            (
                (start, None),
                (start, None),
            ),
            valves,
        )
    )

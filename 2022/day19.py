import collections
import re
import util

BLUEPRINT_PATTERN = re.compile(
    r"^Blueprint (\d+): Each ore robot costs (.*?)\. Each clay robot costs (.*?)\. Each obsidian robot costs (.*?)\. Each geode robot costs (.*?)\.$"
)
COST_PATTERN = re.compile(r"(\d+) (ore|clay|obsidian)")
NEW_ROBOTS = [(1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]


def read_blueprints():
    return [parse_blueprint(line) for line in util.readlines()]


def parse_blueprint(line):
    match = BLUEPRINT_PATTERN.match(line)
    return (
        int(match.group(1)),  # Blueprint ID
        (
            parse_cost(match.group(5)),  # Geode robot cost
            parse_cost(match.group(4)),  # Obsidian robot cost
            parse_cost(match.group(3)),  # Clay robot cost
            parse_cost(match.group(2)),  # Ore robot cost
        ),
    )


def parse_cost(cost):
    resources = {
        material: int(amount) for amount, material in COST_PATTERN.findall(cost)
    }
    return util.Vector(
        0,  # Geodes are never a cost
        resources.get("obsidian", 0),
        resources.get("clay", 0),
        resources.get("ore", 0),
    )


def dig(costs, state):
    max_costs = tuple(max(t) for t in zip(*costs))
    queue = collections.deque([state])
    seen = set()
    geodes = 0
    while queue:
        state = queue.popleft()
        # Abort on repeating states
        if state in seen:
            continue
        seen.add(state)
        # Check our resources
        time, resources, robots = state
        geodes = max(geodes, resources[0])
        if time == 0:
            continue
        # Buy robots!
        for i, cost in enumerate(costs):
            # Do we have enough of this robot already?
            if max_costs[i] and (
                resources[i] >= max_costs[i] * time - robots[i] * (time - 1)
            ):
                continue
            # Can we afford this robot?
            if all(x >= y for x, y in zip(resources, cost)):
                queue.append(
                    (
                        time - 1,
                        resources - cost + robots,
                        robots + NEW_ROBOTS[i],
                    )
                )
                if i == 0:
                    # If we can buy a geode robot, that must be the best!
                    break
                if i == 1:
                    # If we can buy a obisidian robot, that must be good too!
                    break
        else:
            # Or save the resources
            queue.append(
                (
                    time - 1,
                    resources + robots,
                    robots,
                )
            )
    return geodes


if __name__ == "__main__":
    blueprints = read_blueprints()
    print(
        sum(
            bp_id * dig(costs, (24, util.Vector(0, 0, 0, 0), util.Vector(0, 0, 0, 1)))
            for bp_id, costs in blueprints
        )
    )
    print(
        util.prod(
            dig(costs, (32, util.Vector(0, 0, 0, 0), util.Vector(0, 0, 0, 1)))
            for _, costs in blueprints[:3]
        )
    )

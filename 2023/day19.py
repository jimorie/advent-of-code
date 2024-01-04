from __future__ import annotations

import math
import re
import util


def read_input() -> tuple[dict[str, list], util.Generator[dict[str, int]]]:
    """Read the input and return a tuple with the workflows and parts."""
    lines = util.readlines()
    rule_pat = re.compile(r"(\w+)([<>])(\d+):(\w+)")
    workflows = {}
    parts = []
    while line := next(lines):
        name, line = line.split("{")
        rules = []
        for rule in line.strip("}").split(","):
            if ":" in rule:
                key, op, val, target = rule_pat.search(rule).groups()
                rules.append((key, op, int(val), target))
            else:
                rules.append(rule)
        workflows[name] = rules
    for line in lines:
        part = {}
        for var in line.strip("{}").split(","):
            name, value = var.split("=")
            part[name] = int(value)
        parts.append(part)
    return workflows, parts


def find_constraints(
    workflows: dict[str, list], name: str, constraints: dict[str, range]
) -> util.Generator[dict[str, range]]:
    """
    Yield the constraints that cover all accepted combinations. Where
    `workflows` are all the available `workflows`, `name` is the current
    workflow to explore, and `constraints` are the constraints imposed on us
    thus far.
    """
    if name == "A":
        yield constraints
    elif name != "R":
        for rule in workflows[name]:
            if isinstance(rule, tuple):
                key, op, val, target = rule
                next_constraints = add_constraint(constraints.copy(), key, op, val)
                yield from find_constraints(workflows, target, next_constraints)
                op, val = (">", val - 1) if op == "<" else ("<", val + 1)
                add_constraint(constraints, key, op, val)
            else:
                yield from find_constraints(workflows, rule, constraints)


def add_constraint(
    constraints: dict[str, range], key: str, op: str, val: int
) -> dict[str, range]:
    """Add the additional `key` `constraints` imposed by `op` and `val`."""
    r = constraints[key]
    constraints[key] = range(val + 1, r.stop) if op == ">" else range(r.start, val)
    return constraints


if __name__ == "__main__":
    workflows, parts = read_input()
    keys = "xmas"
    start = "in"
    constraints: list[dict[str, range]] = list(
        find_constraints(workflows, start, {key: range(1, 4001) for key in keys})
    )
    print(
        sum(
            sum(part.values())
            for part in parts
            if any(
                all(part[key] in constraint[key] for key in part)
                for constraint in constraints
            )
        )
    )
    print(
        sum(
            math.prod(r.stop - r.start for r in constraint.values())
            for constraint in constraints
        )
    )

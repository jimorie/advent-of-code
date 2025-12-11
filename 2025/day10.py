from __future__ import annotations

import itertools
import util


type Machine = tuple[int, list[int], tuple]


def read_machines() -> Generator[Machine]:
    """Yield a `Machine` tuple for each line in the input."""
    for line in util.readlines():
        lights, line = line[1:].split("] ", 1)
        buttons, joltages = line[:-1].split(" {")
        yield parse_lights(lights), parse_buttons(buttons), tuple(
            int(d) for d in joltages.split(",")
        )


def parse_lights(lights: str) -> int:
    """
    Return a integer representation of the `lights` using bits to represent
    their states.
    """
    return int("".join("1" if c == "#" else "0" for c in reversed(lights)), 2)


def parse_buttons(buttons) -> list[int]:
    """
    Return a list of integer representation for each of the `buttons` using
    bits corresponding to the `lights` whose state they toggle.
    """
    buttons = buttons.split(" ")
    masks = [0] * len(buttons)
    for i, button in enumerate(buttons):
        for light in button[1:-1].split(","):
            masks[i] |= 1 << int(light)
    return masks


def toggle_lights(machine: Machine) -> int:
    """
    Return the least number of button presses required to turn the `machine`
    lights to their desired state.
    """
    goal, buttons, _ = machine
    explore = [(0, 0)]
    seen = {0}
    while explore:
        state, presses = explore.pop(0)
        if state == goal:
            return presses
        for button in buttons:
            next = state ^ button
            if next not in seen:
                explore.append((next, presses + 1))
                seen.add(next)
    raise RuntimeError("No solution found... :/")


def increment_joltages(machine: Machine) -> int:
    """
    WIP. This approach takes way too much time. Yet, I don't want to use
    external libraries. So... will have to come back to this one!
    """
    _, buttons, start = machine
    # Unpack the button bits to tuples for this one... :)
    buttons = [
        tuple(bool(button & (1 << i)) for i in range(len(start))) for button in buttons
    ]
    # Sort the buttons so that we press the ones that are quicker to reach a
    # state we can start pruning from
    buttons.sort(
        key=lambda button: sum(start[i] for i in range(len(start)) if button[i])
    )
    # We need to prune the search space as much as we can for this one! Analyze
    # the buttons we have to see if there are any states we can discard
    # early
    must_be_closer = []
    for i, j in itertools.permutations(range(len(start)), 2):
        if not any(button[i] > button[j] for button in buttons):
            must_be_closer.append((i, j))
    # Start with the desired end state and then the goal is to decrement all
    # tuple members to 0
    explore = [(start, 0)]
    goal = tuple(0 for _ in range(len(start)))
    seen = set()
    # Standard BFS...
    while explore:
        state, presses = explore.pop(0)
        if state == goal:
            return presses
        for button in buttons:
            next = tuple(a - b for a, b in zip(state, button))
            if next in seen:
                continue
            if any(counter < 0 for counter in next):
                continue
            if any(next[i] > next[j] for i, j in must_be_closer):
                continue
            explore.append((next, presses + 1))
            seen.add(next)
    raise RuntimeError("No solution found... :/")


if __name__ == "__main__":
    machines = list(read_machines())
    print(sum(toggle_lights(machine) for machine in machines))
    # TODO: This works for the example input but is too slow for the real input!
    # print(sum(increment_joltages(machine) for machine in machines))

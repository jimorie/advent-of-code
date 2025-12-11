from __future__ import annotations

import functools
import util


type Devices = dict[str, list[str]]


def read_devices() -> Devices:
    """Return a dict with all the devices and their connections in the input."""
    devices = {}
    for line in util.readlines():
        device, connections = line.split(": ")
        devices[device] = connections.split()
    return devices


@functools.cache
def find_paths(parent: str, constraints: set | None = None) -> int:
    """
    Return the number of paths that lead from `parent` to `"out"`. If
    `constraints` are given, then these nodes must appear in the path for it to
    count.
    """
    global devices
    if parent == "out":
        return not constraints
    if constraints and parent in constraints:
        constraints -= {parent}
    return sum(find_paths(child, constraints) for child in devices[parent])


if __name__ == "__main__":
    global devices  # So we can use @functools.cache
    devices = read_devices()
    print(find_paths("you"))
    print(find_paths("svr", constraints=frozenset({"dac", "fft"})))

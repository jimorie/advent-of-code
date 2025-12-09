from __future__ import annotations

import collections
import itertools

import util


type Distance = tuple[float, tuple[util.Position, util.Position]]


def read_boxes() -> util.Grid:
    """Return a grid with all circuit boxes positions' from the input."""
    boxes = util.Grid()
    for line in util.readlines():
        x, y, z = line.split(",")
        boxes[util.Position(int(x), int(y), int(z))] = None
    return boxes


def calculate_distances(boxes: util.Grid) -> list[Distance]:
    """Return a sorted list of distances between each pair of `boxes`."""
    return sorted(
        (pair[0].distance_3d(pair[1]), pair)
        for pair in itertools.combinations(boxes, 2)
    )


def connect_boxes(
    boxes: util.Grid,
    distances: list[Distance],
    stop_at: int | None = None,
    circuits: dict[set] | None = None,
) -> dict[set]:
    """
    Connect the `boxes` by connecting the closest pairs of boxes first.
    Update `boxes` by setting the current circuit of the boxes connected.
    """
    circuits = circuits or collections.defaultdict(set)
    start = 1 if stop_at else max(circuits) + 1
    for i, (distance, (a, b)) in enumerate(distances, start):
        circuit_a = boxes.get(a)
        circuit_b = boxes.get(b)
        if circuit_a and circuit_b and circuit_a != circuit_b:
            # Merge the two existing circuits
            members_b = circuits.pop(circuit_b)
            circuits[circuit_a].update(members_b)
            for pos in members_b:
                boxes[pos] = circuit_a
        else:
            circuit = circuit_a or circuit_b or i
            boxes[a] = circuit
            boxes[b] = circuit
            circuits[circuit].add(a)
            circuits[circuit].add(b)
        # Part 1 stop condition
        if stop_at and i >= stop_at:
            break
        # Part 2 stop condition
        if not stop_at and len(circuits) == 1 and all(boxes.values()):
            break
    return circuits, a, b


if __name__ == "__main__":
    boxes = read_boxes()
    distances = calculate_distances(boxes)

    # Part 1
    circuits, _, _ = connect_boxes(boxes, distances, stop_at=1000)
    sizes = sorted([len(circuit) for circuit in circuits.values()], reverse=True)
    print(util.prod(sizes[:3]))

    # Part 2
    _, a, b = connect_boxes(boxes, distances, circuits=circuits)
    print(a.x * b.x)

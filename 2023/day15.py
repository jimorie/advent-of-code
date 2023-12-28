from __future__ import annotations

import util


def hashit(s: str) -> int:
    """Return the HASH value of `str`."""
    v: int = 0
    for c in s:
        v += ord(c)
        v *= 17
        v %= 256
    return v


def process(steps: list[str]) -> list[dict[str, int]]:
    """
    Process all `steps` and return the resulting list of boxes with
    lenses.
    """
    boxes = [{} for _ in range(256)]
    for step in steps:
        if step.endswith("-"):
            label = step.removesuffix("-")
            boxes[hashit(label)].pop(label, None)
        else:
            label, value = step.split("=")
            boxes[hashit(label)][label] = int(value)
    return boxes


if __name__ == "__main__":
    steps = util.read().strip().split(",")
    print(sum(hashit(step) for step in steps))
    print(
        sum(
            boxnum * slotnum * focallength
            for boxnum, box in enumerate(process(steps), 1)
            for slotnum, focallength in enumerate(box.values(), 1)
        )
    )

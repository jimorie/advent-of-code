from __future__ import annotations

import util


def read_rows() -> util.Generator[list[str]]:
    """Yield each pattern in the input as a list of strings."""
    for chunk in util.readchunks():
        yield chunk.strip().split("\n")


def find_reflection(rows: list[str], cols: bool = False, smudge: bool = False) -> int:
    """
    Return the number of rows before the first reflection in `rows`, multiplied
    by 100 unless `cols` is `True`. If no reflection is found and `cols` is
    `False` instead try to find the reflection in the columns formed by `rows`.
    If `smudge` is `True` a reflection is instead found if exactly one pair of
    lines in the reflection has exactly one character difference.
    """
    for i in range(len(rows) - 1):
        cleaned = False
        for a, b in zip(rows[i::-1], rows[(i + 1) :]):
            diff = sum(ca != cb for ca, cb in zip(a, b))
            if diff == 1 and smudge and smudge is not cleaned:
                cleaned = True
            elif diff:
                break
        else:
            if smudge is cleaned:
                return (i + 1) * (1 if cols else 100)
    if not cols:
        return find_reflection(
            ["".join(col) for col in zip(*rows)],
            cols=True,
            smudge=smudge,
        )


if __name__ == "__main__":
    print(sum(find_reflection(rows) for rows in read_rows()))
    print(sum(find_reflection(rows, smudge=True) for rows in read_rows()))

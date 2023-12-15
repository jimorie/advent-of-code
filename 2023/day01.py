from __future__ import annotations

import operator
import util


DIGITS = {str(n): str(n) for n in range(10)}
NUMERALS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def read_values(valid: dict[str, str]) -> util.Generator[int]:
    """
    Yield the sum of the first and last valid numbers of each line in the
    input.
    """
    for line in util.readlines():
        indices = [(n, line.find(n), line.rfind(n)) for n in valid if n in line]
        first, *_ = min(indices, key=operator.itemgetter(1))
        last, *_ = max(indices, key=operator.itemgetter(2))
        yield int(valid[first] + valid[last])


if __name__ == "__main__":
    print(sum(read_values(DIGITS)))
    print(sum(read_values({**DIGITS, **NUMERALS})))

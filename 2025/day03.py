from __future__ import annotations

import util


def read_banks() -> Generator[tuple[int]]:
    """Yield a tuple representint a battery bank for each line in the input."""
    for line in util.readlines():
        yield tuple(int(c) for c in line)


def get_bank_maximum(bank: tuple[int], count: int = 2) -> int:
    """
    Return the maximum possible joltage by picking `count` number of batteries
    from the `bank`.
    """
    size = len(bank)
    index = 0
    maximum = 0
    for place in range(count - 1, -1, -1):
        v = max(bank[index : size - place])
        index = bank.index(v, index, size - place) + 1
        maximum += v * 10**place
    return maximum


if __name__ == "__main__":
    print(sum(get_bank_maximum(bank, count=2) for bank in read_banks()))
    print(sum(get_bank_maximum(bank, count=12) for bank in read_banks()))

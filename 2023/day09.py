from __future__ import annotations

import util


def read_histories() -> util.Generator[list[int]]:
    """Yield each line in the input as a list of integers."""
    for line in util.readlines():
        yield [int(n) for n in line.split()]


def predict(history: list[int], prev: bool = False) -> int:
    """
    Return the next number in the `history`. (Or previous number if `prev` is
    `True`.)
    """
    if history[-1] == 0:
        return 0
    prediction = predict([b - a for a, b in util.pairwise(history)], prev=prev)
    return history[0] - prediction if prev else history[-1] + prediction


if __name__ == "__main__":
    print(sum(predict(history) for history in read_histories()))
    print(sum(predict(history, prev=True) for history in read_histories()))

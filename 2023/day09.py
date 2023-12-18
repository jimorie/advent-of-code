from __future__ import annotations

import util


def predict(history: list[int], prev: bool = False) -> int:
    """
    Return the next number in the `history`. (Or previous number if `prev` is
    `True`.)
    """
    if any(history):
        prediction = predict([b - a for a, b in util.pairwise(history)], prev=prev)
        return history[0] - prediction if prev else history[-1] + prediction
    return 0


if __name__ == "__main__":
    print(sum(predict(history) for history in util.readintlines()))
    print(sum(predict(history, prev=True) for history in util.readintlines()))

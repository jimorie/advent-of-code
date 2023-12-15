from __future__ import annotations

import util


def read_cards() -> util.Generator[int]:
    """Yield the number of wins for each card in the input."""
    for line in util.readlines():
        _, line = line.split(": ")
        winners, yours = line.split(" | ")
        winners = set(winners.split())
        yield sum(your in winners for your in yours.split())


def count_copies(cards: util.Iterable[int]) -> list[int]:
    """
    Return the numbers of copies for each card based on their number of wins.
    """
    copies = [1] * len(cards)
    for i, w in enumerate(cards):
        for j in range(i + 1, i + 1 + w):
            if j >= len(cards):
                break
            copies[j] += copies[i]
    return copies


if __name__ == "__main__":
    cards = list(read_cards())
    print(sum(int(2 ** (wins - 1)) for wins in cards))
    print(sum(count_copies(cards)))

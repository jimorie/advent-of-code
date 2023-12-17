from __future__ import annotations

import collections
import util


CARDVALUES = dict(pair for pair in zip("AKQJT98765432", range(14, 1, -1)))
JOKER = 0


def read_hands() -> util.Generator[tuple[int, int, int, int, int, int, int]]:
    """
    Yield each hand in the input as a tuple of integers, with the first item
    being the hand rank, the last being the bid and the 5 values in between
    being the card values. This means the hand strengths can be compared
    without further effort.
    """
    for line in util.readlines():
        hand, bid = line.split()
        cards = tuple(CARDVALUES[card] for card in hand)
        yield (rank(cards), *cards, int(bid))


def rank(cards: tuple[int, int, int, int, int]) -> int:
    """
    Return the rank of the card values as an integer, a higher value means a
    stronger hand. Consider jokers.
    """
    counter = collections.Counter(cards)
    if JOKER in counter:
        jokers = counter[JOKER]
        counter[JOKER] = 0
    else:
        jokers = 0
    same = max(counter.values())
    if same + jokers == 5:  # Five of a kind
        return 7
    if same + jokers == 4:  # Four of a kind
        return 6
    if same == 3 and len(counter) == 2:  # Full house
        return 5
    if jokers and len(counter) == 3:  # Also full house
        return 5
    if same + jokers == 3:  # Three of a kind
        return 4
    if same == 2 and len(counter) == 3:  # Two pair
        return 3
    if same + jokers == 2:  # One pair
        return 2
    return 1


def sum_winnings():
    """Return the sum of winnings for all hands in the input."""
    return sum(rank * hand[-1] for rank, hand in enumerate(sorted(read_hands()), 1))


if __name__ == "__main__":
    print(sum_winnings())
    CARDVALUES["J"] = JOKER
    print(sum_winnings())

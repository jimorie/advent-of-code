import collections
import util


def read_cards():
    for line in util.readlines():
        card, line = line.split(": ")
        winners, yours = line.split(" | ")
        winners = set(winners.split())
        yours = set(yours.split())
        yield card, sum(your in winners for your in yours)


def win_copies(cardwins):
    cards = list(cardwins)
    copies = {card: 1 for card in cards}
    for i, card in enumerate(cards):
        for j in range(i + 1, i + 1 + cardwins[card]):
            if j >= len(cards):
                break
            copies[cards[j]] += copies[card]
    return copies


if __name__ == "__main__":
    cardwins = dict(card for card in read_cards())
    print(sum(2 ** (wins - 1) if wins else 0 for wins in cardwins.values()))
    copies = win_copies(cardwins)
    print(sum(copies.values()))

import util


def score_deck(deck):
    return sum(i * card for i, card in enumerate(reversed(deck), 1))


def check_seen(decks, seen):
    for i, deck in enumerate(decks):
        t = tuple(deck)
        if t in seen[i]:
            return True
        seen[i].add(t)
    return False


def copy_decks(decks, cards):
    return [deck[: cards[i]] for i, deck in enumerate(decks)]


def play(decks, recursive=False):
    seen = [set() for _ in decks]
    while all(deck for deck in decks):
        if recursive and check_seen(decks, seen):
            raise RecursionError()  # Player 1 wins
        cards = [deck.pop(0) for deck in decks]
        if recursive and all(card <= len(decks[i]) for i, card in enumerate(cards)):
            try:
                _, winner = play(copy_decks(decks, cards), recursive)
            except RecursionError:
                winner = 0  # Player 1 wins
        else:
            winner = cards.index(max(cards))
        for i in range(len(cards)):
            decks[winner].append(cards[(winner + i) % len(cards)])
    return max((score_deck(deck), i) for i, deck in enumerate(decks))


def read_decks():
    decks = []
    for line in util.readlines():
        if line.startswith("Player"):
            decks.append([])
        else:
            try:
                decks[-1].append(int(line))
            except ValueError:
                pass
    return decks


def main(recursive=False):
    decks = read_decks()
    score, _ = play(decks, recursive)
    return score


if __name__ == "__main__":
    print(main())
    print(main(True))

import util

SCORES = {
    "A X": 1 + 3,
    "A Y": 2 + 6,
    "A Z": 3 + 0,
    "B X": 1 + 0,
    "B Y": 2 + 3,
    "B Z": 3 + 6,
    "C X": 1 + 6,
    "C Y": 2 + 0,
    "C Z": 3 + 3,
}


def score(line):
    them, strategy = line.split()
    # Should we pick the "next", "previous" or same as them?
    diff = ord(strategy) - ord("Y")
    # What index of "ABC" did they play?
    index = ord(them) - ord("A")
    # What index should we play?
    index = (index + diff) % 3
    # Translate to "XYZ".
    us = chr(ord("X") + index)
    return SCORES[f"{them} {us}"]


if __name__ == "__main__":
    print(sum(SCORES[line] for line in util.readlines()))
    print(sum(score(line) for line in util.readlines()))

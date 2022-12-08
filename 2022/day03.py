import util


def itemprio(char):
    prio = ord(char)
    if prio >= ord("a"):
        return prio - ord("a") + 1
    return prio - ord("A") + 27


def find_misplaced_prio(line):
    half = len(line) // 2
    return itemprio(set.intersection(set(line[:half]), set(line[half:])).pop())


def find_badge_prio(lines):
    return itemprio(set.intersection(*(set(line) for line in lines)).pop())


if __name__ == "__main__":
    print(sum(find_misplaced_prio(line) for line in util.readlines()))
    print(sum(find_badge_prio(lines) for lines in util.readlinegroups(3)))

import util


def parse_range(assignment):
    start, end = assignment.split("-")
    return (int(start), int(end))


def parse_assignment(line):
    a1, a2 = line.split(",")
    return (*parse_range(a1), *parse_range(a2))


def find_overlaps(test):
    for line in util.readlines():
        assignment = parse_assignment(line)
        if test(*assignment):
            yield assignment


def test_overlap(s1, e1, s2, e2):
    return (s1 >= s2 and e1 <= e2) or (s2 >= s1 and e2 <= e1)


def test_partial_overal(s1, e1, s2, e2):
    return s1 <= s2 <= e1 or s1 <= e2 <= e1 or s2 <= s1 <= e2 or s2 <= e1 <= e2


if __name__ == "__main__":
    print(sum(1 for _ in find_overlaps(test_overlap)))
    print(sum(1 for _ in find_overlaps(test_partial_overal)))

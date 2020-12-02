import itertools
import util


def day1(numbers, key, size=2):
    for combination in itertools.combinations(numbers, size):
        if sum(combination) == key:
            return util.prod(combination)
    raise SystemExit("No solution found")


if __name__ == "__main__":
    print(day1(util.readints(), 2020, size=2))

import itertools
import util


def find_invalid(numbers, size):
    for i in range(size, len(numbers)):
        if not any(
            sum(combination) == numbers[i]
            for combination in itertools.combinations(numbers[i - 25 : i], 2)
        ):
            return numbers[i]
    raise SystemExit("No solution found")


if __name__ == "__main__":
    print(find_invalid(list(util.readints()), 25))

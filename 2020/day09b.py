import day09a
import util


def find_continuous_set(numbers, target):
    for i in range(len(numbers)):
        total = numbers[i]
        for j in range(i + 1, len(numbers)):
            total += numbers[j]
            if total == target:
                continuous_set = sorted(numbers[i : j + 1])
                return continuous_set[0] + continuous_set[-1]
            if total > target:
                break
    raise SystemExit("No solution found")


if __name__ == "__main__":
    numbers = list(util.readints())
    target = day09a.find_invalid(numbers, 25)
    print(find_continuous_set(numbers, target))

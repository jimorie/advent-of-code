import collections
import util


def jolt_differences(adapters):
    adapters = sorted(adapters)
    differences = collections.Counter(
        adapters[i] - (adapters[i - 1] if i else 0) for i in range(0, len(adapters))
    )
    differences[3] += 1
    return differences[1] * differences[3]


if __name__ == "__main__":
    print(jolt_differences(util.readints()))

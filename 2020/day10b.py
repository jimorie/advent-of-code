import functools
import util


def next_possible(adapters, start):
    i = start + 1
    while i < len(adapters) and adapters[i] - adapters[start] <= 3:
        yield i
        i += 1


def count_possible(adapters):
    adapters = sorted(adapters)
    adapters.insert(0, 0)

    @functools.lru_cache
    def count_possible_from(start):
        if start == len(adapters) - 1:
            return 1
        return sum(count_possible_from(i) for i in next_possible(adapters, start))

    return count_possible_from(0)


if __name__ == "__main__":
    print(count_possible(util.readints()))

import itertools
import functools
import json
import util


def read_pairs():
    for chunk in util.readchunks():
        a, b = chunk.splitlines()
        yield json.loads(a), json.loads(b)


def compare_pair(a, b):
    if isinstance(a, int):
        if isinstance(b, int):
            return a - b
        a = [a]
    elif isinstance(b, int):
        b = [b]
    for ai, bi in zip(a, b):
        r = compare_pair(ai, bi)
        if r != 0:
            return r
    return len(a) - len(b)


def find_divider_packets():
    divider_a = [[2]]
    divider_b = [[6]]
    packets = list(itertools.chain.from_iterable(read_pairs()))
    packets.append(divider_a)
    packets.append(divider_b)
    packets.sort(key=functools.cmp_to_key(compare_pair))
    return (packets.index(divider_a) + 1) * (packets.index(divider_b) + 1)


if __name__ == "__main__":
    print(sum(i for i, (a, b) in enumerate(read_pairs(), 1) if compare_pair(a, b) < 0))
    print(find_divider_packets())

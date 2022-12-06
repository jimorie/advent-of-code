import collections
import util


def parse_stacks(lines):
    line = lines.pop(-1)
    labels = {i: line[i] for i in range(1, len(line), 4)}
    stacks = collections.defaultdict(list)
    for line in reversed(lines):
        for i in range(1, len(line), 4):
            if i < len(line) and line[i] != " ":
                stacks[labels[i]].append(line[i])
    return stacks


def parse_input():
    p1, p2 = util.readchunks()
    return parse_stacks(p1.splitlines()), p2.splitlines()


def move_stacks(crane):
    stacks, lines = parse_input()
    for line in lines:
        crane(line, stacks)
    return "".join(v[-1] for _, v in sorted(stacks.items()))


def crate_mover_9000(line, stacks):
    _, amount, _, src, _, trg = line.split()
    for _ in range(int(amount)):
        stacks[trg].append(stacks[src].pop())


def crate_mover_9001(line, stacks):
    _, amount, _, src, _, trg = line.split()
    amount = int(amount)
    stacks[trg].extend(stacks[src][-amount:])
    stacks[src] = stacks[src][:-amount]


if __name__ == "__main__":
    print(move_stacks(crate_mover_9000))
    print(move_stacks(crate_mover_9001))

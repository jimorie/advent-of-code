import operator
import util


class Monkey:
    def __init__(self, chunk):
        lines = chunk.splitlines()
        self.name = lines.pop(0).strip(":")
        self.items = self.parse_items(lines.pop(0))
        self.operation = self.parse_operation(lines.pop(0))
        self.test_divisor = int(lines.pop(0)[len("  Test: divisible by ") :])
        self.if_true = int(lines.pop(0)[len("    If true: throw to monkey ") :])
        self.if_false = int(lines.pop(0)[len("    If false: throw to monkey ") :])
        self.inspect_count = 0

    @staticmethod
    def parse_items(line):
        return [int(item) for item in line[len("  Starting items: ") :].split(", ")]

    @staticmethod
    def parse_operation(line):
        op, arg = line[len("  Operation: new = old ") :].split()
        if op == "+":
            op = operator.add
        elif op == "*":
            op = operator.mul
        else:
            raise RuntimeError("Unknown operator")
        return lambda old: op(old, old if arg == "old" else int(arg))

    def take_turn(self, part, divisible_by_all):
        while self.items:
            item = self.items.pop(0)
            self.inspect_count += 1
            item = self.operation(item)
            if part == 1:
                item //= 3
            elif part == 2:
                item %= divisible_by_all
            target = self.if_false if item % self.test_divisor else self.if_true
            yield (item, target)


def read_monkeys():
    return [Monkey(chunk) for chunk in util.readchunks()]


def play_keep_away(rounds=20, part=1):
    monkeys = read_monkeys()
    divisible_by_all = (
        util.prod(monkey.test_divisor for monkey in monkeys) if part == 2 else 0
    )
    for n in range(rounds):
        for monkey in monkeys:
            for item, target in monkey.take_turn(part, divisible_by_all):
                monkeys[target].items.append(item)
    return monkeys


def find_monkey_business_score(rounds=20, part=1):
    monkeys = play_keep_away(rounds, part)
    inspected = sorted(m.inspect_count for m in monkeys)
    return inspected[-2] * inspected[-1]


if __name__ == "__main__":
    print(find_monkey_business_score(rounds=20, part=1))
    print(find_monkey_business_score(rounds=10000, part=2))

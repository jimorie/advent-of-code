import operator
import util


def read_monkeys():
    monkeys = {}
    for line in util.readlines():
        name, expr = line.split(": ")
        try:
            monkeys[name] = int(expr)
        except ValueError:
            m1, op, m2 = expr.split()
            monkeys[name] = (util.OPERATORS[op], m1, m2)
    return monkeys


def make_tree(monkeys, name, unknown=None):
    expr = monkeys[name]
    if isinstance(expr, int):
        # Make leaf node tuple with its name, value and flag whether it's the
        # unknown variable.
        return (name, expr, name == unknown)
    op, m1, m2 = expr
    n1 = make_tree(monkeys, m1, unknown=unknown)
    n2 = make_tree(monkeys, m2, unknown=unknown)
    # Make recursive node tuple with its name, operator, left and right
    # subtree, and flag whether the unknown variable is in either subtree.
    return (name, op, n1, n2, n1[-1] or n2[-1])


def solve_tree(node, expected=None, solutions=None):
    if len(node) == 3:
        # Leaf node
        name, expr, unknown = node
        if unknown and expected:
            # This is the unknown variable! Set and return the expected
            # solution.
            solutions[name] = expected
            return expected
        return expr
    # Recursive node
    name, op, n1, n2, unknown = node
    if expected is None or unknown is False:
        return op(solve_tree(n1), solve_tree(n2))
    if n1[-1]:
        # Unknown variable in first sub-tree
        r2 = solve_tree(n2)
        if op is operator.add:
            expected = expected - r2
        elif op is operator.mul:
            expected = expected // r2
        elif op is operator.sub:
            expected = expected + r2
        elif op is operator.floordiv:
            expected = expected * r2
        r1 = solve_tree(n1, expected=expected, solutions=solutions)
    elif n2[-1]:
        # Unknown variable in second sub-tree
        r1 = solve_tree(n1)
        if op is operator.add:
            expected = expected - r1
        elif op is operator.mul:
            expected = expected // r1
        elif op is operator.sub:
            expected = r1 - expected  # Change order, not operator
        elif op is operator.floordiv:
            expected = r1 // expected  # Change order, not operator
        r2 = solve_tree(n2, expected=expected, solutions=solutions)
    return op(r1, r2)


if __name__ == "__main__":
    monkeys = read_monkeys()
    root = make_tree(monkeys, "root", unknown="humn")
    # Part 1: Just evaluate the tree, no unknown variable.
    print(solve_tree(root))
    # Part 2: Figure out the value of "humn" if "root" operator is - and its
    # expected value is 0
    root = tuple(x if x is not operator.add else operator.sub for x in root)
    solutions = {}
    solve_tree(root, expected=0, solutions=solutions)
    print(solutions["humn"])

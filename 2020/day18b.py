import day18a
import operator
import util


level1_operators = {"*": operator.mul}
level2_operators = {"+": operator.add}


def level2_parser(tokens, root_parser):
    return day18a.evaluate(tokens, level2_operators, day18a.leaf_parser, root_parser)


def root_parser(tokens):
    return day18a.evaluate(tokens, level1_operators, level2_parser, root_parser)


if __name__ == "__main__":
    print(sum(root_parser(day18a.tokenize(line)) for line in util.readlines()))

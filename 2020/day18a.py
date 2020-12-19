import operator
import util


operators = {
    "+": operator.add,
    "*": operator.mul,
}


def evaluate(tokens, operators, term_parser, root_parser):
    result = term_parser(tokens, root_parser)
    while tokens and tokens[0] in operators:
        t = tokens.pop(0)
        result = operators[t](result, term_parser(tokens, root_parser))
    return result


def leaf_parser(tokens, root_parser):
    t = tokens.pop(0)
    if t == "(":
        result = root_parser(tokens)
        tokens.pop(0)  # ")"
    else:
        result = int(t)
    return result


def root_parser(tokens):
    return evaluate(tokens, operators, leaf_parser, root_parser)


def tokenize(line):
    return [t for t in line if t != " "]


if __name__ == "__main__":
    print(sum(root_parser(tokenize(line)) for line in util.readlines()))

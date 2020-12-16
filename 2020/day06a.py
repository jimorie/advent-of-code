import util


def answers(group):
    return {c for c in group if c.isalpha()}


if __name__ == "__main__":
    print(sum(len(answers(group)) for group in util.readchunks()))

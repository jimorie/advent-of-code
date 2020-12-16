import day06a
import util


def common_answers(group):
    individual_answers = (day06a.answers(person) for person in group.splitlines())
    return set.intersection(*individual_answers)


if __name__ == "__main__":
    print(sum(len(common_answers(group)) for group in util.readchunks()))

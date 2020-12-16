import day02a
import util


def validate(line):
    pos1, pos2, char, password = day02a.parse(line)
    return (password[pos1 - 1] == char) + (password[pos2 - 1] == char) == 1


if __name__ == "__main__":
    print(util.count(validate, util.readlines()))

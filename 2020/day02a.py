import util


def parse(line):
    rule, char, password = line.split()
    atleast, atmost = rule.split("-")
    return int(atleast), int(atmost), char[0], password


def validate(line):
    atleast, atmost, char, password = parse(line)
    return atleast <= password.count(char) <= atmost


if __name__ == "__main__":
    print(util.count(validate, util.readlines()))

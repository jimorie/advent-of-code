import util


required_fields = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}


def parse(chunk):
    return {k: v for k, v in (field.split(":") for field in chunk.split())}


def validate(chunk):
    return parse(chunk).keys() >= required_fields


if __name__ == "__main__":
    print(util.count(validate, util.readchunks()))

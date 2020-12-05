import day04a
import util


day04b = __import__(__name__)


def validate(chunk):
    fields = day04a.parse(chunk)
    try:
        return all(
            is_valid(field, fields.get(field, "")) for field in day04a.required_fields
        )
    except ValueError:
        return False


def is_valid(field, value):
    return getattr(day04b, f"validate_{field}")(value)


def validate_byr(value):
    return 1920 <= int(value) <= 2002


def validate_iyr(value):
    return 2010 <= int(value) <= 2020


def validate_eyr(value):
    return 2020 <= int(value) <= 2030


def validate_hgt(value):
    if value.endswith("cm"):
        return 150 <= int(value[:-2]) <= 193
    if value.endswith("in"):
        return 59 <= int(value[:-2]) <= 76
    return False


def validate_hcl(value):
    return len(value) == 7 and value.startswith("#") and int(value[1:], 16) >= 0


def validate_ecl(value):
    return value in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")


def validate_pid(value):
    return len(value) == 9 and value.isdigit()


if __name__ == "__main__":
    print(util.count(validate, util.readchunks()))

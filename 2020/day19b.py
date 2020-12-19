import day19a
import util


if __name__ == "__main__":
    rules, lines = day19a.parse_rules(util.readlines())
    rules["8"] = "42 | 42 8"
    rules["11"] = "42 31 | 42 11 31"
    print(day19a.count(rules, lines))

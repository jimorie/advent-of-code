import util
import re


def parse_rules(lines):
    rules = {}
    for line in lines:
        if line == "":
            break
        idx, rule = line.split(": ")
        rules[idx] = rule
    return rules, lines


def build_regex(idx, rules, depth=0):
    if depth > 14:  # limit found by stepping up until output stabilizes
        return ""
    rule = rules[idx]
    if rule.startswith('"'):
        return rule.strip('"')
    if "|" in rule:
        rule1, rule2 = rule.split(" | ")
        regex1 = "".join(build_regex(r, rules, depth + 1) for r in rule1.split(" "))
        regex2 = "".join(build_regex(r, rules, depth + 1) for r in rule2.split(" "))
        return f"({regex1}|{regex2})"
    return "".join(build_regex(r, rules, depth + 1) for r in rule.split(" "))


def count(rules, lines):
    regex = re.compile(build_regex("0", rules))
    return sum(1 for line in lines if regex.fullmatch(line))


if __name__ == "__main__":
    rules, lines = parse_rules(util.readlines())
    print(count(rules, lines))

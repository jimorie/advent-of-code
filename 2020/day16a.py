import util


def parse_rules(lines):
    rules = {}
    for line in lines:
        if line == "":
            break
        name, rulepart = line.split(": ")
        rules[name] = [
            (int(a), int(b))
            for a, b in (rule.split("-") for rule in rulepart.split(" or "))
        ]
    return rules


def parse(lines):
    rules = parse_rules(lines)
    next(lines)  # "your ticket:"
    my_ticket = [int(n) for n in next(lines).split(",")]
    next(lines)  # ""
    next(lines)  # "nearby tickets:"
    nearby_tickets = ([int(n) for n in line.split(",")] for line in lines)
    return rules, my_ticket, nearby_tickets


def validate(value, rules):
    return {
        name
        for name, ranges in rules.items()
        if any(a <= value <= b for a, b in ranges)
    }


def day16a(lines):
    rules, my_ticket, nearby_tickets = parse(lines)
    return sum(
        value
        for ticket in nearby_tickets
        for value in ticket
        if not validate(value, rules)
    )


if __name__ == "__main__":
    print(day16a(util.readlines()))

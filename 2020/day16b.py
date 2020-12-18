import day16a
import itertools
import util


def validate_ticket(ticket, rules):
    valid = [day16a.validate(value, rules) for value in ticket]
    return valid if all(validfields for validfields in valid) else None


def find_candidates(my_ticket, nearby_tickets, rules):
    candidates = [None] * len(my_ticket)
    for ticket in itertools.chain([my_ticket], nearby_tickets):
        ticket_candidates = validate_ticket(ticket, rules)
        if ticket_candidates is None:
            continue
        for i, field_candidates in enumerate(ticket_candidates):
            if candidates[i] is None:
                candidates[i] = field_candidates
            else:
                candidates[i].intersection_update(field_candidates)
    return candidates


def unique_product(args, i=0, prefix=None):
    if prefix is None:
        prefix = []
    for valid in args[i]:
        if valid in prefix:
            continue
        if i + 1 < len(args):
            for p in unique_product(args, i + 1, prefix + [valid]):
                yield p
        else:
            yield prefix + [valid]


def day16b(lines):
    rules, my_ticket, nearby_tickets = day16a.parse(lines)
    candidates = find_candidates(my_ticket, nearby_tickets, rules)
    unique = next(unique_product(candidates))
    return util.prod(
        my_ticket[i] for i, field in enumerate(unique) if field.startswith("departure")
    )


if __name__ == "__main__":
    print(day16b(util.readlines()))

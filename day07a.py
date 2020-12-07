import collections
import util


def parse_bags(lines):
    bags = collections.defaultdict(dict)
    for line in lines:
        if line.endswith("no other bags."):
            continue
        parent, children = line.split(" bags contain ")
        for childpart in children.split(", "):
            count, *child, _ = childpart.split()
            bags[" ".join(child)][parent] = int(count)
    return bags


def find_parents(bags, child):
    parents = set(bags[child])
    for parent in bags[child]:
        parents.update(find_parents(bags, parent))
    return parents


if __name__ == "__main__":
    print(len(find_parents(parse_bags(util.readlines()), "shiny gold")))

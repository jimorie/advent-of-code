import day07a
import util


def count_children(bags, parent):
    return sum(
        count + count * count_children(bags, child)
        for child, count in (
            (child, parents[parent])
            for child, parents in bags.items()
            if parent in parents
        )
    )


if __name__ == "__main__":
    print(count_children(day07a.parse_bags(util.readlines()), "shiny gold"))

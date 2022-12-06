import util


def find_distinct_marker(distinct):
    line = util.read()
    for i in range(distinct, len(line)):
        if len(set(line[i - distinct : i])) == distinct:
            return i
    raise RuntimeError("No marker found")


if __name__ == "__main__":
    print(find_distinct_marker(4))
    print(find_distinct_marker(14))

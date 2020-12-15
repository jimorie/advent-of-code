import util


def say(n, r, n2r):
    prev_r = n2r.get(n, r)
    n2r[n] = r
    return r - prev_r, r + 1


def elfgame(numbers, endround=2020):
    n2r = {}
    r = 1
    for start_n in numbers:
        n, r = say(start_n, r, n2r)
    while r < endround:
        n, r = say(n, r, n2r)
    return n


if __name__ == "__main__":
    print(elfgame(util.readints()))

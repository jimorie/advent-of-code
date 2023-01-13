import util


SNAFU = {
    "0": 0,
    "1": 1,
    "2": 2,
    "-": -1,
    "=": -2,
}


def to_decimal(s):
    return sum(SNAFU[s[len(s) - i - 1]] * (5**i) for i in range(len(s)))


def to_snafu(d):
    snafu = ""
    mem = 0
    while d:
        d, r = divmod(d, 5)
        r += mem
        if r > 4:
            snafu = "0" + snafu
        elif r == 4:
            snafu = "-" + snafu
            mem = 1
        elif r == 3:
            snafu = "=" + snafu
            mem = 1
        else:
            snafu = str(r) + snafu
            mem = 0
    if mem:
        snafu = str(mem) + snafu
    return snafu


if __name__ == "__main__":
    print(to_snafu(sum(to_decimal(line) for line in util.readlines())))

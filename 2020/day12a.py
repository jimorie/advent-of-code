import util


moves = {
    0: (0, 1),
    90: (1, 0),
    180: (0, -1),
    270: (-1, 0),
}


dirs = {
    "N": 0,
    "E": 90,
    "S": 180,
    "W": 270,
}


def day12a(lines, heading=90):
    x = y = 0
    for line in lines:
        instr = line[0]
        arg = int(line[1:])
        if instr == "R":
            heading = (heading + arg) % 360
        elif instr == "L":
            heading = (heading - arg + 360) % 360
        else:
            dx, dy = moves[dirs.get(instr, heading)]
            x += dx * arg
            y += dy * arg
    return abs(x) + abs(y)


if __name__ == "__main__":
    print(day12a(util.readlines()))

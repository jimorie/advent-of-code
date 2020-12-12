import day12a
import util


def day12b(lines, wx=10, wy=1):
    x = y = 0
    for line in lines:
        instr = line[0]
        arg = int(line[1:])
        if instr in ("L", "R"):
            if instr == "L":
                arg = 360 - arg
            if arg == 90:
                wx, wy = wy, -wx
            elif arg == 180:
                wx, wy = -wx, -wy
            elif arg == 270:
                wx, wy = -wy, wx
        elif instr in ("N", "E", "S", "W"):
            dx, dy = day12a.moves[day12a.dirs[instr]]
            wx += dx * arg
            wy += dy * arg
        elif instr == "F":
            x += wx * arg
            y += wy * arg
    return abs(x) + abs(y)


if __name__ == "__main__":
    print(day12b(util.readlines()))

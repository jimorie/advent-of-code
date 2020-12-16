import day13a
import util


def busjam(lines):
    _, buses = day13a.parse(lines)
    time = 0
    step = 1
    for delay, bus in enumerate(buses):
        if bus == "x":
            continue
        while (time + delay) % bus:
            time += step
        step *= bus
    return time


if __name__ == "__main__":
    print(busjam(util.readlines()))

import util


def parse(lines):
    earliest, buses = lines
    return (
        int(earliest),
        [int(bus) if bus != "x" else bus for bus in buses.split(",")],
    )


def earliestbus(lines):
    earliest, buses = parse(lines)
    wait_time, next_bus = min(
        (bus - earliest % bus, bus) for bus in buses if bus != "x"
    )
    return wait_time * next_bus


if __name__ == "__main__":
    print(earliestbus(util.readlines()))

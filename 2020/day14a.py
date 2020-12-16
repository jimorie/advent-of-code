import util


def parse_mask(line):
    return line.split("mask = ")[1]


def parse_mem(line):
    addr, value = line.split("] = ")
    return int(addr[len("mem[") :]), int(value)


def apply_mask(mask, value):
    for i, b in enumerate(reversed(mask)):
        if b == "1":
            value |= 1 << i
        elif b == "0":
            value &= ~(1 << i)
    return value


def day14a(lines):
    mem = {}
    mask = ""
    for line in lines:
        if line.startswith("mask"):
            mask = parse_mask(line)
        elif line.startswith("mem"):
            addr, value = parse_mem(line)
            mem[addr] = apply_mask(mask, value)
    return sum(mem.values())


if __name__ == "__main__":
    print(day14a(util.readlines()))

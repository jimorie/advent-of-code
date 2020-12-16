import day14a
import util


def float_mask(mask):
    if "X" in mask:
        prefix, mask = mask.split("X", 1)
        for suffix in float_mask(mask):
            yield prefix + "0" + suffix
            yield prefix + "1" + suffix
    else:
        yield mask


def parse_mask(line):
    return day14a.parse_mask(line).replace("0", "Z")


def day14b(lines):
    mem = {}
    masks = None
    for line in lines:
        if line.startswith("mask"):
            masks = list(float_mask(parse_mask(line)))
        elif line.startswith("mem"):
            addr, value = day14a.parse_mem(line)
            for mask in masks:
                mem[day14a.apply_mask(mask, addr)] = value
    return sum(mem.values())


if __name__ == "__main__":
    print(day14b(util.readlines()))

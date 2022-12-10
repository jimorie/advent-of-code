import util


def generate_signals():
    x = 1
    cycle = 1
    for line in util.readlines():
        if line == "noop":
            cycle_cost = 1
            x_mod = 0
        elif line.startswith("addx"):
            cycle_cost = 2
            _, x_mod = line.split()
            x_mod = int(x_mod)
        else:
            raise RuntimeError("Unknown operation")
        for _ in range(cycle_cost):
            yield (cycle, x)
            cycle += 1
        x += x_mod


def find_signal_strengths(cycles):
    return sum(cycle * x for cycle, x in generate_signals() if cycle in cycles)


def draw_crt(rows=6, cols=40):
    crt = [["."] * cols for _ in range(rows)]
    for cycle, x in generate_signals():
        cycle -= 1  # Cycle 1 draws pixel 0
        row, col = divmod(cycle, cols)
        row %= rows
        if x - 1 <= col <= x + 1:  # Sprite width 3
            crt[row][col] = "#"
    return "\n".join("".join(row) for row in crt)


if __name__ == "__main__":
    print(find_signal_strengths({20, 60, 100, 140, 180, 220}))
    print(draw_crt())

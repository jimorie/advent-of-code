import util


class GameConsole:
    def __init__(self, program):
        self.program = list(
            [op, int(arg)] for op, arg in (line.split() for line in program)
        )
        self.reset()

    def reset(self):
        self.pos = 0
        self.accumulator = 0

    def run(self):
        visited = []
        while self.pos < len(self.program):
            if self.pos in visited:
                break
            visited.append(self.pos)
            op, arg = self.program[self.pos]
            getattr(self, f"eval_{op}")(arg)
        return visited

    def eval_nop(self, arg):
        self.pos += 1

    def eval_jmp(self, arg):
        self.pos += arg

    def eval_acc(self, arg):
        self.accumulator += arg
        self.pos += 1


if __name__ == "__main__":
    hhgc = GameConsole(util.readlines())
    hhgc.run()
    print(hhgc.accumulator)

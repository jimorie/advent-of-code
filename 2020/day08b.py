import day08a
import util


class BacktrackingGameConsole(day08a.GameConsole):
    def run(self):
        visited = super().run()
        while self.pos < len(self.program):
            last_pos = visited.pop()
            last_op = self.program[last_pos][0]
            if last_op not in ("nop", "jmp"):
                continue
            try_op = "nop" if last_op == "jmp" else "jmp"
            self.program[last_pos][0] = try_op
            self.reset()
            super().run()
            self.program[last_pos][0] = last_op


if __name__ == "__main__":
    hhgc = BacktrackingGameConsole(util.readlines())
    hhgc.run()
    print(hhgc.accumulator)

from __future__ import annotations

import util


class Platform(util.Grid):
    """
    Represent a platform with rounded rocks (O) and cube-shaped rocks (#).
    """

    @classmethod
    def from_iterable(cls, rows):
        def cast(c):
            return c if c != "." else None

        return super().from_iterable(rows)

    def tilt(self):
        """
        Tilt the platform so that all rounded rocks roll as far north as
        possible.
        """
        col = -1
        for pos, c in sorted(self.items()):
            if col != pos.x:
                col = pos.x
                blocker = -1
            if c == "#":
                blocker = pos.y
            elif c == "O":
                self.pop(pos)
                self[util.Position(pos.x, blocker + 1)] = c
                blocker += 1

    def spin(self):
        """Tilt the platform north, west, south and east."""
        for _ in range(4):
            self.tilt()
            self.rotate()

    def longspin(self, cycles: int = 1_000_000_000):
        """Spin the platform a large number of cycles."""
        cycle = 0
        states = {self.hash(): cycle}
        while cycle < cycles:
            self.spin()
            cycle += 1
            state = self.hash()
            if state in states:
                _, remainder = divmod(cycles - cycle, cycle - states[state])
                cycle = cycles - remainder
                states.clear()
            states[state] = cycle

    def hash(self):
        """Return a hashable representation of the platform state."""
        return frozenset(k for k, v in self.items() if v == "O")

    def get_load(self):
        """Return the load on the platform's north support beam."""
        return sum(platform.height - pos.y for pos, c in self.items() if c == "O")

    def __str__(self):
        return (
            "\n".join(
                "".join(self.get(util.Position(x, y), ".") for x in range(self.width))
                for y in range(self.height)
            )
            + "\n"
        )


if __name__ == "__main__":
    # Part 1
    platform = Platform.from_iterable(util.readlines())
    platform.tilt()
    print(platform.get_load())

    # Part 2
    platform = Platform.from_iterable(util.readlines())
    platform.longspin()
    print(platform.get_load())

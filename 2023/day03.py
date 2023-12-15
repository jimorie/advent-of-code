from __future__ import annotations

import util


class Schematic:
    def __init__(self):
        self.grid: dict[util.Position, str] = {
            util.Position(x, y): char
            for y, line in enumerate(util.readlines())
            for x, char in enumerate(line)
            if char != "."
        }

    def read_number(self, pos: util.Position) -> tuple[int, set[util.Position]]:
        """Return the full number at `pos` and all positions it occupies."""
        number = self.grid.get(pos, "")
        if not number.isdigit():
            return None, None
        positions = {pos}
        for dir in (util.Direction.WEST, util.Direction.EAST):
            next_pos = pos + dir
            while True:
                if next_pos not in self.grid:
                    break
                if not self.grid[next_pos].isdigit():
                    break
                if dir == util.Direction.WEST:
                    number = self.grid[next_pos] + number
                else:
                    number = number + self.grid[next_pos]
                positions.add(next_pos)
                next_pos += dir
        return int(number), positions

    def find_part_numbers(self, pos) -> util.Generator[int]:
        """Yield all numbers adjacent to `pos`."""
        seen = set()
        for neighbour in pos.neighbours:
            if neighbour in seen:
                continue
            number, positions = self.read_number(neighbour)
            if number:
                yield number
                seen.update(positions)

    def find_all_part_numbers(self) -> util.Generator[int]:
        """Yield all numbers adjacent to a non-number."""
        for pos, char in self.grid.items():
            if char.isdigit():
                continue
            yield from self.find_part_numbers(pos)

    def find_gear_ratios(self) -> util.Generator[int]:
        """
        Yield the product of the two numbers adjacent to each `*`, where there
        are exactly two numbers adjacent.
        """
        for pos, char in self.grid.items():
            if char == "*":
                numbers = list(self.find_part_numbers(pos))
                if len(numbers) == 2:
                    yield numbers[0] * numbers[1]


if __name__ == "__main__":
    schematic = Schematic()
    print(sum(schematic.find_all_part_numbers()))
    print(sum(schematic.find_gear_ratios()))

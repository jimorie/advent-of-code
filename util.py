from __future__ import annotations

import contextlib
import functools
import itertools
import operator
import os.path
import sys
import typing

from pprint import pprint  # noqa


if typing.TYPE_CHECKING:
    from collections.abc import Callable, Generator, Iterable, Sequence
    from typing import TextIO


@contextlib.contextmanager
def inputfile() -> Generator[TextIO]:
    if len(sys.argv) > 1:
        # Use the provided argument (useful with sample data)
        inputpath = sys.argv[1]
    else:
        if sys.argv and sys.argv[0]:
            # Find inputfile based on executing script
            dirpart, filepart = os.path.split(sys.argv[0])
        else:
            # Find inputfile based on the module calling us (useful with REPL)
            import inspect

            for frame in reversed(inspect.stack()):
                if frame.filename != __file__ and frame.filename != "<stdin>":
                    dirpart, filepart = os.path.split(frame.filename)
                    break
            else:
                raise RuntimeError("No executing script")
        day, _ = os.path.splitext(filepart)
        day = day.rstrip("abcde")
        inputpath = os.path.join(dirpart, "input", day)
    with open(inputpath, "r") as f:
        yield f


def readlines() -> Generator[str]:
    with inputfile() as f:
        return (line.strip("\n") for line in f.readlines())


def read() -> str:
    with inputfile() as f:
        return f.read()


def readchunks() -> Generator[str]:
    with inputfile() as f:
        chunk = ""
        for line in f.readlines():
            if line != "\n":
                chunk += line
            elif chunk:
                yield chunk
                chunk = ""
        if chunk:
            yield chunk


def readlinegroups(lines_per_group) -> Generator[str]:
    group = []
    for line in readlines():
        group.append(line)
        if len(group) >= lines_per_group:
            yield group
            group = []


def readints() -> Generator[int]:
    for line in readlines():
        for n in line.split(","):
            yield int(n)


def readintlines(delimiter=None) -> Generator[list[int]]:
    for line in readlines():
        yield [int(n) for n in line.split(delimiter)]


def prod(numbers: Iterable[int]) -> int:
    return functools.reduce(operator.mul, numbers)


def count(validator: Callable, iterable: Iterable) -> int:
    return sum(1 for item in iterable if item and validator(item))


def unique_product(args: Sequence[Sequence], index: int = 0) -> Generator[tuple]:
    if index >= len(args):
        yield tuple()
    else:
        for suffix in unique_product(args, index + 1):
            for arg in args[index]:
                if arg not in suffix:
                    yield (arg,) + suffix


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def batched(iterable, n):
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(itertools.islice(it, n)):
        yield batch


class Vector(tuple):
    def __new__(cls, *args):
        return super().__new__(cls, args)

    def __add__(self, other: tuple | int) -> Vector:
        if isinstance(other, int):
            return self.__class__(*(a + other for a in self))
        return self.__class__(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other: tuple | int) -> Vector:
        if isinstance(other, int):
            return self.__class__(*(a - other for a in self))
        return self.__class__(*(a - b for a, b in zip(self, other)))

    def __mul__(self, other: tuple | int) -> Vector:
        if isinstance(other, int):
            return self.__class__(*(a * other for a in self))
        return self.__class__(*(a * b for a, b in zip(self, other)))


class Direction(Vector):
    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[1]

    @property
    def z(self) -> int:
        return self[2]

    def rotate(self, rotation: int = 1) -> Direction:
        return self.CARDINALS[
            (self.CARDINALS.index(self) + rotation) % len(self.CARDINALS)
        ]

    def rotation(self, other: Direction) -> int:
        delta = self.CARDINALS.index(other) - self.CARDINALS.index(self)
        if delta > 2:
            delta -= 4
        elif delta < -2:
            delta += 4
        return delta


Direction.EAST = Direction(1, 0, 0)
Direction.SOUTH = Direction(0, 1, 0)
Direction.WEST = Direction(-1, 0, 0)
Direction.NORTH = Direction(0, -1, 0)
Direction.UP = Direction(0, 0, 1)
Direction.DOWN = Direction(0, 0, -1)
Direction.NORTHEAST = Direction.NORTH + Direction.EAST
Direction.SOUTHEAST = Direction.SOUTH + Direction.EAST
Direction.SOUTHWEST = Direction.SOUTH + Direction.WEST
Direction.NORTHWEST = Direction.NORTH + Direction.WEST
Direction.CARDINALS = (Direction.EAST, Direction.SOUTH, Direction.WEST, Direction.NORTH)
Direction.ORDINALS = (
    Direction.SOUTHEAST,
    Direction.SOUTHWEST,
    Direction.NORTHWEST,
    Direction.NORTHEAST,
)
Direction.CARDINALS_3D = Direction.CARDINALS + (Direction.UP, Direction.DOWN)


class Position(Direction):
    def __sub__(self, other: tuple | int) -> Vector:
        if isinstance(other, Position):
            return Direction(self.x - other.x, self.y - other.y, 0)
        return super().__sub__(other)

    @property
    def cardinals(self) -> Generator[Position]:
        for direction in self.CARDINALS:
            yield self + direction

    @property
    def ordinals(self) -> Generator[Position]:
        for direction in self.ORDINALS:
            yield self + direction

    @property
    def neighbours(self) -> Generator[Position]:
        for direction in itertools.product(*((0, 1, -1),) * 2):
            if direction != (0, 0):
                yield self + direction

    @property
    def cardinals_3d(self) -> Generator[Position]:
        for pos in self.cardinals:
            yield pos
        yield self + self.UP
        yield self + self.DOWN

    @property
    def neighbours_3d(self) -> Generator[Position]:
        for direction in itertools.product(*((0, 1, -1),) * 3):
            if direction != (0, 0, 0):
                yield self + direction

    def manhattan_distance(self, other: Position) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class Grid(dict):
    height = None
    width = None

    @classmethod
    def from_iterable(cls, rows, cast=None, ignore=None):
        grid = cls()
        for y, row in enumerate(rows):
            for x, value in enumerate(row):
                if ignore and value in ignore:
                    continue
                if cast:
                    value = cast(value)
                    if value is None:
                        continue
                grid[Position(x, y)] = value
        grid.width = x + 1
        grid.height = y + 1
        return grid

    def index(self, other):
        for pos, value in self.items():
            if value == other:
                return pos
        raise ValueError(f"{other} is not in Grid")

    def is_inside(self, pos: Position):
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    @property
    def inner(self):
        return (
            Position(x, y)
            for y in range(1, self.height - 1)
            for x in range(1, self.width - 1)
        )

    def rotate(self):
        copy = self.copy()
        self.clear()
        for pos, value in copy.items():
            self[Position(self.height - 1 - pos.y, pos.x)] = value
        self.height, self.width = self.width, self.height


OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.floordiv,
    "<": operator.lt,
    ">": operator.gt,
}

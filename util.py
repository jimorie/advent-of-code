import contextlib
import functools
import operator
import os.path
import sys


@contextlib.contextmanager
def inputfile():
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
        day = day.rstrip("ab")
        inputpath = os.path.join(dirpart, "input", day)
    with open(inputpath, "r") as f:
        yield f


def readlines():
    with inputfile() as f:
        return (line.strip() for line in f.readlines())


def read():
    with inputfile() as f:
        return f.read()


def readchunks():
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


def readlinegroups(lines_per_group):
    group = []
    for line in readlines():
        group.append(line)
        if len(group) >= lines_per_group:
            yield group
            group = []


def readints():
    for line in readlines():
        for n in line.split(","):
            yield int(n)


def prod(numbers):
    return functools.reduce(operator.mul, numbers)


def count(validator, iterable):
    return sum(1 for item in iterable if item and validator(item))


def unique_product(args, index=0):
    if index >= len(args):
        yield tuple()
    else:
        for suffix in unique_product(args, index + 1):
            for arg in args[index]:
                if arg not in suffix:
                    yield (arg,) + suffix


class Position(tuple):
    CARDINAL_DIRECTIONS = ((0, 1), (1, 0), (-1, 0), (0, -1))
    ORDINAL_DIRECTIONS = ((1, 1), (1, -1), (-1, -1), (-1, 1))

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    def __new__(cls, *args):
        return super().__new__(cls, args)

    def __add__(self, other):
        return self._apply(other, operator.add)

    def __sub__(self, other):
        return self._apply(other, operator.sub)

    def _apply(self, other, oper):
        return self.__class__(
            *(
                oper(self[i], (other[i] if i < len(other) else 0))
                for i in range(len(self))
            )
        )

    @property
    def cardinals(self):
        for direction in self.CARDINAL_DIRECTIONS:
            yield self + direction

    @property
    def ordinals(self):
        for direction in self.ORDINAL_DIRECTIONS:
            yield self + direction


class Grid:
    def __init__(self, grid):
        self.grid = grid

    def __getitem__(self, pos):
        return self.grid[pos[1]][pos[0]]

    def __setitem__(self, pos, value):
        self.grid[pos[1]][pos[0]] = value

    def __iter__(self):
        return (
            Position(x, y)
            for y in range(len(self.grid))
            for x in range(len(self.grid[y]))
        )

    def __contains__(self, pos):
        return (
            pos[1] >= 0
            and pos[1] < len(self.grid)
            and pos[0] >= 0
            and pos[0] < len(self.grid[pos[1]])
        )

    def items(self):
        return (
            (Position(x, y), self.grid[y][x])
            for y in range(len(self.grid))
            for x in range(len(self.grid[y]))
        )

    def is_edge(self, pos):
        return (
            pos[1] == 0
            or pos[1] == len(self.grid) - 1
            or pos[0] == 0
            or pos[0] == len(self.grid[pos[1]])
        )

    def index(self, other):
        for pos, value in self.items():
            if value == other:
                return pos
        raise ValueError(f"{other} is not in Grid")

    @property
    def height(self):
        return len(self.grid)

    @property
    def width(self):
        return len(self.grid[0]) if self.grid else 0

    @property
    def inner(self):
        return (
            Position(x, y)
            for y in range(1, len(self.grid) - 1)
            for x in range(1, len(self.grid[y]) - 1)
        )

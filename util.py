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


class Vector(tuple):
    def __new__(cls, *args):
        return super().__new__(cls, args)

    def __add__(self, other):
        return self.__class__(*(a + b for a, b in zip(self, other)))

    def __sub__(self, other):
        return self.__class__(*(a - b for a, b in zip(self, other)))


class Position(Vector):
    CARDINAL_DIRECTIONS = ((0, 1), (1, 0), (-1, 0), (0, -1))
    ORDINAL_DIRECTIONS = ((1, 1), (1, -1), (-1, -1), (-1, 1))
    SPACE_DIRECTIONS = (
        (0, 1, 0),
        (1, 0, 0),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    )

    @property
    def x(self):
        return self[0]

    @property
    def y(self):
        return self[1]

    @property
    def z(self):
        return self[2]

    @property
    def cardinals(self):
        for direction in self.CARDINAL_DIRECTIONS:
            yield self + direction

    @property
    def ordinals(self):
        for direction in self.ORDINAL_DIRECTIONS:
            yield self + direction

    @property
    def neighbours_3d(self):
        for direction in self.SPACE_DIRECTIONS:
            yield self + direction


class Grid(dict):
    def __init__(self, rows=None):
        if rows:
            for y, row in enumerate(rows):
                self.height = y
                for x, value in enumerate(row):
                    self[Position(x, y)] = value
                    self.width = x
        else:
            self.height = None
            self.width = None

    def is_edge(self, pos):
        return (
            pos[1] == 0
            or pos[1] == self.height - 1
            or pos[0] == 0
            or pos[0] == self.width - 1
        )

    def index(self, other):
        for pos, value in self.items():
            if value == other:
                return pos
        raise ValueError(f"{other} is not in Grid")

    @property
    def inner(self):
        return (
            Position(x, y)
            for y in range(1, self.height - 1)
            for x in range(1, self.width - 1)
        )

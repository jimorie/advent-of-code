import contextlib
import functools
import operator
import os.path
import sys


@contextlib.contextmanager
def inputfile():
    if not sys.argv or not sys.argv[0]:
        raise RuntimeError("No executing script")
    dirpart, filepart = os.path.split(sys.argv[0])
    day, _ = os.path.splitext(filepart)
    day = day.rstrip("ab")
    with open(os.path.join(dirpart, "input", day), "r") as f:
        yield f


def readlines():
    with inputfile() as f:
        return (line.strip() for line in f.readlines())


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


def readints():
    for line in readlines():
        for n in line.split(","):
            yield int(n)


def prod(numbers):
    return functools.reduce(operator.mul, numbers)


def count(validator, iterable):
    return sum(1 for item in iterable if item and validator(item))

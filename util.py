import functools
import operator
import sys


def readlines():
    return (line.strip() for line in sys.stdin.readlines())


def readints():
    return (int(line.strip()) for line in sys.stdin.readlines())


def readchunks():
    chunk = ""
    for line in sys.stdin.readlines():
        if line != "\n":
            chunk += line
        elif chunk:
            yield chunk
            chunk = ""
    if chunk:
        yield chunk


def prod(numbers):
    return functools.reduce(operator.mul, numbers)


def count(validator, iterable):
    return sum(1 for item in iterable if item and validator(item))

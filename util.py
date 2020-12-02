import functools
import operator
import sys


def readlines():
    return (line.strip() for line in sys.stdin.readlines())


def readints():
    return (int(line.strip()) for line in sys.stdin.readlines())


def prod(numbers):
    return functools.reduce(operator.mul, numbers)

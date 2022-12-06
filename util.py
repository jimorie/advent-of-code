import contextlib
import functools
import operator
import os.path
import sys


@contextlib.contextmanager
def inputfile():
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
    with open(os.path.join(dirpart, "input", day), "r") as f:
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


def readints():
    for line in readlines():
        for n in line.split(","):
            yield int(n)


def prod(numbers):
    return functools.reduce(operator.mul, numbers)


def count(validator, iterable):
    return sum(1 for item in iterable if item and validator(item))

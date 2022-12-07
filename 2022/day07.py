import collections
import pathlib
import util


def parse_terminal():
    cwd = pathlib.Path("/")
    fs = collections.defaultdict(lambda: (set(), dict()))
    dirs, files = fs[cwd]
    for line in util.readlines():
        if line.startswith("$"):
            args = line.split()
            if args[1] == "cd":
                if args[2] == "..":
                    cwd = cwd.parent
                else:
                    cwd = cwd.joinpath(args[2])
            elif args[1] == "ls":
                dirs, files = fs[cwd]
                dirs.clear()
                files.clear()
        else:
            size, name = line.split(" ", 1)
            if size == "dir":
                dirs.add(cwd.joinpath(name))
            else:
                files[name] = int(size)
    return fs


def dirsize(p, fs):
    if p in fs:
        dirs, files = fs[p]
        return sum(files.values()) + sum(dirsize(d, fs) for d in dirs)
    return 0


def dirsizes():
    fs = parse_terminal()
    return {p: dirsize(p, fs) for p in fs}


def find_smallest_to_delete():
    sizes = dirsizes()
    used = sizes[pathlib.Path("/")]
    unused = 70000000 - used
    required = 30000000 - unused
    return min(size for size in sizes.values() if size >= required)


if __name__ == "__main__":
    print(sum(size for size in dirsizes().values() if size <= 100000))
    print(find_smallest_to_delete())

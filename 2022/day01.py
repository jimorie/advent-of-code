import itertools
import util


def read_chunk_sums():
    for chunk in util.readchunks():
        yield sum(int(line) for line in chunk.splitlines())


if __name__ == "__main__":
    print(max(read_chunk_sums()))
    print(sum(itertools.islice(sorted(read_chunk_sums(), reverse=True), 0, 3)))

from __future__ import annotations

import util


def read_code_ranges() -> Generator[range]:
    """Yield all code ranges in the input."""
    for part in util.read().split(","):
        a, b = part.split("-")
        yield range(int(a), int(b) + 1)


def is_valid_1(code: str) -> bool:
    """Return `True` if `code` is valid, else `False`."""
    chunksize = len(code) // 2
    return code[:chunksize] != code[chunksize:]


def is_valid_2(code: str) -> bool:
    """Return `True` if `code` is valid, else `False`."""
    for chunksize in range(len(code) // 2, 0, -1):
        if len(code) % chunksize:
            continue
        if code[:chunksize] * (len(code) // chunksize) == code:
            return False
    return True


def find_invalid(validator: Callable) -> Generator[int]:
    """Yield all invalid codes in the input."""
    for code_range in read_code_ranges():
        for code in code_range:
            if not validator(str(code)):
                yield code


if __name__ == "__main__":
    print(sum(find_invalid(is_valid_1)))
    print(sum(find_invalid(is_valid_2)))

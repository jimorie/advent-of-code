from __future__ import annotations

import collections
import util


def read_records(copies: int = 1) -> tuple[str, list[int]]:
    """
    Yield a tuple of the record and its valid arrangements of broken
    springs for each line in the input.
    """
    for line in util.readlines():
        record, valid = line.split()
        record = "?".join([record] * copies)
        valid = [int(n) for n in valid.split(",")] * copies
        yield record, valid


def count_arrangements(record: str, valid: list[int]) -> int:
    """
    Return the number of `valid` arrangements that can be read from the
    `record`. Implemented as a non-deterministic finite state machine.
    """
    # Define all possible states in our state machine as a string of "#" and
    # "." characters. The "#" state represents a single "#" or "?" character in
    # the `record`, as defined by the `valid` groups. The "." state represents
    # the space between the valid groups (can represent any number of "." or
    # "?" characters in the `record`.
    statemachine: str = "." + ".".join("#" * n for n in valid) + "."

    # Since our state machine is non-deterministic it can progress into
    # multiple new states, therefore we use a dict to keep track of all
    # possible states we could be in (the index of our `statemachine`) and how
    # many paths that led us there. Initialized to the first state with a count
    # of 1.
    states: dict[int, int] = collections.defaultdict(int)
    states[0] = 1

    # Fuel the state machine with the characters in our record
    for c in record:
        # Create a new `states` mapping that we can progress into
        newstates: dict[int, int] = collections.defaultdict(int)

        # Progress each of our current states into new states
        for state, count in states.items():
            # Can we stay in the same state?
            if statemachine[state] == "." and c in "?.":
                newstates[state] += count
            # Can we move to the next state?
            if state + 1 < len(statemachine):
                if c == "?" or c == statemachine[state + 1]:
                    newstates[state + 1] += count

        # Replace the states with the new
        states = newstates

    # Return the number of paths that led us to the last (or next to last if
    # the arrangement ended with a "#") state
    return states[len(statemachine) - 1] + states[len(statemachine) - 2]


if __name__ == "__main__":
    print(
        sum(
            count_arrangements(record, valid)
            for record, valid in read_records(copies=1)
        )
    )
    print(
        sum(
            count_arrangements(record, valid)
            for record, valid in read_records(copies=5)
        )
    )

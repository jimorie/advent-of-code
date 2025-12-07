from __future__ import annotations

import itertools
import functools
import re

import util


def read_problems() -> list:
    *lines, operators = util.readlines()
    operators = re.findall(r"[^\s]\s*", operators)
    col_indices = [0, *itertools.accumulate(len(col) for col in operators)]
    return list(
        zip(
            [util.OPERATORS.get(operator.strip()) for operator in operators],
            *[
                tuple(line[i:j] for i, j in zip(col_indices, col_indices[1:]))
                for line in lines
            ],
        )
    )


def reread_problems(problems: list) -> list:
    return [
        (operator, *("".join(value) for value in zip(*values)))
        for operator, *values in problems
    ]


def solve_problem(problem: tuple) -> int:
    operator, *values = problem
    return functools.reduce(
        operator, (int(value) for value in values if len(value.strip()))
    )


if __name__ == "__main__":
    problems = read_problems()
    print(sum(solve_problem(problem) for problem in problems))
    print(sum(solve_problem(problem) for problem in reread_problems(problems)))

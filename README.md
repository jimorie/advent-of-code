# Advent of Code

My solutions to [Advent of Code](https://adventofcode.com/).

All solutions are written for Python 3.9+ and use only standard library utilities.

All solution files can be executed without arguments on the command line. The script will try to find a matching input file under the `input` directory relative to the script. E.g. `./2023/day01.py` will try to read `./2023/input/day01`.

    $ python3 2023/day01.py
    55002
    55093

You can also specify the input file as an extra argument:

    $ python3 2023/day04.py example
    13
    30

## util.py

The `util.py` module contains common helper functions used in the solutions.

## download.py

The `download.py` script can be used to download input files from [adventofcode.com](https://adventofcode.com/). It requires an active session key ot be stored in the `sessionkey` file.

The script will also create a template for the solution file if non already exists.

    $ python3 download.py 2023 10
    Fetching input file /Users/pnystrom/Projects/advent-of-code/2023/input/day10
    Writing empty solution file /Users/pnystrom/Projects/advent-of-code/2023/day10.py

## runall.py

The `runall.py` script can be used to execute all solution files in the repo (that there are input files for):

    $ python3 runall.py
    day01a.py: 888331
        (0.005 s)
    day01b.py: 130933530
        (0.102 s)
    day02a.py: 378
        (0.004 s)
    day02b.py: 280
        (0.006 s)
    day03a.py: 195
        (0.001 s)
    ...

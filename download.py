import argparse
import pathlib
import sys
import urllib.request


if __name__ == "__main__":
    try:
        year = int(sys.argv[1])
        day = int(sys.argv[2])
    except (IndexError, ValueError):
        raise SystemExit(f"Usage: {sys.argv[0]} <year> <day>")
    try:
        sessionkey = pathlib.Path(__file__).parent.joinpath("sessionkey").read_text().strip()
    except FileNotFoundError:
        raise SystemExit("Missing sessionkey file")
    request = urllib.request.Request(
        f"https://adventofcode.com/{year}/day/{day}/input",
        headers={"Cookie": f"session={sessionkey}"},
    )
    response = urllib.request.urlopen(request)
    year_dir = pathlib.Path(__file__).parent / str(year)
    day_padded = f"day{day:02}"
    input_path = year_dir / "input" / day_padded
    input_path.parent.mkdir(parents=True, exist_ok=True)
    input_path.write_bytes(response.read())
    print(f"Fetching input file {input_path}")
    py_path = year_dir / f"{day_padded}.py"
    if not py_path.exists():
        print(f"Writing empty solution file {py_path}")
        py_path.write_text(
"""from __future__ import annotations

import util


if __name__ == "__main__":
    print()
"""
            )


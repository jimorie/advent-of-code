from __future__ import annotations

import math
import util


def read_games() -> Generator[tuple[str, list[dict[str, int]]]]:
    """Yield all games in the input."""
    for line in util.readlines():
        yield parse_game(line)


def parse_game(line: str) -> tuple[str, list[dict[str, int]]]:
    """Return a tuple with a game ID and a list of dicts with the revealed data."""
    game, line = line.split(": ")
    revealed = [
        dict(parse_item(item) for item in reveal.split(", "))
        for reveal in line.split("; ")
    ]
    return (int(game[len("Game ") :]), revealed)


def parse_item(item: str) -> tuple[str, int]:
    """Return a tuple with the color and its count."""
    count, color = item.split(" ")
    return (color, int(count))


def validate(maxes: dict) -> util.Generator[int]:
    """
    Yield the IDs of the games in the input that are possible with the given
    maxes.
    """
    for game, revealed in read_games():
        if any(
            any(reveal[color] > count for reveal in revealed if color in reveal)
            for color, count in maxes.items()
        ):
            continue
        yield game


def powers(colors: list[str]) -> util.Generator[int]:
    """
    Yield the product of the maximum revealed number of all colors for each
    game in the input.
    """
    for _, revealed in read_games():
        yield math.prod(
            max(reveal[color] for reveal in revealed if color in reveal)
            for color in colors
        )


if __name__ == "__main__":
    print(sum(validate({"red": 12, "green": 13, "blue": 14})))
    print(sum(powers(["red", "green", "blue"])))

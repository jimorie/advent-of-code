import math
import util


def parse_game(line):
    game, line = line.split(": ")
    revealed = line.split("; ")
    game = int(game[len("Game "):])

    def parse_item(item):
        count, color = item.split(" ")
        return (color, int(count))

    revealed = [
        dict(
            parse_item(item)
            for item in reveal.split(", ")
        )
        for reveal in revealed
    ]
    return (game, revealed)


def read_games():
    for line in util.readlines():
        yield parse_game(line)


def validate(maxes):
    for game, revealed in read_games():
        if any(
            any(
                reveal[color] > count
                for reveal in revealed if color in reveal
            )
            for color, count in maxes.items()
        ):
            continue
        yield game


def powers(colors):
    for _, revealed in read_games():
        yield math.prod(
            max(
                reveal[color]
                for reveal in revealed if color in reveal
            )
            for color in colors
        )


if __name__ == "__main__":
    print(sum(validate({"red": 12, "green": 13, "blue": 14})))
    print(sum(powers(["red", "green", "blue"])))

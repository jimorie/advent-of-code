import day05a
import util


def find_empty_seat(tickets):
    seats = sorted(day05a.seatid(ticket) for ticket in tickets)
    for i in range(1, len(seats)):
        if seats[i] == seats[i - 1] + 2:
            return seats[i] - 1
    raise SystemExit("No empty seat found.")


if __name__ == "__main__":
    print(find_empty_seat(util.readlines()))

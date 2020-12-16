import util


def rownum(rowcode):
    return int(rowcode.replace("F", "0").replace("B", "1"), 2)


def seatnum(seatcode):
    return int(seatcode.replace("L", "0").replace("R", "1"), 2)


def seatid(ticket):
    i = max(ticket.rfind("F"), ticket.rfind("B")) + 1
    return rownum(ticket[:i]) * 2 ** (len(ticket) - i) + seatnum(ticket[i:])


if __name__ == "__main__":
    print(max(seatid(ticket) for ticket in util.readlines()))

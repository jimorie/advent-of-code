import collections
import util


def read_numbers():
    return [(i, int(line)) for i, line in enumerate(util.readlines())]


def decrypt_numbers(numbers, repeat=1, decrypt_key=1):
    mixed = collections.deque(numbers)
    for _ in range(repeat):
        # Loop over the unique (index, value) items in original order
        for item in numbers:
            # Rotate the next item to mix into head position
            mixed.rotate(-mixed.index(item))
            # Pop the item, then rotate the item's new position into head position
            mixed.rotate(-mixed.popleft()[1] * decrypt_key)
            # Insert the item at it's mixed position
            mixed.appendleft(item)
    # Find the index of the item with value 0 and return the solution from there
    for i in range(len(mixed)):
        if mixed[i][1] == 0:
            return sum(
                mixed[(i + n) % len(mixed)][1] * decrypt_key for n in [1000, 2000, 3000]
            )


if __name__ == "__main__":
    numbers = read_numbers()
    print(decrypt_numbers(numbers))
    print(decrypt_numbers(numbers, repeat=10, decrypt_key=811589153))

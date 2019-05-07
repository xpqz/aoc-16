from itertools import count, cycle
import re

class Disc:
    def __init__(self, size, startpos):
        self.size = size
        self.data = cycle(range(size))
        self.current = -1
        while self.current != startpos:
            self.current = next(self.data)

    def move(self):
        self.current = next(self.data)
        return self.current

def read_data(filename="data/input15.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    d = [
        [int(n) for n in re.findall(r"-?\d+", l)]
        for l in lines
    ]
    return [Disc(a[1], a[3]) for a in d]

def tick(discs):
    return [d.move() for d in discs]

def find_time(discs):
    end_state = [
        (disc.size - index) % disc.size
        for index, disc in enumerate(discs)
    ]

    for time in count():
        if tick(discs) == end_state:
            break

    return time

if __name__ == "__main__":
    lines = read_data()

    print(find_time(parse_data(lines)))
    print(find_time(parse_data(lines) + [Disc(11, 0)]))

import sys
from collections import defaultdict

def read_data(filename="data/input01.data"):
    with open(filename) as f:
        data = f.read().strip().split(", ")
    return [(l[0], int(l[1:])) for l in data]

def move(pos, heading, step):
    turns = {
        ("N", "R"): ("E", (1, 0)),
        ("N", "L"): ("W", (-1, 0)),
        ("E", "R"): ("S", (0, -1)),
        ("E", "L"): ("N", (0, 1)),
        ("S", "R"): ("W", (-1, 0)),
        ("S", "L"): ("E", (1, 0)),
        ("W", "R"): ("N", (0, 1)),
        ("W", "L"): ("S", (0, -1)),
    }

    (new_heading, delta) = turns[(heading, step[0])]

    return (pos[0] + delta[0]*step[1], pos[1] + delta[1]*step[1]), new_heading

def visited(current, previous):
    if current[0] == previous[0]:
        step = 1 if current[1] >= previous[1] else -1
        return ((current[0], y) for y in range(previous[1], current[1], step))

    step = 1 if current[0] >= previous[0] else -1
    return ((x, current[1]) for x in range(previous[0], current[0], step))


if __name__ == "__main__":

    pos = (0, 0)
    heading = "N"

    d = read_data()
    for step in d:
        pos, heading = move(pos, heading, step)

    print(abs(pos[0]) + abs(pos[1]))

    pos = (0, 0)
    heading = "N"
    c = defaultdict(int)
    for step in d:
        new_pos, heading = move(pos, heading, step)
        for v in visited(new_pos, pos):
            c[v] += 1
            if c[v] > 1:
                print(abs(v[0]) + abs(v[1]))
                sys.exit()
        pos = new_pos

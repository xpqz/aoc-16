def read_data(filename="data/input02.data"):
    with open(filename) as f:
        return [list(l) for l in f.read().splitlines()]

def move(current, direction):
    return [
        {},
        {"U": 1, "D": 4, "L": 1, "R": 2},
        {"U": 2, "D": 5, "L": 1, "R": 3},
        {"U": 3, "D": 6, "L": 2, "R": 3},
        {"U": 1, "D": 7, "L": 4, "R": 5},
        {"U": 2, "D": 8, "L": 4, "R": 6},
        {"U": 3, "D": 9, "L": 5, "R": 6},
        {"U": 4, "D": 7, "L": 7, "R": 8},
        {"U": 5, "D": 8, "L": 7, "R": 9},
        {"U": 6, "D": 9, "L": 8, "R": 9}
    ][current][direction]

def move2(current, direction):
    return {
        1: {"D": 3},
        2: {"D": 6, "R": 3},
        3: {"U": 1, "D": 7, "L": 2, "R": 4},
        4: {"D": 8, "L": 3},
        5: {"R": 6},
        6: {"U": 2, "D": "A", "L": 5, "R": 7},
        7: {"U": 3, "D": "B", "L": 6, "R": 8},
        8: {"U": 4, "D": "C", "L": 7, "R": 9},
        9: {"L": 8},
        "A": {"U": 6, "R": "B"},
        "B": {"U": 7, "D": "D", "L": "A", "R": "C"},
        "C": {"U": 8, "L": "B"},
        "D": {"U": "B"}
    }[current].get(direction, current)

def code(data, start, movefn):
    current = start
    result = []
    for row in data:
        for m in row:
            current = movefn(current, m)
        result.append(current)

    return result


if __name__ == "__main__":
    d = read_data()
    print("".join(str(i) for i in code(d, 5, move)))
    print("".join(str(i) for i in code(d, 5, move2)))

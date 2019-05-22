import re

def read_data(filename="data/input20.data"):
    with open(filename) as f:
        return f.read().splitlines()


def parse_data(lines):
    return sorted([
        tuple(int(n) for n in re.findall(r"\d+", l))
        for l in lines
    ], key=lambda x: x[0])

def overlaps(rng_a, rng_b):
    if rng_a[1] >= rng_b[0]-1 and rng_b[1] >= rng_a[0]:
        return (rng_a[0], max(rng_a[1], rng_b[1]))
    return None

def lowest_allowed(ranges):
    a = ranges[0]
    for i in range(1, len(ranges)):
        b = ranges[i]
        c = overlaps(a, b)
        if c is None:
            break
        a = c

    return a[1]+1


def total_allowed(ranges):
    count = 0
    a = ranges[0]
    for i in range(1, len(ranges)):
        b = ranges[i]
        c = overlaps(a, b)
        if c is None:
            count += b[0] - (a[1] + 1)
            a = b
        else:
            a = c

    return count

if __name__ == "__main__":
    data = read_data()
    blacklist = parse_data(data)
    print(lowest_allowed(blacklist))
    print(total_allowed(blacklist))

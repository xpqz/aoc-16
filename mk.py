import sys

def lines(name):
    return f"""def read_data(filename="data/input{name}.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    return lines

if __name__ == "__main__":
    lines = read_data()

    data = parse_data(lines)

    print(data)
"""


def ints(name):
    return f"""import re

def read_data(filename="data/input{name}.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    return [
        [int(n) for n in re.findall(r"-?\d+", l)]
        for l in lines
    ]

if __name__ == "__main__":
    lines = read_data()

    data = parse_data(lines)

    print(data)
"""

if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(lines(sys.argv[0]))
    else:
        print(ints(sys.argv[0]))

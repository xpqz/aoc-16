from itertools import cycle, islice
import re

def read_data(filename="data/input09.data"):
    with open(filename) as f:
        return f.read().splitlines()

def ffwd(s, pos, ch):
    start = pos
    try:
        while s[pos] != ch:
            pos += 1
    except IndexError:
        pos = len(s)

    return pos, s[start:pos]

def expand(s):
    pos = 0
    while True:
        if pos >= len(s):
            break

        pos, data = ffwd(s, pos, "(")
        yield data

        if pos >= len(s):
            break

        pos, data = ffwd(s, pos, ")")
        chars, repeat = (int(n) for n in re.findall(r"-?\d+", data))

        yield s[pos:pos+chars] * repeat

        pos += 1



if __name__ == "__main__":
    data = read_data()

    data = [
        # "ADVENT",
        "A(1x5)BC",
        # "(3x3)XYZ",
        # "A(2x2)BCD(2x2)EFG",
        # "(6x1)(1x3)A",
        # "X(8x2)(3x3)ABCY"
    ]

    for i in data:
        for s in expand(i):
            print(s, end="")
        print()

import re

def read_data(filename="data/input09.data"):
    with open(filename) as f:
        return f.read().splitlines()

def expand(s):
    while True:
        try:
            ch = next(s)
            while ch != "(":
                yield ch
                ch = next(s)
        except StopIteration:
            break

        spec = ""
        while ch != ")":
            spec += ch
            ch = next(s)

        chars, repeat = (int(n) for n in re.findall(r"-?\d+", spec))

        data = ""
        while chars:
            data += next(s)
            chars -= 1
        yield data * repeat

if __name__ == "__main__":
    data = read_data()
    total = 0
    for i in expand(iter(data[0])):
        total += len(i)
    print(total)
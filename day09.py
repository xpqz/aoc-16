import re

def read_data(filename="data/input09.data"):
    with open(filename) as f:
        return f.read().splitlines()[0]

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

def length(s):

    if s == "":
        return 0

    total = 0

    pos = 0
    while pos < len(s):
        ch = s[pos]
        try:
            while ch != "(":
                total += 1
                pos += 1
                ch = s[pos]

            pos += 1
        except IndexError:
            break

        spec = ""
        while ch != ")":
            spec += ch
            ch = s[pos]
            pos += 1

        spec += s[pos]

        chars, repeat = (int(n) for n in re.findall(r"-?\d+", spec))

        total += length(s[pos:pos+chars]) * repeat

        pos += chars

    return total

if __name__ == "__main__":
    data = read_data()
    total = 0
    for i in expand(iter(data)):
        total += len(i)
    print(total)
    print(length(data))

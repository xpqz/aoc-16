from itertools import cycle, islice
import re

def read_data(filename="data/input08.data"):
    with open(filename) as f:
        return f.read().splitlines()

def rol(l, c):
    return list(islice(cycle(l), c, len(l)+c))

def ror(l, c):
    return list(reversed(list((islice(cycle(reversed(l)), c, len(l)+c)))))

def trn(l):
    return [*map(list, zip(*l))]

def matr(xsize, ysize, value=0):
    return [[value for _ in range(xsize)] for _ in range(ysize)]

def rect(m, xsize, ysize):
    for y in range(ysize):
        for x in range(xsize):
            m[y][x] = 1

def d(m):
    for y, row in enumerate(m):
        for x, value in enumerate(row):
            if value == 1:
                print("#", end="")
            else:
                print(".", end="")
        print()

def lit(m):
    return sum(list(map(sum, m)))

if __name__ == "__main__":
    data = read_data()
    matrix = matr(50, 6)

    for line in data:
        components = line.split(" ")
        if components[0] == "rect":
            x, y = (int(n) for n in re.findall(r"-?\d+", line))
            rect(matrix, x, y)
        elif components[0] == "rotate":
            elem, count = (int(n) for n in re.findall(r"-?\d+", line))
            if components[1] == "row":
                matrix[elem] = ror(matrix[elem], count)
            else:
                matrix = trn(matrix)
                matrix[elem] = ror(matrix[elem], count)
                matrix = trn(matrix)

    print(lit(matrix))
    print(d(matrix))

from functools import reduce
from itertools import islice
import re

def read_data(filename="data/input03.data"):
    with open(filename) as f:
        return [
            [int(n) for n in re.findall(r"-?\d+", l)]
            for l in f.read().splitlines()
        ]

def t(r):
    a, b, c = r
    return int((a + b > c) and (a + c > b) and (b + c > a))

def chunk(arr, n):
    itr = iter(arr)
    item = list(islice(itr, n))
    while item:
        yield item
        item = list(islice(itr, n))

def transpose(arr):
    return [*zip(*arr)]

def valid_triangles(data):
    return reduce(lambda a, r: a+t(r), data, 0)

if __name__ == "__main__":
    d = read_data()
    print(valid_triangles(d))
    print(reduce(lambda a, c: a+valid_triangles(transpose(c)), chunk(d, 3), 0))
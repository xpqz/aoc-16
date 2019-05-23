from dataclasses import dataclass
from itertools import product
import re
from typing import Tuple

@dataclass
class Node:
    pos: Tuple[int, int]
    size: int
    used: int
    avail: int

def read_data(filename="data/input22.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    nodes = []
    for row in lines[2:]:
        ints = [int(n) for n in re.findall(r"-?\d+", row)]
        nodes.append(Node(
            pos=(ints[0], ints[1]),
            size=ints[2],
            used=ints[3],
            avail=ints[4]
        ))
    return nodes

def is_viable_pair(pair):
    a, b = pair
    return int(a.used > 0 and a != b and a.used <= b.avail)

if __name__ == "__main__":
    lines = read_data()
    nodes = parse_data(lines)
    print(sum(map(is_viable_pair, product(nodes, nodes))))

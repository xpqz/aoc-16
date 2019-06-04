
"""
This problem divides into two parts:

1. Create a costed, fully connected graph of the numbered nodes.
Costs are the lengths of the shortest paths in the maze.
2. Find the cheapest Hamiltonian path, starting at node 0.

For (1) we repeatedly apply the a* search algorithm, using the
manhattan distance as the heuristic.
For (2) we find the MST, and do a pre-order traversal, visiting
child nodes in order of number of children and edge cost.
"""
from collections import defaultdict
from graph import a_star_search, manhattan, prim_mst


def read_data(filename="data/input24.data"):
    with open(filename) as f:
        return f.read().splitlines()


def parse_data(lines):
    """
    Create an adjacency graph from the input data and a set of the numbered nodes
    with positions.
    """
    walls = set()
    nodes = {}
    graph = {}
    for y, row in enumerate(lines):
        for x, ch in enumerate(row):
            if ch == ".":
                continue
            pos = (x, y)
            if ch == "#":
                walls.add(pos)
            else:
                nodes[int(ch)] = pos

    for y, row in enumerate(lines):
        for x, ch in enumerate(row):
            if ch == "#":
                continue

            graph[x, y] = [
                pos for pos in [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
                if pos not in walls
            ]

    return graph, nodes

def traverse_mst(costed_graph, tree, node):
    """
    Visit all nodes in pre-order of (number of children, cost)
    """
    yield node

    child_nodes = []
    for n in tree[node]:
        ch_count = len(tree[n])
        cost = costed_graph[node][n]
        child_nodes.append((ch_count, cost, n))

    for _, _, n in sorted(child_nodes):
        yield from traverse_mst(costed_graph, tree, n)

def path_cost(costed_graph, path):
    total = 0
    for i in range(len(path)-1):
        total += costed_graph[path[i]][path[i+1]]
    return total

def weighted_graph(adj_graph, nodes):
    g = defaultdict(dict)
    for node1, pos1 in nodes.items():
        for node2, pos2 in nodes.items():
            if pos1 == pos2:
                continue
            cost = len(a_star_search(adj_graph, pos1, pos2, manhattan))
            g[node1][node2] = cost
    return g


if __name__ == "__main__":
    lines = read_data()

    g = weighted_graph(*parse_data(lines))

    minimal_spanning_tree = prim_mst(g, 0)

    cheapest_path = list(traverse_mst(g, minimal_spanning_tree, 0))

    cost = path_cost(g, cheapest_path)

    print(cost)

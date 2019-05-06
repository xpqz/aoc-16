import sys

def imports():
    return """import heapq
import re
"""

def lines(name):
    return f"""def read_data(filename="data/input{name}.data"):
    with open(filename) as f:
        return f.read().splitlines()
"""

def ints():
    return """def parse_data(lines):
    return [
        [int(n) for n in re.findall(r"-?\d+", l)]
        for l in lines
    ]
"""

def driver():
    return """if __name__ == "__main__":
    lines = read_data()

    data = parse_data(lines)

    print(data)
"""

def dijkstra():
    return """def neighbours(node):
    x, y = node
    for p in {(x-1, y), (x+1, y), (x, y-1), (x, y+1)}:
        if p[0] >= 0 and p[1] >= 0:
            yield p

def dijkstra(start, end):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]

        if current == end:
            break

        for neighbour in neighbours(current):
            new_cost = cost_so_far[current] + 1  # cost of 1
            if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                cost_so_far[neighbour] = new_cost
                heapq.heappush(frontier, (new_cost, neighbour))
                came_from[neighbour] = current

    current = end
    path = []

    while current != start:
        path.append(current)
        current = came_from[current]

    path.append(start)
    path.reverse()

    return path
"""

if __name__ == "__main__":

    print(imports())
    print()
    print(lines(sys.argv[0]))
    print()
    print(ints())
    print()
    print(dijkstra())
    print()
    print(driver())

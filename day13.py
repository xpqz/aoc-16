import heapq

def kind(x, y):
    magic = 1364
    return ["#", "."][int(bin(x*x + 3*x + 2*x*y + y + y*y + magic).count("1")%2==0)]

def neighbours(x, y):
    for p in {(x-1, y), (x+1, y), (x, y-1), (x, y+1)}:
        if p[0] >= 0 and p[1] >= 0 and kind(p[0], p[1]) == ".":
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

        for neighbour in neighbours(current[0], current[1]):
            new_cost = cost_so_far[current] + 1
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


def dijkstra2(start, max_distance=50):
    """
    Unique points reachable at 50 steps or fewer.
    """
    frontier = []
    heapq.heappush(frontier, (0, start))
    cost_so_far = {start: 0}

    while frontier:
        current = heapq.heappop(frontier)[1]
        for neighbour in neighbours(current[0], current[1]):
            new_cost = cost_so_far[current] + 1
            if new_cost <= max_distance:
                if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                    cost_so_far[neighbour] = new_cost
                    heapq.heappush(frontier, (new_cost, neighbour))

    return set(cost_so_far.keys())

if __name__ == "__main__":
    path = dijkstra((1, 1), (31, 39))
    print(len(path)-1)  # skip start point
    print(len(dijkstra2((1, 1))))

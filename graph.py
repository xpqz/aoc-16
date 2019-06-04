
from collections import defaultdict
from dataclasses import dataclass, field
from heapq import heappush, heappop, heapify
from queue import PriorityQueue
from typing import Any


def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

@dataclass(order=True)
class QueueItem:
    priority: int
    item: Any = field(compare=False)


def a_star_search(graph, start, end, heuristic):
    frontier = []
    frontier = PriorityQueue()
    frontier.put(QueueItem(heuristic(start, end), start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while not frontier.empty():
        current = frontier.get().item
        if current == end:
            break

        for state in graph[current]:
            new_cost = cost_so_far[current] + 1  # uniform step cost of 1
            if state not in cost_so_far or new_cost < cost_so_far[state]:
                cost_so_far[state] = new_cost
                frontier.put(QueueItem(new_cost + heuristic(state, end), state))
                came_from[state] = current
    else:  #  nobreak
        return []

    current = end
    path = []

    while current != start:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return path

def prim_mst(graph, start):
    mst = defaultdict(set)
    visited = set([start])
    edges = [
        (cost, start, to)
        for to, cost in graph[start].items()
    ]
    heapify(edges)

    while edges:
        cost, frm, to = heappop(edges)
        if to not in visited:
            visited.add(to)
            mst[frm].add(to)
            for to_next, cost in graph[to].items():
                if to_next not in visited:
                    heappush(edges, (cost, to, to_next))

    return mst

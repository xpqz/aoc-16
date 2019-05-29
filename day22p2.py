"""
This probem is not quite what it might seem at a cursory look.

With a few assumptions, the dimensionality can be reduced:

1. A single node exists that has 0 usage.
2. We only need to consider moves that involve this empty node.
3. A set of large nodes exist that form "barriers" to be avoided.

The graph/grid now has very few nodes of actual interest:

 T.............................G
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 .....##########################
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 ...............................
 .............E.................
 ...............................
 ...............................
 ...............................

The solution is clearly visible, and derivable by hand.

However -- let's a-star it.
"""
from dataclasses import dataclass, field
from typing import Any, Set, Tuple
from queue import PriorityQueue
import re


@dataclass(frozen=True)
class Context:
    unmovables: Set[Tuple[int, int]]
    xsize: int
    ysize: int


def read_data(filename="data/input22.data"):
    with open(filename) as f:
        return f.read().splitlines()


def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])


def parse_data(lines, unmovable):
    xsize, ysize = 0, 0
    unmovables = set()

    for row in lines[2:]:
        ints = [int(n) for n in re.findall(r"-?\d+", row)]
        xpos, ypos, used = ints[0], ints[1], ints[3]

        if xpos > xsize:
            xsize = xpos
        if ypos > ysize:
            ysize = ypos

        if used == 0:
            empty = (xpos, ypos)
        elif used > unmovable:
            unmovables.add((xpos, ypos))

    g = Grid(goal=(xsize, 0), empty=empty)
    ctx = Context(unmovables=unmovables, xsize=xsize, ysize=ysize)

    return g, ctx


@dataclass(frozen=True)
class Grid:
    goal: Tuple[int, int]
    empty: Tuple[int, int]

    def _move(self, to_node):
        if to_node == self.goal:
            return Grid(goal=self.empty, empty=to_node)
        return Grid(goal=self.goal, empty=to_node)

    def heuristic(self):
        """
        We want to minimise the sum distance of the goal to the target and the empty
        to the goal.
        """
        return manhattan(self.empty, self.goal) + manhattan(self.goal, (0, 0))

    def neighbours(self, ctx):
        for pos in self._valid_moves(ctx):
            yield self._move(pos)

    def _valid_moves(self, ctx):
        for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            n = (self.empty[0] + delta[0], self.empty[1] + delta[1])
            if (
                    0 <= n[0] <= ctx.xsize and
                    0 <= n[1] <= ctx.ysize and
                    n not in ctx.unmovables
            ):
                yield n


@dataclass(order=True)
class QueueItem:
    priority: int
    item: Any = field(compare=False)


def a_star_search(start, ctx):
    frontier = []
    frontier = PriorityQueue()
    frontier.put(QueueItem(start.heuristic(), start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    end = None

    while not frontier.empty():
        current = frontier.get().item
        if current.goal == (0, 0):
            end = current
            break

        for state in current.neighbours(ctx):
            new_cost = cost_so_far[current] + 1  # uniform edge cost of 1
            if state not in cost_so_far or new_cost < cost_so_far[state]:
                cost_so_far[state] = new_cost
                frontier.put(QueueItem(new_cost + state.heuristic(), state))
                came_from[state] = current

    current = end
    path = []

    while current != start:
        path.append(current)
        current = came_from[current]

    # path.append(start)
    path.reverse()

    return path


if __name__ == "__main__":
    lines = read_data()
    unmovable = 400

    grid, ctx = parse_data(lines, unmovable)
    path = a_star_search(grid, ctx)

    print(len(path))

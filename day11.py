from collections import deque
from itertools import chain, combinations
from more_itertools import partition

def elm(f):
    e = []
    for row in f[0]:
        e.extend(row)
    return sorted(e)

def is_microchip(s):
    return s[1] == "M"

def chip_to_generator(chip):
    assert is_microchip(chip)
    return chip[0]+"G"

def is_valid_state(state):
    generators, chips = partition(is_microchip, state)

    chips = set(chips)
    generators = set(generators)

    # Each chip needs a corresponding generator unless there are
    # no generators.
    if not generators or not chips:
        return True

    for c in chips:
        if chip_to_generator(c) not in generators:
            return False

    return True


def allowed_in_elevator(move):
    """
    Valid: single element, two chips, two generators, chip + matching generator
    """
    if not move[0] or not move[1]:  # Single element
        return True

    if is_microchip(move[0]) and is_microchip(move[1]):   # Two chips
        return True

    if not is_microchip(move[0]) and not is_microchip(move[1]):   # Two generators
        return True

    # chip + matching generator
    if is_microchip(move[0]) and move[1] == chip_to_generator(move[0]):
        return True

    if is_microchip(move[1]) and move[0] == chip_to_generator(move[1]):
        return True

    return False

def floors(setlist, elevator=0):
    return (tuple(frozenset(l) for l in setlist), elevator)

def display(f):
    data, elevator = f
    elements = elm(f)
    for row in [3, 2, 1, 0]:
        if elevator == row:
            print(f"F{row+1} E  ", end="")
        else:
            print(f"F{row+1} .  ", end="")
        for e in elements:
            if e in data[row]:
                print(f"{e} ", end="")
            else:
                print(".  ", end="")
        print()

def state(f, floor, move, remove=False):
    data = f[0]

    if remove:
        return frozenset(data[floor] - set(move))

    return frozenset({e for e in chain(data[floor], move) if e is not None})

def valid_moves(f):
    """
    Elevator can move one or two items up or down one step, but both
    start and destination floors must always be in a stable state, as
    must the elevator itself.
    """
    data, elevator = f
    valid = set()
    available_floors = [f for f in [elevator-1, elevator+1] if f >= 0 and f < 4]
    for move in combinations({*data[elevator], None}, 2):
        if not allowed_in_elevator(move):
            continue
        start_state = state(f, elevator, move, remove=True)
        if not is_valid_state(start_state):
            continue
        for floor in available_floors:
            target_state = state(f, floor, move)
            if is_valid_state(target_state):
                valid.add((floor, move))

    return valid

def move(f, m):
    """
    m is assumed to be valid.
    Return a new state
    """
    current_data, current_elevator = f
    new_elevator, moving_items = m[0], set(m[1])

    new_data = []

    for i, row in enumerate(current_data):
        if i == current_elevator:
            new_data.append(state(f, i, moving_items, remove=True))
        elif i == new_elevator:
            new_data.append(state(f, i, moving_items))
        else:
            new_data.append(row)

    return (tuple(new_data), new_elevator)


def breadth_first_search(start):
    frontier = deque([start])
    came_from = {start: None}
    end = floors([{}, {}, {}, set(elm(f))], 3)

    while frontier:
        current = frontier.popleft()
        if current == end:
            break

        for m in valid_moves(current):
            new_state = move(current, m)
            if new_state not in came_from:
                frontier.append(new_state)
                came_from[new_state] = current

    current = end
    path = []

    while current != start:
        path.append(current)
        current = came_from[current]

    path.reverse()

    return path


if __name__ == "__main__":
    f = floors([
        {"SG", "SM", "PG", "PM"},         # F1
        {"TG", "RG", "RM", "CG", "CM"},   # F2
        {"TM"},                           # F3
        {}                                # F4
    ])

    seq = breadth_first_search(f)

    print(len(seq))

    # Part 2: more elements on F1. THIS TAKES A WHILE!
    f = floors([
        {"SG", "SM", "PG", "PM", "EG", "EM", "DG", "DM"},   # F1
        {"TG", "RG", "RM", "CG", "CM"},                     # F2
        {"TM"},                                             # F3
        {}                                                  # F4
    ])

    seq = breadth_first_search(f)
    print(len(seq))

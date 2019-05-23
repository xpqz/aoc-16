from itertools import islice, cycle
import re

def read_data(filename="data/input21.data"):
    with open(filename) as f:
        return f.read().splitlines()

def process_instructions(lines, l):
    rotate_abs = re.compile(r"^rotate (left|right) (\d+) steps?$")
    rotate_rel = re.compile(r"^rotate based on position of letter (.)$")
    switch_rel = re.compile(r"^swap letter (.) with letter (.)$")
    switch_abs = re.compile(r"^swap position (\d+) with position (\d+)")
    rev = re.compile(r"^reverse positions (\d+) through (\d+)$")
    move_pos = re.compile(r"^move position (\d+) to position (\d+)$")

    for line in lines:
        m = rotate_abs.match(line)
        if m:
            if m.group(1) == "left":
                l = rotate_left(l, int(m.group(2)))
            else:
                l = rotate_right(l, int(m.group(2)))
            continue

        m = rotate_rel.match(line)
        if m:
            l = rotate_right_by_index(l, m.group(1))
            continue

        m = switch_rel.match(line)
        if m:
            l = swap_letters(l, m.group(1), m.group(2))
            continue

        m = switch_abs.match(line)
        if m:
            l = swap_position(l, int(m.group(1)), int(m.group(2)))
            continue

        m = rev.match(line)
        if m:
            l = reverse_span(l, int(m.group(1)), int(m.group(2)))
            continue

        m = move_pos.match(line)
        if m:
            l = move_position(l, int(m.group(1)), int(m.group(2)))
            continue

    return l

def swap_position(l, x, y):
    l[x], l[y] = l[y], l[x]
    return l

def swap_letters(l, a, b):
    return swap_position(l, l.index(a), l.index(b))

def rotate_left(l, steps):
    return list(islice(cycle(l), steps, len(l)+steps))

def rotate_right(l, steps):
    return list(reversed(rotate_left(list(reversed(l)), steps)))

def rotate_right_by_index(l, a):
    steps = l.index(a)
    return rotate_right(l, 1 + steps + int(steps >= 4))

def reverse_span(l, x, y):
    x, y = min(x, y), max(x, y)
    return l[:x] + list(reversed(l[x:y+1])) + l[y+1:]

def move_position(l, x, y):
    item = l[x]
    del l[x]
    l.insert(y, item)
    return l

if __name__ == "__main__":
    lines = read_data()
    result = process_instructions(lines, list("abcdefgh"))
    print(f"{''.join(result)}")

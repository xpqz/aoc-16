from itertools import islice, cycle
import re

def read_data(filename="data/input21.data"):
    with open(filename) as f:
        return f.read().splitlines()

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

class Scrambler:
    def __init__(self, instructions):
        self.instructions = instructions

    @staticmethod
    def _rotate_abs(line, string):
        rotate_abs = re.compile(r"^rotate (left|right) (\d+) steps?$")
        m = rotate_abs.match(line)
        if not m:
            return False
        if m.group(1) == "left":
            return rotate_left(string, int(m.group(2)))
        return rotate_right(string, int(m.group(2)))

    @staticmethod
    def _un_rotate_abs(line, string):
        rotate_abs = re.compile(r"^rotate (left|right) (\d+) steps?$")
        m = rotate_abs.match(line)
        if not m:
            return False
        if m.group(1) == "left":
            return rotate_right(string, int(m.group(2)))
        return rotate_left(string, int(m.group(2)))

    @staticmethod
    def _rotate_rel(line, string):
        rotate_rel = re.compile(r"^rotate based on position of letter (.)$")
        m = rotate_rel.match(line)
        if not m:
            return False
        return rotate_right_by_index(string, m.group(1))

    @staticmethod
    def _un_rotate_rel(line, string):
        rotate_rel = re.compile(r"^rotate based on position of letter (.)$")
        m = rotate_rel.match(line)
        if not m:
            return False
        for i in range(len(string)+3):
            test = rotate_left(string, i)
            if rotate_right_by_index(test, m.group(1)) == string:
                return test
        return False

    @staticmethod
    def _switch_rel(line, string):
        switch_rel = re.compile(r"^swap letter (.) with letter (.)$")
        m = switch_rel.match(line)
        if not m:
            return False
        return swap_letters(string, m.group(1), m.group(2))

    @staticmethod
    def _un_switch_rel(line, string):
        return Scrambler._switch_rel(line, string)

    @staticmethod
    def _switch_abs(line, string):
        switch_abs = re.compile(r"^swap position (\d+) with position (\d+)")
        m = switch_abs.match(line)
        if not m:
            return False
        return swap_position(string, int(m.group(1)), int(m.group(2)))

    @staticmethod
    def _un_switch_abs(line, string):
        return Scrambler._switch_abs(line, string)

    @staticmethod
    def _rev(line, string):
        rev = re.compile(r"^reverse positions (\d+) through (\d+)$")
        m = rev.match(line)
        if not m:
            return False
        return reverse_span(string, int(m.group(1)), int(m.group(2)))

    @staticmethod
    def _un_rev(line, string):
        return Scrambler._rev(line, string)

    @staticmethod
    def _move_pos(line, string):
        move_pos = re.compile(r"^move position (\d+) to position (\d+)$")
        m = move_pos.match(line)
        if not m:
            return False
        return move_position(string, int(m.group(1)), int(m.group(2)))

    @staticmethod
    def _un_move_pos(line, string):
        move_pos = re.compile(r"^move position (\d+) to position (\d+)$")
        m = move_pos.match(line)
        if not m:
            return False
        return move_position(string, int(m.group(2)), int(m.group(1)))

    def _apply_rules(self, data, rules, string):
        for line in data:
            string = next(filter(None, map(lambda rule, l=line: rule(l, string), rules)))

        return string

    def scramble(self, string):
        rules = [
            Scrambler._rotate_abs, Scrambler._rotate_rel, Scrambler._switch_rel,
            Scrambler._switch_abs, Scrambler._rev, Scrambler._move_pos
        ]
        return self._apply_rules(self.instructions, rules, string)

    def unscramble(self, string):
        rules = [
            Scrambler._un_rotate_abs, Scrambler._un_rotate_rel, Scrambler._un_switch_rel,
            Scrambler._un_switch_abs, Scrambler._un_rev, Scrambler._un_move_pos
        ]
        return self._apply_rules(reversed(self.instructions), rules, string)


if __name__ == "__main__":
    lines = read_data()
    scrambler = Scrambler(lines)

    result = scrambler.scramble(list("abcdefgh"))
    print(f"{''.join(result)}")

    result = scrambler.unscramble(list("fbgdceah"))
    print(f"{''.join(result)}")

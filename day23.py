"""
This is the asmbunny code.

0:  cpy a b
1:  dec b
2:  cpy a d      # L6
3:  cpy 0 a

# This is where all the time is spent (4-9)
# which can be replaced with a = b*d
4:  cpy b c      # L2
    5:  inc a        # L1
    6:  dec c
    7:  jnz c -2     # if c goto L1
    8:  dec d
9:  jnz d -5     # if d goto L2

10: dec b
11: cpy b c
12: cpy c d

13: dec d        # L3
14: inc c
15: jnz d -2     # if d goto L3

16: tgl c
17: cpy -16 c
18: jnz 1 c

19: cpy 87 c
20: jnz 80 d     # L5; goto address reg[d]

    21: inc a        # L4
    22: inc d
    23: jnz d -2     # if d goto L4

24: inc c
25: jnz c -5     # if c goto L5

"""

def read_data(filename="data/input23.data"):
    with open(filename) as f:
        return f.read().splitlines()


def parse_data(lines):
    data = [line.split(" ") for line in lines]
    for instr in data:
        try:
            instr[1] = int(instr[1])
        except (ValueError, IndexError):
            pass
        try:
            instr[2] = int(instr[2])
        except (ValueError, IndexError):
            pass

    return data


class Machine:
    def __init__(self, instructions):
        self.data = instructions
        self.regs = {"a": 0, "b": 0, "c": 0, "d": 0}
        self.ip = 0

    def icpy(self, instr):
        (reg_or_int1, reg_or_int2) = instr

        self.ip += 1

        if isinstance(reg_or_int1, int) and isinstance(reg_or_int2, int):
            # skip silently if self-modified code cannot be executed
            return

        if isinstance(reg_or_int1, int):
            self.regs[reg_or_int2] = reg_or_int1
        else:
            self.regs[reg_or_int2] = self.regs[reg_or_int1]


    def idec(self, instr):
        reg = instr[0]
        self.regs[reg] -= 1
        self.ip += 1

    def iinc(self, instr):
        reg = instr[0]
        self.regs[reg] += 1
        self.ip += 1

    def ijnz(self, instr):
        (reg_or_val1, reg_or_val2) = instr
        if isinstance(reg_or_val1, int):
            cnd = reg_or_val1
        else:
            cnd = self.regs[reg_or_val1]

        if cnd != 0:
            if isinstance(reg_or_val2, int):
                offset = reg_or_val2
            else:
                offset = self.regs[reg_or_val2]

            self.ip += offset
        else:
            self.ip += 1


    def itgl(self, instr):
        reg_or_int = instr[0]
        if isinstance(reg_or_int, int):
            loc = self.ip + reg_or_int
        else:
            loc = self.ip + self.regs[reg_or_int]

        if 0 <= loc < len(self.data):
            if len(self.data[loc]) == 2:
                if self.data[loc][0] == "inc":
                    self.data[loc][0] = "dec"
                else:
                    self.data[loc][0] = "inc"
            else:
                if self.data[loc][0] == "jnz":
                    self.data[loc][0] = "cpy"
                else:
                    self.data[loc][0] = "jnz"

        self.ip += 1

    def step(self):
        if self.ip < 0 or self.ip >= len(self.data):
            return False
        instr = self.data[self.ip]
        getattr(self, f"i{instr[0]}")(instr[1:])
        return True

    def step2(self):
        if self.ip < 0 or self.ip >= len(self.data):
            return False

        if self.ip == 4:  # L2 loop
            self.regs["a"] += self.regs["d"]*self.regs["b"]
            self.regs["c"] = 0
            self.regs["d"] = 0
            self.ip = 9

        instr = self.data[self.ip]

        getattr(self, f"i{instr[0]}")(instr[1:])

        return True

if __name__ == "__main__":

    data = read_data()
    instr = parse_data(data)

    m = Machine(instr)
    m.regs["a"] = 7

    while m.step():
        pass

    print(m.regs["a"])

    instr = parse_data(data)
    m = Machine(instr)
    m.regs["a"] = 12

    while m.step2():
        pass

    print(m.regs["a"])

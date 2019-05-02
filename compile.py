"""
Helper tool for day12 and similar tasks -- do some jump annotations
as a starting point for disassembly.
"""


def read_data(filename="data/input12.data"):
    with open(filename) as f:
        return f.read().splitlines()


def parse_data(lines):
    code = []
    for line in lines:
        code.append(tuple(line.split(" ")))
    return code, {"a": 0, "b": 0, "c": 0, "d": 0}


class Machine:
    def __init__(self, lines):
        self.code, self.regs = parse_data(lines)
        self.ip = 0
        self.labels = {}
        self.statements = []
        self.label_id = 1

    def icpy(self, arg1, arg2):
        self.statements.append(f"{arg2} = {arg1}")

    def idec(self, arg1, _arg2=None):
        self.statements.append(f"{arg1} -= 1")

    def iinc(self, arg1, _arg2=None):
        self.statements.append(f"{arg1} += 1")

    def ijnz(self, arg1, arg2):
        jump_to = self.ip + int(arg2)
        if jump_to not in self.labels:
            label = f"L{self.label_id}"
            self.label_id += 1
            self.labels[jump_to] = label
        else:
            label = self.labels[jump_to]

        cmp = f"{arg1} != 0"

        if cmp == "1 != 0":
            self.statements.append(f"GOTO {label}")
        else:
            self.statements.append(f"IF {arg1} != 0: GOTO {label}")

    def compile(self):
        for self.ip, op in enumerate(self.code):
            getattr(self, f"i{op[0]}")(*op[1:])

        for self.ip, line in enumerate(self.statements):
            op = f"{self.code[self.ip]}"
            op = op.replace("(", "")
            op = op.replace("'", "")
            op = op.replace(")", "")
            op = op.replace(",", "")

            l = ""
            if self.ip in self.labels:
                l = self.labels[self.ip]
            elif line.startswith("IF") or line.startswith("GOTO"):
                l = line
            print("{0:>2}: {1:<17} {2:<18}".format(self.ip, op, l))


if __name__ == "__main__":
    machine = Machine(read_data())

    machine.compile()

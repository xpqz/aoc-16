import re

def read_data(filename="data/input10.data"):
    with open(filename) as f:
        return f.read().splitlines()

def parse_data(lines):
    bots = {}
    outputs = set()
    for line in lines:
        m = re.search(r"^value (\d+) goes to bot (\d+)$", line)
        if m:
            bid = m.group(2)
            value = int(m.group(1))
            if bid not in bots:
                bots[bid] = {"id": bid, "values": []}
            bots[bid]["values"].append(value)
            continue

        m = re.search(
            r"bot (\d+) gives low to (output|bot) (\d+) and high to (output|bot) (\d+)",
            line
        )

        bid = m.group(1)
        low = m.group(3)
        high = m.group(5)
        if bid not in bots:
            bots[bid] = {"id": bid, "values": []}

        if m.group(2) == "output":
            low = f"output-{low}"
            outputs.add(low)
        if m.group(4) == "output":
            high = f"output-{high}"
            outputs.add(high)

        if bid not in bots:
            bots[bid] = {"id": bid, "values": []}
        bots[bid].update({"low": low, "high": high})

    for o in outputs:
        bots[o] = {"values": []}

    return bots

def has_two(b):
    return {
        bid: spec
        for bid, spec in b.items()
        if len(spec["values"]) == 2
    }

def find_low_high(b, l, h):
    while True:
        state = {}
        twos = has_two(b)

        if not twos:
            return False

        for bid, spec in b.items():
            if bid not in twos:
                state[bid] = spec

        for bid, spec in twos.items():
            low, high = sorted(spec["values"])

            if low == l and high == h:
                return bid

            state[spec["low"]]["values"].append(low)
            state[spec["high"]]["values"].append(high)
            spec["values"] = []
            state[bid] = spec

        b = state


def output_product(b):
    while True:
        state = {}
        twos = has_two(b)

        if not twos:
            return False

        for bid, spec in b.items():
            if bid not in twos:
                state[bid] = spec

        for bid, spec in twos.items():
            low, high = sorted(spec["values"])

            state[spec["low"]]["values"].append(low)
            state[spec["high"]]["values"].append(high)
            spec["values"] = []
            state[bid] = spec

            if b["output-0"]["values"] and b["output-1"]["values"] and b["output-2"]["values"]:
                return b["output-0"]["values"][0] * b["output-1"]["values"][0] * b["output-2"]["values"][0]

        b = state

if __name__ == "__main__":
    data = read_data()

    bots = parse_data(data)

    print(find_low_high(bots, 17, 61))
    print(output_product(bots))

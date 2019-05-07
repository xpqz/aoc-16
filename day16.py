def dragon(state):
    return state + "0" + "".join("0" if d == "1" else "1" for d in reversed(state))

def fill(state, size):
    while len(state) < size:
        state = dragon(state)
    return state[:size]

def pairs(state):
    for i in range(0, len(state), 2):
        yield state[i:i+2]

def value(pair):
    return str(int(pair in {"00", "11"}))

def checksum_round(c):
    chs = ""
    for pair in pairs(c):
        chs += value(pair)
    return chs

def checksum(state):
    while True:
        state = checksum_round(state)
        if len(state)%2 != 0:
            return state

if __name__ == "__main__":
    for size in [272, 35651584]:
        print(checksum(fill("10111100110001111", size)))

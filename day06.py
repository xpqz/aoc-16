from collections import Counter

def transpose(arr):
    return [*zip(*arr)]

def read_data(filename="data/input06.data"):
    with open(filename) as f:
        return transpose([list(l) for l in f.read().splitlines()])

def least_common(counter):
    return min(counter.most_common(), key=lambda x: x[1])[0]


if __name__ == "__main__":
    d = read_data()

    for line in d:
        print(Counter(line).most_common(1)[0][0], end="")
    print()

    for line in d:
        print(least_common(Counter(line)), end="")
    print()

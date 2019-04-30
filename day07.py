import re

def read_data(filename="data/input07.data"):
    with open(filename) as f:
        return f.read().splitlines()

def has_abba(c):
    p = re.compile(r"([a-z])([a-z])\2\1")
    m = p.search(c)

    return m and m.group(1) != m.group(2)

def abas(s):
    for i in range(len(s)):
        sect = s[i:i+3]
        if len(sect) == 3 and sect[0] == sect[2]:
            yield sect


def tls(ip):
    hypernet = False
    supernet = 0
    for i in re.split(r"([\[\]])", ip):
        if not hypernet and i == "[":
            hypernet = True
            continue

        if hypernet and i == "]":
            hypernet = False
            continue

        abba = has_abba(i)
        if hypernet and abba:
            return False

        if not hypernet and abba:
            supernet += 1

    return supernet > 0


def ssl(ip):
    hypernets = []
    supernets = []
    hypernet = False

    for i in re.split(r"([\[\]])", ip):
        if not hypernet and i == "[":
            hypernet = True
            continue

        if hypernet and i == "]":
            hypernet = False
            continue

        if hypernet:
            hypernets.append(i)
        else:
            supernets.append(i)

    for supernet in supernets:
        for aba in abas(supernet):
            bab = f"{aba[1]}{aba[0]}{aba[1]}"
            for hn in hypernets:
                if bab in hn:
                    return True

    return False

if __name__ == "__main__":
    d = read_data()

    print(len(list(filter(tls, d))))
    print(len(list(filter(ssl, d))))

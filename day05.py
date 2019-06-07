import hashlib
from itertools import count

def passw(seed):
    pw = ""
    for i in count(0):
        m = hashlib.md5()
        m.update(f"{seed}{i}".encode("utf-8"))
        d = m.hexdigest()
        if d[:5] == "00000":
            pw += d[5]
            if len(pw) == 8:
                break
    return pw


def passw2(seed):
    pw = ["_", "_", "_", "_", "_", "_", "_", "_"]
    print("".join(pw), end="\r", flush=True)
    for i in count(0):
        m = hashlib.md5()
        m.update(f"{seed}{i}".encode("utf-8"))
        d = m.hexdigest()
        if d[:5] == "00000" and d[5] in "01234567":
            index = int(d[5])
            if pw[index] == "_":
                pw[index] = d[6]
                print("".join(pw), end="\r", flush=True)
                if "_" not in pw:
                    break

    return "".join(pw)

if __name__ == "__main__":
    print(passw("ffykfhsq"))
    print(passw2("ffykfhsq"))

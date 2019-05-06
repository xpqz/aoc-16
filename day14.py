
from functools import lru_cache
import hashlib
from itertools import count
import re

def get_digest(s):
    m = hashlib.md5()
    m.update(s.encode("utf-8"))
    return m.hexdigest()

@lru_cache(maxsize=2048)
def h(i, seed="ahsbgdzn"):
    return get_digest(f"{seed}{i}")

@lru_cache(maxsize=2048)
def stretch(digest):
    for _ in range(2016):
        digest = get_digest(digest)
    return digest

def find_keys(seed="ahsbgdzn"):
    keys = 0
    pattern = re.compile(r"(.)\1\1")
    for i in count():
        digest = h(i, seed=seed)
        match = pattern.search(digest)

        # If we have three in a row, search the subsequent
        # 1000 hashes for a five-in-a-row of the same char.
        if match:
            pattern2 = re.compile(match.group(1)+"{5}")
            for j in range(i+1, i+1002):
                digest2 = h(j, seed=seed)
                if pattern2.search(digest2):
                    keys += 1
                    break
            if keys == 64:
                return i

def find_stretched_keys(seed="ahsbgdzn"):
    keys = 0
    pattern = re.compile(r"(.)\1\1")
    for i in count():
        digest = stretch(h(i, seed=seed))
        match = pattern.search(digest)
        if match:
            pattern2 = re.compile(match.group(1)+"{5}")
            for j in range(i+1, i+1002):
                digest2 = stretch(h(j, seed=seed))
                if pattern2.search(digest2):
                    keys += 1
                    break
            if keys == 64:
                return i

if __name__ == "__main__":
    index = find_keys(seed="ahsbgdzn")
    print(index)

    index = find_stretched_keys(seed="ahsbgdzn")
    print(index)

"""
For part two we need a data structure that can be indexed like a list,
but offer better than O(N) deletes. "blist" implements Indexable but
is a btree under the hood.

See https://pypi.org/project/blist/ http://stutzbachenterprises.com/blist/

"""
from blist import blist

def elf_circle(length):
    circle = blist()

    for elf_id in range(1, length+1):
        circle.append(elf_id)

    return circle

def steal_opposite(elfcount=3_014_603):
    circle = elf_circle(elfcount)

    pos = 0
    while len(circle) > 1:
        elfcount = len(circle)
        pos %= elfcount
        half = elfcount // 2
        opposite = (pos + half) % elfcount
        del circle[opposite]

        if opposite > pos:
            pos += 1
            if pos >= len(circle):
                pos = 0

    return circle[0]


def steal_next(elfcount=3_014_603):
    circle = elf_circle(elfcount)

    pos = 0
    while len(circle) > 1:
        elfcount = len(circle)
        target = (pos+1) % elfcount
        del circle[target]

        pos = target

    return circle[0]


if __name__ == "__main__":
    elf_count = 3_014_603
    print(steal_next(elf_count))
    print(steal_opposite(elf_count))

"""
For part two we need a data structure that can be indexed like a list,
but offer better than O(N) deletes. "blist" implements Indexable but
is a btree under the hood.

See https://pypi.org/project/blist/ http://stutzbachenterprises.com/blist/

"""
from blist import blist


def steal_opposite(elfcount=3_014_603):
    circle = blist([elf_id for elf_id in range(1, elfcount+1)])

    pos = 0
    elfcount = len(circle)
    while elfcount > 1:
        pos %= elfcount
        opposite = (pos + elfcount // 2) % elfcount
        del circle[opposite]
        if opposite > pos:
            pos += 1
        elfcount -= 1

    return circle[0]


def steal_next(elfcount=3_014_603):
    circle = blist([elf_id for elf_id in range(1, elfcount+1)])

    pos = 0
    elfcount = len(circle)
    while elfcount > 1:
        target = (pos+1) % elfcount
        del circle[target]
        pos = target
        elfcount -= 1

    return circle[0]


if __name__ == "__main__":
    elf_count = 3_014_603
    print(steal_next(elf_count))
    print(steal_opposite(elf_count))

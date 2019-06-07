"""
STEP 1: Annotate loops

0:  cpy a d
1:  cpy 11 c

2:  cpy 231 b <---+             BLOCK ONE
3:  inc d    <--+ |
4:  dec b       | |
5:  jnz b -2 ---+ |
6:  dec c         |
7:  jnz c -5 -----+

8:  cpy d a
9:  jnz 0 0
10: cpy a b

11: cpy 0 a                      BLOCK TWO
12: cpy 2 c  <-----------+
13: jnz b 2  --------+   | <-+
14: jnz 1 6  --> ..  |   |   |    exit loops: goto 20
15: dec b    <-------+   |   |
16: dec c                |   |
17: jnz c -4 ------------|---+
18: inc a                |
19: jnz 1 -7  -----------+

20: cpy 2 b                      BLOCK THREE
21: jnz c 2  ---+
22: jnz 1 4  ---|--+ <-+
23: dec b    <--+  |   |
24: dec c          |   |
25: jnz 1 -4  -----|---+
26: jnz 0 0  <-----+


27: out b                 ^
                          |  ^
28: jnz a -19 ------------+  |
29: jnz 1 -21 ---------------+

STEP 2: Resolve BLOCK ONE

Two nested loops, amounting to a multiplication:

while True:
    b = 231           # 2
    while True:
        d += 1        # 3
        b -= 1        # 4
        if b == 0:    # 5
            break
    c -= 1
    if c == 0:
        break

which simplifies to:

while c != 0:
    b = 231
    while b != 0:
        d += 1
        b -= 1
    c -= 1

and finally

d = a + 231 * 11

b = 0
c = 0

STEP 3: Resolve BLOCK TWO

8:  cpy d a
9:  jnz 0 0
10: cpy a b

done = False
while True:
    c = 2
    while True:
        if b == 0:
            done = True
            break
        b -= 1
        c -= 1

        if c == 0:
            break
    if done:
        break
    a += 1

which is a long-winded way of saying

a = a // 2
c = 2 - a%2

STEP 4: Resolve BLOCK THREE

20: cpy 2 b                BLOCK THREE
21: jnz c 2  ---+
22: jnz 1 4  ---|--+ <-+
23: dec b    <--+  |   |
24: dec c          |   |
25: jnz 1 -4  -----|---+
26: jnz 0 0  <-----+

b = 2
while True:
    if c == 0:
        break
    b -= 1
    c -= 1

which is

b = 2 - c

but by this stage c = 2 - a%2 so BLOCK THREE becomes

b = a % 2

The last two loops are straight-forward. The whole program becomes:

d = a + 2541
while True:
    a = d
    while a != 0:
        b = a % 2
        a //= 2
        print(f"{b} ", end="")
    print()

So what's going on here? It's basically computing the binary representation of d, over and over.

For a = 1 we get:

0 1 1 1  0 1 1 1  1 0 0 1
0 1 1 1  0 1 1 1  1 0 0 1
0 1 1 1  0 1 1 1  1 0 0 1
0 1 1 1  0 1 1 1  1 0 0 1
0 1 1 1  0 1 1 1  1 0 0 1
0 1 1 1  0 1 1 1  1 0 0 1
0 1 1 1  0 1 1 1  1 0 0 1
...

So we need a positive number that added to 2541 produces the following three LS bytes in binary:

0 1 0 1  0 1 0 1  0 1 0 1  (0x555)


"""

from itertools import count

def run():
    for aa in count(1):
        a = aa

        d = a + 2541
        a = d

        v = ""
        while a != 0:
            b = a % 2
            a //= 2
            v += f"{b}"

        if v == "010101010101":
            return aa

if __name__ == "__main__":
    print(run())

"""
This is an alternative approach to day12 p2.

"Compiled" to Python it runs considerably faster, even without
obvious optimisations to remove the crude loops.
"""
a, b, c, d = 0, 0, 1, 0

#  0: cpy 1 a
a = 1

#  1: cpy 1 b
b = 1

#  2: cpy 26 d
d = 26

#  5: cpy 7 c           L1
c = 7

#  6: inc d             L3
while True:
    d += 1

    #  7: dec c
    c -= 1

    #  8: jnz c -2          IF c != 0: GOTO L3
    if c == 0:
        break

while True:
    #  9: cpy a c           L2
    c = a

    # 10: inc a             L4
    while True:
        a += 1

        # 11: dec b
        b -= 1

        # 12: jnz b -2          IF b != 0: GOTO L4
        if b == 0:
            break

    # 13: cpy c b
    b = c

    # 14: dec d
    d -= 1

    # 15: jnz d -6          IF d != 0: GOTO L2
    if d == 0:
        break

# 16: cpy 16 c
c = 16

while True:
    # 17: cpy 12 d          L6
    d = 12

    while True:
        # 18: inc a             L5
        a += 1

        # 19: dec d
        d -= 1

        # 20: jnz d -2          IF d != 0: GOTO L5
        if d == 0:
            break

    # 21: dec c
    c -= 1

    # 22: jnz c -5          IF c != 0: GOTO L6
    if c == 0:
        break


print(f"a:{a} b:{b} c:{c} d:{d}")

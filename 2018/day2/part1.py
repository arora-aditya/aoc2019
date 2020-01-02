from collections import Counter
with open("input.txt", "r") as f:
    lines = f.readlines()
    twos = 0
    threes = 0
    for line in lines:
        c = Counter(line.rstrip())
        f2, f3 = False, False
        for char, value in c.items():
            if value == 2:
                f2 = True
            if value == 3:
                f3 = True
        if f2:
            twos += 1
        if f3:
            threes += 1
    print(twos*threes, twos, threes)
# 7688
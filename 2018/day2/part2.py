from collections import Counter

def difference(line, line_old):
    flag = False
    for i in range(len(line)):
        if line[i] != line_old[i]:
            if flag:
                return False
            flag = True
    return flag

with open("input.txt", "r") as f:
    lines = f.readlines()
    twos = 0
    threes = 0
    seen = {}
    for line in map(lambda x: x.strip(), lines):
        c = Counter(line)
        for line_old, c_old in seen.items():
            diff = c_old - c
            if len(diff) != 1:
                continue
            if difference(line, line_old):
                print(line_old)
                print(line)
            break
        seen[line] = c
        
# lsrivmotzbdxpkxnaqmuwcchj
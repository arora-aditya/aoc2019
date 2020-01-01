with open("input.txt", "r") as f:
    lines = f.readlines()
    su = 0
    seen = set()
    flag = True
    while flag:
        for line in lines:
            su += int(line)
            if su in seen:
                flag = False
                break
            seen.add(su)
    print(su)
# 394
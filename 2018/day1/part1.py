with open("input.txt", "r") as f:
    lines = f.readlines()
    su = 0
    for line in lines:
        su += int(line)
    print(su)
# 520
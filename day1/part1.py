with open("input.txt", "r") as f:
    lines = f.readlines()
    su = 0
    for line in lines:
        print(int(line)//3 - 2)
        su += int(line)//3 - 2
    print(su)
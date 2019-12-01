from math import floor
with open("input.txt", "r") as f:
    lines = f.readlines()
    su = 0
    for line in lines:
        fuel = int(line)//3 - 2
        su += fuel
        while fuel > 0:
            fuel = fuel//3 - 2
            if fuel >= 0:
                su += fuel
    print(su)
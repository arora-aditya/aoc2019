def satisfy(i):
    l = list(map(int, str(i)))
    m = -float('inf')
    flag = False
    for k in range(len(l)):
        if l[k] == m:
            flag = True
        if l[k] >= m:
            m = l[k]
        else:
            return False
    return flag 

with open("input.txt", "r") as f: 
    line = list(map(int, f.readline().split('-')))
    count = 0
    lower, upper = line[0], line[1]
    for i in range(lower, upper+1):
        if satisfy(i):
            count += 1
            print(i)
    print(count)
# 1019
    
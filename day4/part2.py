from collections import defaultdict

def satisfy(k):
    l = list(map(int, str(k)))
    m = -float('inf')
    flag = 0
    di = defaultdict(dict)
    for i in range(len(l)):
        if l[i] != m:
            di[l[i]][i] = 0
            count = 0
        if l[i] == m:
            di[l[i]][i - count] += 1
            count += 1
        if l[i] > m:
            di[l[i]][i - count] += 1
            count += 1
        if l[i] < m:
            di[l[i]][i - count] += 1
            count += 1
            return False
        m = l[i]
    for key in di:
        for index in di[key]:
            if di[key][index] == 2:
                return True
    return False

with open("input.txt", "r") as f:     
    line = list(map(int, f.readline().split('-')))
    count = 0
    lower, upper = line[0], line[1]
    for i in range(lower, upper+1):
        if satisfy(i):
            count += 1
            print(i)
    print(count)
# 660
    
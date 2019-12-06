from collections import defaultdict

def path(start_coordinates, direction, count):
    if d == 'U':
        return [[start_coordinates[0], start_coordinates[1] + i] for i in range(1, count)]
    elif d == 'D':
        return [[start_coordinates[0], start_coordinates[1] - i] for i in range(1, count)]
    elif d == 'R':
        return [[start_coordinates[0] + i, start_coordinates[1]] for i in range(1, count)]
    elif d == 'L':
        return [[start_coordinates[0] - i, start_coordinates[1]] for i in range(1, count)]

def memoize(path):
    di = defaultdict(set)
    for p in path:
        di[p[0]].add(p[1])
    return di

with open("input.txt", "r") as f:
    
    lines = f.readlines()
    # assert len(lines) == 2, 'Only 2 lines'
    L1 = map(lambda x: (x[0], int(x[1:])), lines[0].split(','))
    L2 = map(lambda x: (x[0], int(x[1:])), lines[1].split(','))
    L1_path, L2_path = [], []
    c = [0,0]
    for p in L1:
        d, v = p
        L1_path.extend(path(c, d, v+1))
        c = L1_path[-1]
    c = [0,0]
    for p in L2:
        d, v = p
        L2_path.extend(path(c, d, v+1))
        c = L2_path[-1]
    L1_path = memoize(L1_path)
    L2_path = memoize(L2_path)
    m = [float('inf'), float('inf')]
    for p in L1_path:
        L1_y = L1_path[p]
        L2_y = L2_path[p]
        se = L1_y & L2_y
        if len(se) >= 1:
            for r in se:
                if p + r < m[0] + m[1]:
                    m = [p, r]
    print(m)
    print(m[0] + m[1])
# 557
    
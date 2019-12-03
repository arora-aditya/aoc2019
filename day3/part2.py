from collections import defaultdict

def path(start_coordinates, direction, count):
    if d == 'U':
        return [[start_coordinates[0], start_coordinates[1] + i, start_coordinates[2] + i] for i in range(1, count)]
    elif d == 'D':
        return [[start_coordinates[0], start_coordinates[1] - i, start_coordinates[2] + i] for i in range(1, count)]
    elif d == 'R':
        return [[start_coordinates[0] + i, start_coordinates[1], start_coordinates[2] + i] for i in range(1, count)]
    elif d == 'L':
        return [[start_coordinates[0] - i, start_coordinates[1], start_coordinates[2] + i] for i in range(1, count)]

def memoize(path):
    di = defaultdict(dict)
    di
    for p in path:
        di[p[0]][p[1]] = p[2]
    return di

with open("input.txt", "r") as f:
    
    lines = f.readlines()
    # assert len(lines) == 2, 'Only 2 lines'
    L1 = map(lambda x: (x[0], int(x[1:])), lines[0].split(','))
    L2 = map(lambda x: (x[0], int(x[1:])), lines[1].split(','))
    L1_path, L2_path = [], []
    c = [0,0,0]
    for p in L1:
        d, v = p
        L1_path.extend(path(c, d, v+1))
        c = L1_path[-1]
    c = [0,0, 0]
    for p in L2:
        d, v = p
        L2_path.extend(path(c, d, v+1))
        c = L2_path[-1]
    L1_path_memo = memoize(L1_path)
    L2_path_memo = memoize(L2_path)
    m = [[float('inf'), float('inf'), float('inf')], [float('inf'), float('inf'), float('inf')]]
    for p in L1_path_memo:
        L1_y = L1_path_memo[p]
        L2_y = L2_path_memo[p]
        se = L1_y.keys() & L2_y.keys()
        if len(se) >= 1:
            for r in se:
                s = L1_y[r] + L2_y[r]
                if s < m[0][2] + m[1][2]:
                    m = [[p, r, L1_y[r]], [p, r, L2_y[r]]]
    print(m)
    print(m[0][2] + m[1][2])
# 3931283
    
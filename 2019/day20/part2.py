import sys
from collections import defaultdict, deque

DIRECTIONS = {
    1: 1j,
    4: 1,
    3: -1,
    2: -1j,
}
def neighbors(position):
    for i, d in DIRECTIONS.items():
        yield (position + d), i + 1

def parse_file(filename):
    with open(filename) as f:
        lines = [list(line.rstrip()) for line in f.readlines()]
        return lines

def convert_to_map(inputs):
    di = {}
    for i in range(len(inputs)):
        for j in range(len(inputs[i])):
            di[j + i*1j] = inputs[i][j]
    return di

def parse_portals(map):
    p = defaultdict(list)
    rp = {}
    for position, c in map.items():
        if c in '.# ':
            continue
        pos = None
        sl = None
        fl = c
        for n, _ in neighbors(position):
            if n not in map:
                continue
            if map[n] == '.':
                pos = n
            elif map[n] not in '.# ':
                sl = map[n]
        if pos is None or sl is None:
            continue
        [fl, sl] = list(sorted([fl, sl]))
        p[fl + sl].append(pos)
        rp[pos] = fl + sl

    return p, rp

def bfs_start_to_end(map, p, rp):
    w, h = max(v.real for v in map.keys()), max(v.imag for v in map.keys())
    start = p['AA'][0]

    queue = deque([(start, 0, 0)])
    visited = set([(start, 0)])
    while queue:
        position, d, slo = queue.popleft()
        if slo == 0 and position == p['ZZ'][0]:
            return d
        if map[position] == '#':
            continue
        if slo < 0:
            continue
        for n, _ in neighbors(position):
            sl = slo
            if map[n] not in '#. ':
                lp = p[rp[position]]
                if len(lp) < 2:
                    continue

                if position.real < 3 or position.real > w - 3 or position.imag < 3 or position.imag > h - 3:
                    sl -= 1
                else:
                    sl += 1
                if lp[0] == position:
                    n = lp[1]
                else:
                    n = lp[0]
            if (n, sl) not in visited:
                visited.add((n, sl))
                queue.append((n, d + 1, sl))

def main(f):
    inputs = convert_to_map(parse_file(f))
    p, rp = parse_portals(inputs)
    print(bfs_start_to_end(inputs, p, rp))


TEST = 'input_test_part2.txt'
REAL = 'input.txt'

# 8384

if __name__ == "__main__":
    main(REAL)
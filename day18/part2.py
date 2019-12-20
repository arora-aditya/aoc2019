import itertools
import collections
import heapq
from pprint import pprint

def parse_file(filename):
    grids = [[], [], [], []]
    with open(filename) as f:
        lines = [line.strip() for line in f.readlines()]
        R, C = len(lines), len(lines[0])
        for line in lines[:R//2 + 1]:
            grids[0].append(line[:C//2 + 1])
            grids[1].append(line[C//2:])
        for line in lines[R//2:]:
            grids[2].append(line[:C//2 + 1])
            grids[3].append(line[C//2:])
    return grids
            
        
TEST1 = 'input_test_part2_1.txt'
TEST2 = 'input_test_part2_2.txt'
TEST3 = 'input_test_part2_3.txt'
TEST4 = 'input_test_part2_4.txt'
REAL = 'input.txt'
TESTS = [TEST1, TEST2, TEST3, TEST4, REAL]

def shortestPathAllKeys(grid):
    R, C = len(grid), len(grid[0])

    # The points of interest
    location = {v: (r, c)
                for r, row in enumerate(grid)
                for c, v in enumerate(row)
                if v not in '.#'}

    def neighbors(r, c):
        for cr, cc in ((r-1, c), (r, c-1), (r+1, c), (r, c+1)):
            if 0 <= cr < R and 0 <= cc < C:
                yield cr, cc

    # The distance from source to each point of interest
    def bfs_from(source):
        r, c = location[source]
        seen = [[False] * C for _ in range(R)]
        seen[r][c] = True
        queue = collections.deque([(r, c, 0)])
        dist = {}
        while queue:
            r, c, d = queue.popleft()
            if source != grid[r][c] != '.':
                dist[grid[r][c]] = d
                continue # Stop walking from here if we reach a point of interest
            for cr, cc in neighbors(r, c):
                if grid[cr][cc] != '#' and not seen[cr][cc]:
                    seen[cr][cc] = True
                    queue.append((cr, cc, d+1))
        return dist        

    dists = {place: bfs_from(place) for place in location}
    
    
    keys_in_grid = set([p for p in location if p.islower()])
    print(keys_in_grid)
    target_state = 0
    for p in keys_in_grid:
        target_state |= (1 << (ord(p) - ord('a')))

    #Dijkstra
    pq = [(0, '@', 0)]
    final_dist = collections.defaultdict(lambda: float('inf'))
    final_dist['@', 0] = 0
    while pq:
        d, place, state = heapq.heappop(pq)
        print(state, target_state, pq)
        if final_dist[place, state] < d: continue
        if state == target_state: return d
        for destination, d2 in dists[place].items():
            state2 = state
            if destination.islower(): #key
                state2 |= (1 << (ord(destination) - ord('a')))
            elif destination.isupper(): #lock
                if destination not in keys_in_grid:
                    # print(f'Passing over a key not in quadrant {destination}')
                    pass
                # if not(state & (1 << (ord(destination) - ord('A')))): #no key
                #     # continue
                #     pass

            if d + d2 < final_dist[destination, state2]:
                final_dist[destination, state2] = d + d2
                heapq.heappush(pq, (d+d2, destination, state2))

    return -1

for TEST in TESTS[4:]:
    grids = parse_file(TEST)
    su = 0
    for grid in grids:
        ans = shortestPathAllKeys(grid)
        su += ans
        print(su)
        print('*'*100)
    print(su, grids)
        
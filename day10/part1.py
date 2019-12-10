from collections import defaultdict, namedtuple
from itertools import permutations 
from functools import lru_cache
from fractions import Fraction
from pprint import pprint as print

INF = float('inf')

Point = namedtuple('Point', ['x', 'y', 'dx', 'dy'])

Line = namedtuple('Line', ['m', 'c'])

@lru_cache(None)
def distance(origin, point):
    num = (point.y - origin.y)
    den = (point.x - origin.x)
    return pow(num*num + den*den, 0.5)

@lru_cache(None)
def line_between_points(origin, point):
    num = (point.y - origin.y)
    den = (point.x - origin.x)
    if den != 0:
        m = Fraction(num, den)
        c = Fraction(point.y*den - num*point.x, den)
    else:
        m = INF
        c = INF
    return Line(m=m, c=c)

def line_of_sight(origin, other_points):
    lines = defaultdict(set)
    for point in other_points:
        if point != origin:
            point_copy = Point(x=point.x, y = point.y, dx=(point.x - origin.x) > 0, dy=(point.y - origin.y) > 0)
            lines[line_between_points(origin, point)].add(point_copy)
    ans = 0
    overall = set()
    for line, points in lines.items():
        visible = set()
        for point_to_add in points:
            flag = True
            for added_points in visible:
                if point_to_add.dx == added_points.dx and point_to_add.dy == added_points.dy:
                    flag = False
            if flag:
                visible.add(point_to_add)
        ans += len(visible) 
        overall |= visible
    return ans, overall
            

with open('input.txt') as f:
    lines = [list(line.strip()) for line in f.readlines()]
    R, C = len(lines), len(lines[0])

    ma = -float('inf')
    c = None
    
    asteroids = set()
    for i in range(R):
        for j in range(C):
            if lines[i][j] != '.':
                asteroids.add(Point(x=j, y=i, dx=0, dy=0))
    dp = [[0]*C for i in range(R)]
    for asteroid in asteroids:
        count, visible = line_of_sight(asteroid, asteroids)
        if ma < count:
            ma = count
            c = asteroid
    
    print(ma)
# 278

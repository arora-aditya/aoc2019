from collections import defaultdict, namedtuple
from itertools import permutations 
from functools import lru_cache
from fractions import Fraction
from math import atan2, pi
# from pprint import pprint as print

INF = Fraction(9999999999999999999999, 1)

Point = namedtuple('Point', ['x', 'y', 'dx', 'dy', 'r'])

Line = namedtuple('Line', ['m', 'c'])
Polar = namedtuple('Polar', ['theta'])

@lru_cache(None)
def distance(origin, point):
    num = (point.y - origin.y)
    den = (point.x - origin.x)
    return pow(num*num + den*den, 0.5)

@lru_cache(None)
def angle_between_points(origin, point):
    num = (point.y - origin.y)
    den = (point.x - origin.x)
    r = distance(origin, point)
    theta = atan2(num, den)*180/pi
    return Polar(theta=theta), r

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
    
def shoot(origin, other_points):
    order_of_shooting = []
    angles = defaultdict(set)
    for point in other_points:
        if point != origin:
            angle, r = angle_between_points(origin, point)
            point_copy = Point(
                x=point.x, 
                y = point.y, 
                dx=(point.x - origin.x), 
                dy=(point.y - origin.y),
                r=r,
            )
            angles[angle].add(point_copy)
    order_of_angles = list(sorted(angles.keys()))
    sort_points_by_distance = defaultdict(list)
    for angle in order_of_angles:
        sort_points_by_distance[angle] = list(sorted(angles[angle], key=lambda x: x.r))
    
    for i, angle in enumerate(order_of_angles):
        if angle.theta >= -90.0:
            break

    order_of_angles = order_of_angles[i:] + order_of_angles[:i]
    
    while True:
        flag = True
        for angle in order_of_angles:
            if len(sort_points_by_distance[angle]) > 0:
                point_to_shoot = sort_points_by_distance[angle].pop(0)
                order_of_shooting.append(point_to_shoot)
                flag = False
        if flag:
            break
    return order_of_shooting
    
                
def line_of_sight(origin, other_points):
    lines = defaultdict(set)
    for point in other_points:
        if point != origin:
            point_copy = Point(x=point.x, y = point.y, dx=(point.x - origin.x) > 0, dy=(point.y - origin.y) > 0, r=0)
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

def get_perfect_coordinates(asteroids):
    ma = -float('inf')
    c = None
    
    for asteroid in asteroids:
        count, visible = line_of_sight(asteroid, asteroids)
        if ma < count:
            ma = count
            c = asteroid
    
    return c         

with open('input.txt') as f:
    lines = [list(line.strip()) for line in f.readlines()]
    R, C = len(lines), len(lines[0])

    
    asteroids = set()
    for i in range(R):
        for j in range(C):
            if lines[i][j] != '.':
                asteroids.add(Point(x=j, y=i, dx=0, dy=0, r=0))

    station = get_perfect_coordinates(asteroids)

    
    print(f'station: {station}')
    order_of_shooting = shoot(station, asteroids)

    print(order_of_shooting[199].x*100 + order_of_shooting[199].y)
    
    
# 1417

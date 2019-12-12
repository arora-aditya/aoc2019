from collections import defaultdict, namedtuple
from itertools import permutations 
from functools import lru_cache
from queue import Queue
from threading import Thread
from fractions import Fraction
from math import gcd
# from pprint import pprint as print

INF = float('inf')

class Planet(namedtuple('Planet', ['x', 'y', 'z'])):
    __slots__ = ()
    def __add__(self, v):
        return Planet(self.x + v.dx, self.y + v.dy, self.z + v.dz)

class Velocity(namedtuple('Velocity', ['dx', 'dy', 'dz'])):
    __slots__ = ()
    def __add__(self, o): 
        return Velocity(self.dx + o.dx, self.dy + o.dy, self.dz + o.dz)
    def is_zero(self):
        return self.dx == 0 and self.dy == 0 and self.dz == 0
    def is_zero(self, key):
        return getattr(self, key) == 0

class Planets(namedtuple('Planets', ['p1', 'p2', 'p3', 'p4'])):
    __slots__ = ()
    def equality(self, first_position, key):
        for i in range(len(self)):
            if getattr(self[i], key) != getattr(first_position[i], key):
                return False
        return True

def velocities(planet1, planet2):
    # print(planet1, planet2)
    # print('-'*80)
    # gaynamede, callisto
    velocity_planet1 = [0]*3
    velocity_planet2 = [0]*3
    
    if planet1.x < planet2.x:
        velocity_planet1[0], velocity_planet2[0] = 1, -1
    elif planet1.x > planet2.x:
        velocity_planet1[0], velocity_planet2[0] = -1, 1
    
    if planet1.y < planet2.y:
        velocity_planet1[1], velocity_planet2[1] = 1, -1
    elif planet1.y > planet2.y:
        velocity_planet1[1], velocity_planet2[1] = -1, 1
    if planet1.z < planet2.z:
        velocity_planet1[2], velocity_planet2[2] = 1, -1
    elif planet1.z > planet2.z:
        velocity_planet1[2], velocity_planet2[2] = -1, 1
    
    return Velocity(*velocity_planet1), Velocity(*velocity_planet2)
    
def parse_planet(line):
    coordinates = [int(x[2:]) for x in line[1:-1].split(', ')]
    return Planet(*coordinates)    

def energy(p, v):
    pot_e = sum([abs(x) for x in p])
    kit_e = sum([abs(x) for x in v])
    return pot_e * kit_e

planets = []

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

with open('input.txt') as f:
    lines = [line.strip() for line in f.readlines()]
    for line in lines:
        planets.append(parse_planet(line))
    
    velocities_list = [Velocity(0,0,0)]*len(planets)
    
    past_positions = set()
    
    for i in range(len(planets)):
        planets[i] += velocities_list[i]
        # print({planets[i]: velocities_list[i]})
    
    first_pos = Planets(*planets)
    
    x, y, z = 0, 0, 0
    
    STEPS = 1
    while x == 0 or y == 0 or z == 0:
        STEPS += 1
        for i in range(len(planets)):
            for j in range(i+1, len(planets)):
                v1, v2 = velocities(planets[i], planets[j])
                velocities_list[i] += v1
                velocities_list[j] += v2
        for i in range(len(planets)):
            planets[i] += velocities_list[i]
            # print({planets[i]: velocities_list[i]})
        planets_pos = Planets(*planets)
        if planets_pos.equality(first_pos, 'x'):
            zeroed = True
            for v in velocities_list:
                zeroed = zeroed and v.is_zero('dx')
            if x == 0:
                x = STEPS
                # print(f'X: {x}', end='\n\n')
        if planets_pos.equality(first_pos, 'y'):
            zeroed = True
            for v in velocities_list:
                zeroed = zeroed and v.is_zero('dy')
            if y == 0:
                y = STEPS
                # print(f'Y: {y}', end='\n\n')
        if planets_pos.equality(first_pos, 'z'):
            zeroed = True
            for v in velocities_list:
                zeroed = zeroed and v.is_zero('dz')
            if z == 0:
                z = STEPS
                # print(f'Z: {z}', end='\n\n')
        past_positions.add(planets_pos)
        # print(STEPS, end='\r')
    print(lcm(x, lcm(y,z)))
# 295693702908636

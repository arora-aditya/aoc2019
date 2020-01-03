from collections import defaultdict, namedtuple
from itertools import permutations 
from functools import lru_cache
from fractions import Fraction
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

with open('input.txt') as f:
    lines = [line.strip() for line in f.readlines()]
    for line in lines:
        planets.append(parse_planet(line))
    
    velocities_list = [Velocity(0,0,0)]*len(planets)
    
    for i in range(len(planets)):
        planets[i] += velocities_list[i]
        print({planets[i]: velocities_list[i]})
    print('*' * 80)

    
    STEPS = 1000
    for step in range(STEPS):
        for i in range(len(planets)):
            for j in range(i+1, len(planets)):
                v1, v2 = velocities(planets[i], planets[j])
                velocities_list[i] += v1
                velocities_list[j] += v2
        for i in range(len(planets)):
            planets[i] += velocities_list[i]
            # print({planets[i]: velocities_list[i]})
        # print('*' * 80)
    ans = 0
    for i, planet in enumerate(planets):
        e = energy(planet, velocities_list[i])
        # print(planet, velocities_list[i], e)
        ans += e
    print(ans)

# 12082

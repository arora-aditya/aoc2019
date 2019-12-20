import doctest
import itertools
import copy
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
from pprint import pprint

def parse_file(filename):
    with open(filename) as f:
        lines = [list(line.rstrip()) for line in f.readlines()]
        return lines

def convert_to_map(inputs):
    di = {}
    for i in range(len(inputs)):
        for j in range(len(inputs[i])):
            if inputs[i][j] != ' ' and inputs[i][j] != '#':
                di[j + i*1j] = inputs[i][j]
    return di
        
TEST = 'input_test_part1.txt'
REAL = 'input.txt'

DIRECTIONS = {
    1: 1j,
    4: 1,
    3: -1,
    2: -1j,
}

def display(screen):
    miny = int(min(v.imag for v in screen.keys()))
    maxy = int(max(v.imag for v in screen.keys()))
    minx = int(min(v.real for v in screen.keys()))
    maxx = int(max(v.real for v in screen.keys()))

    for y in range(miny, maxy + 1):
        y *= 1j
        for x in range(minx, maxx + 1):
            print(screen.get(x + y, ' '), end='')
        print()

def get_neighbouring_character(position, inputs):
    for i, d in DIRECTIONS.items():
        val = inputs.get(position + d, ' ')
        if val >= 'A' and val <= 'Z':
            return val, position+d

def main():
    inputs = convert_to_map(parse_file(REAL))
    
    map = dict()
    graph = nx.Graph()
    
    pending = list(inputs.keys())
    portals = {}
    while pending:
        position = pending.pop()
        for i, d in DIRECTIONS.items():
            response = inputs.get(position + d, ' ')
            if response != ' ':
                # print(position+d, response, position, inputs.get(position))
                if response == '#':
                    map[position + d] = '#'
                elif response == '.':
                    map[position + d] = '.'
                    # print(f'E added {position, position+d}')
                    graph.add_edge(position, position + d)
                else:
                    first_pos = position + d
                    map[first_pos] = response
                    second_char, second_pos = get_neighbouring_character(first_pos, inputs)
                    portal = ''.join(sorted([response, second_char]))
                    if portal not in portals:
                        portals[portal] = [first_pos]
                    else:
                        first_portal = portals[portal][0]
                        portals[portal].append(first_pos)
                        portals[portal].append(second_pos)
    count = 0
    
    for k, portal in portals.items():
        for i in range(len(portal)):
            for j in range(len(portal)):
                to, fro = portal[i], portal[j]
                if to != fro:
                    graph.add_edge(to, fro)
                    graph.add_edge(fro, to)
            
    
    start = 57 + 132j
    end = 132 + 55j
    # start = 19 + 2j
    # end = 2 + 17j


    path = []
    le = 0
    for node in nx.shortest_path(graph, start, end):
        if map[node] >= 'A' and map[node] <= 'Z':
            pass
        else:
            path.append(node)
            le += 1
        
    print(le-1)

# 686

if __name__ == "__main__":
    main()
    

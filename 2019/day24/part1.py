import doctest
import itertools
import copy
from collections import defaultdict
import networkx as nx
from pprint import pprint
from enum import Enum

DIRECTIONS = {1j, 1, -1, -1j}

class Biodiversity:
    def __init__(self, scenario=[]):
        self.screen = {}
        for i in range(len(scenario)):
            for j in range(len(scenario[i])):
                self.screen[i*1j + j] = scenario[i][j]

    def display(self):
        miny = int(min(v.imag for v in self.screen.keys()))
        maxy = int(max(v.imag for v in self.screen.keys()))
        minx = int(min(v.real for v in self.screen.keys()))
        maxx = int(max(v.real for v in self.screen.keys()))

        for y in range(miny, maxy + 1):
            y *= 1j
            for x in range(minx, maxx + 1):
                print(self.screen.get(x + y, ' '), end='')
            print()
        print('*'*80)

    def score(self):
        scoring = ''
        miny = int(min(v.imag for v in self.screen.keys()))
        maxy = int(max(v.imag for v in self.screen.keys()))
        minx = int(min(v.real for v in self.screen.keys()))
        maxx = int(max(v.real for v in self.screen.keys()))
        
        for y in range(miny, maxy + 1):
            y *= 1j
            order = ''
            for x in range(minx, maxx + 1):
                order += self.screen.get(x + y, '.')
            scoring += order
        print(scoring)
        ans = 0
        for i in range(len(scoring)):
            if scoring[i] == '#':
                ans += (1 << i)
        return ans

    def step(self):
        buggy = set()
        empty = set()
        for coord in self.screen:
            count = 0
            seen = set()
            for direction in DIRECTIONS:
                if self.screen.get(coord + direction, '.') == '#':
                    count += 1
                    seen.add(coord + direction)
            if self.screen[coord] == '.':
                if count == 1 or count == 2:
                    buggy.add(coord)
            else:
                if count != 1:
                    empty.add(coord)
        for coord in buggy:
            self.screen[coord] = '#'
        for coord in empty:
            self.screen[coord] = '.'
    
def parse_file(filename):
    with open(filename) as f:
        lines = []
        for line in f.readlines():
            line = line.strip()
            lines.append(line)
        return lines
            
        
TEST = 'input_test_part1.txt'
REAL = 'input.txt'

def main():
    inputs = parse_file(REAL)

    b = Biodiversity(inputs)
    b.display()
    seen_scores = set([b.score()])
    while True:
        b.step()
        b.display()
        score = b.score()
        if score in seen_scores:
            print(score)
            break
        seen_scores.add(score)
    

if __name__ == "__main__":
    main()
    

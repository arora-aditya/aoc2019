from collections import defaultdict, namedtuple
from itertools import permutations 
from pprint import pprint as print
from math import ceil

BASE_PATTERN = [0, 1, 0, -1]

def parse_file(filename):
    with open(filename) as f:
        line = f.readline()
        return [int(x) for x in line]

def repeat_list(list, times=100):
    ans = []
    for i in range(times):
        ans.extend(list)
    return ans
    
def get_pattern(output_element=1, base_pattern=BASE_PATTERN):
    ans = []
    for num in base_pattern:
        ans.extend([num]*output_element)
    return ans[1:] + ans[:1]

def get_units_digit(num):
    return int(abs(num))%10

def next_phase(current_phase):
    next_phase = []
    for i in range(len(current_phase)):
        su = 0
        pattern = get_pattern(i+1)
        # print(pattern)
        LE_P = len(pattern)
        prods = []
        for j in range(len(current_phase)):
            su += pattern[j%LE_P] * current_phase[j]
            prods.append((pattern[j%LE_P], current_phase[j]))
        next_phase.append(get_units_digit(su))
    return next_phase

def invert_ordering(ordering):
    di = defaultdict(set)
    for key, val in ordering.items():
        di[val].add(key)
    return di
            

TEST = 'input_test_part1.txt'
REAL = 'input.txt'
phase0 = parse_file(REAL)
print({0: phase0})
for i in range(1, 101):
    phase0 = next_phase(phase0)
    print({i: phase0[:8]})
    


        
    
from collections import defaultdict, namedtuple
from itertools import permutations 
from pprint import pprint as pprint
from math import ceil

import functools

BASE_PATTERN = [0, 1, 0, -1]


def parse_file(filename):
    with open(filename) as f:
        line = f.readline().strip()
        return [int(x) for x in line]

def repeat_list(list, times=10000):
    ans = []
    for i in range(times):
        ans.extend(list)
    return ans

def get_units_digit(num):
    return int(abs(num))%10

def compute_products(inputs):
    pattern = np.array(inputs['pattern']).reshape((-1, 4))
    current_phase = np.array(inputs['current_phase']).reshape((-1, 4))
    return get_units_digit(np.sum(np.multiply(current_phase, pattern)))

def next_phase(current_phase):
    dp = [0]*len(current_phase)
    next_phase = [0]*len(current_phase)
    dp[0] = current_phase[0]
    for i in range(1, len(dp)):
        dp[i] = dp[i-1] + current_phase[i]
    for j in range(len(current_phase)):
        next_phase[j] = get_units_digit(dp[-1] - dp[j] + current_phase[j])
    return next_phase
        

def get_offset(phase):
    offset_list = [str(x) for x in phase[:7]]
    offset = int(''.join(offset_list))  
    return offset

TEST = 'input_test_part2.txt'
REAL = 'input.txt'
phase0 = repeat_list(parse_file(REAL), times=10000)
offset = get_offset(phase0)
# print(offset)
# print(len(phase0))
# print({0: phase0[offset:offset+8]})
for i in range(1, 101):
    phase0 = next_phase(phase0)
print({100: phase0[offset:offset+8]})
    
# 57920757

        
    
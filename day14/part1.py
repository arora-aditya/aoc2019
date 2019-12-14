from collections import defaultdict, namedtuple
from itertools import permutations 
from pprint import pprint as print
from math import ceil

Material = namedtuple('Material', ['name', 'quantity'])

Reaction = namedtuple('Material', ['inputs', 'output'])


def parse_file(filename):
    reactions = {
        # mapping of output to reaction
    }
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            [inputs, output] = line.split(' => ')
            material_inputs = []
            reaction_inputs = {}
            for input in inputs.split(', '):
                [q, m] = input.split(' ')
                material_inputs.append(Material(m, int(q)))
            [q, m] = output.split(' ')
            material_output = Material(m.strip(), int(q))
            if material_output.name in reactions:
                print('OOFFDA')
            reactions[material_output.name] = [material_inputs, material_output]
    return reactions

def calculate_ore(reactions, ordering, ORE_DISTANCE):
    inputs_needed = defaultdict(int)
    inputs_needed['FUEL'] = 1
    for i in range(ORE_DISTANCE):
        for m in ordering[i]:
            [inputs, o] = reactions[m]
            scaling_factor = ceil(inputs_needed[o.name]/o.quantity)
            for k in inputs:
                inputs_needed[k.name] += scaling_factor*k.quantity
    return inputs_needed['ORE']

def order_reaction(reactions):
    FUEL_DISTANCE = 0
    fuel_inputs = reactions['FUEL'][0]
    level = [m.name for m in fuel_inputs]
    ordering = {'FUEL': FUEL_DISTANCE}
    FUEL_DISTANCE += 1
    while level:
        next_level = []
        while level:
            current_input = level.pop(0)
            if current_input != 'ORE':
                inputs = reactions[current_input][0]
                next_level.extend([m.name for m in inputs])
            ordering[current_input] = FUEL_DISTANCE 
        level = next_level
        FUEL_DISTANCE += 1
    return ordering, FUEL_DISTANCE - 1
    
def invert_ordering(ordering):
    di = defaultdict(set)
    for key, val in ordering.items():
        di[val].add(key)
    return di
            

TEST = 'input_test_part1.txt'
REAL = 'input.txt'
reactions = parse_file(REAL)
ordering, ORE_DISTANCE = order_reaction(reactions)
ordering = invert_ordering(ordering)
print(calculate_ore(reactions, ordering, ORE_DISTANCE))
        
    
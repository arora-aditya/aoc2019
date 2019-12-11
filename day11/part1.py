from collections import defaultdict, namedtuple
from itertools import permutations 
from pprint import pprint as print


Point = namedtuple('Point', ['x', 'y', 'direction'])
current_pos = Point(x=0, y=0, direction='UPUP')
positions = {}


def parse_instruction(ins):
    if len(ins) < 5:
        ins = '0'*(5-len(ins)) + ins
    sizes = {
        1: 4,
        2: 4,
        3: 2,
        4: 2,
        5: 3,
        6: 3,
        7: 4,
        8: 4,
        9: 2,
        99: -1,
    }
    param_modes = None
    opcode = int(ins[-2:])
    
    param_modes = [int(ins[2]), int(ins[1]), int(ins[0]),]
    size = sizes[opcode]
    return opcode, size, param_modes

def get_index(L, index):
    if index < 0:
        return 'aodjsioahdfioahodas'
    if index >= len(L):
        elements_to_add = [0]*(index - len(L)+1)
        L.extend(elements_to_add)
    # print(f'Aget({index} {len(L)}) = {L[index]}')
    return L, L[index]

def set_index(L, index, value):
    if index < 0:
        return 'aodjsioahdfioahodas'
    if index >= len(L):
        elements_to_add = [0]*(index - len(L)+1)
        L.extend(elements_to_add)
    L[index] = value
    # print(f'Aset({index} {len(L)}) = {L[index]}')
    return L, index

def param_mode(L, mode, index, relative_base):
    if mode == 0:
        L, _ans = get_index(L, index)
        L, ans = get_index(L, _ans)
    elif mode == 1:
        L, ans = get_index(L, index)
    elif mode == 2:
        L, _ans = get_index(L, index)
        L, ans = get_index(L, relative_base + _ans)
    return ans

def diff(before, after, new_i, relative_base):
    flag = True
    for i in range(len(before)):
        if before[i] != after[i]:
            print(f'index {i} {before[i]} --> {after[i]} {new_i} {relative_base}')
            flag = False
    if len(before) != len(after):
        print(f'{len(after) - len(before)} extended')
        for i in range(len(before), len(after)):
            if after[i] != 0:
                print(f'index {i} "NA" --> {after[i]} {new_i} {relative_base}')
    if flag:
        print(f'--------------- {new_i} {relative_base}')
    

def run(L, input_signals, i, relative_base):
    global position
    flag = True
    halted = False
    outputs = []
    # print(L, None, None, [], relative_base, i, outputs)
    while i < len(L):
        opcode, size, param_modes = parse_instruction(str(L[i]))
        # print(opcode, size, param_modes, i)
        before = L[:]
        new_i = None
        if opcode == 99:
            print('HALT')
            halted = True
            break
        elif opcode == 1:
            val = param_mode(L, param_modes[0], i+1, relative_base) + param_mode(L, param_modes[1], i+2, relative_base)
            L, _index = get_index(L, i+3)
            if param_modes[2] == 2:
                _index = relative_base + _index
            L, index = set_index(L, _index, val)
        elif opcode == 2:
            val = param_mode(L, param_modes[0], i+1, relative_base) * param_mode(L, param_modes[1], i+2, relative_base)
            L, _index = get_index(L, i+3)
            if param_modes[2] == 2:
                _index = relative_base + _index
            L, index = set_index(L, _index, val)
        elif opcode == 3:
            _index = L[i+1]
            if param_modes[0] == 2:
                _index = relative_base + L[i+1]
            if current_pos._replace(direction='YEE') in positions:
                color_of_current_pos = positions[current_pos._replace(direction='YEE')]
            else: 
                color_of_current_pos = 0
            # print({'INPUT': [current_pos, color_of_current_pos]})
            L, index = set_index(L, _index, color_of_current_pos)
        elif opcode == 4:
            ot = param_mode(L, param_modes[0], i+1, relative_base)
            outputs.append(ot)
            break
            # print('OUTPUT', output)
        elif opcode == 5:
            if param_mode(L, param_modes[0], i+1, relative_base) != 0:
                new_i = param_mode(L, param_modes[1], i+2, relative_base)
        elif opcode == 6:
            if param_mode(L, param_modes[0], i+1, relative_base) == 0:
                new_i = param_mode(L, param_modes[1], i+2, relative_base)
        elif opcode == 7:
            if param_mode(L, param_modes[0], i+1, relative_base) < param_mode(L, param_modes[1], i+2, relative_base):
                val = 1
            else:
                val = 0
            # print(f'<{param_mode(L, param_modes[0], i+1, relative_base)}{param_mode(L, param_modes[1], i+2, relative_base)}{val}')
            L, _index = get_index(L, i+3)
            if param_modes[2] == 2:
                _index = relative_base + _index
            L, index = set_index(L, _index, val)
        elif opcode == 8:
            if param_mode(L, param_modes[0], i+1, relative_base) == param_mode(L, param_modes[1], i+2, relative_base):
                val = 1
            else:
                val = 0
            # print(f'={param_mode(L, param_modes[0], i+1, relative_base)},{param_mode(L, param_modes[1], i+2, relative_base)},{val}')
            L, _index = get_index(L, i+3)
            if param_modes[2] == 2:
                _index = relative_base + _index
            L, index = set_index(L, _index, val)
        elif opcode == 9:
            offset = param_mode(L, param_modes[0], i+1, relative_base)
            relative_base += offset
        # diff(before, L, new_i, relative_base)
        i += size
        if new_i is not None:
            i = new_i
        # print(L, opcode, size, param_modes, relative_base, i, outputs)
        # input()
    # print(L, opcode, size, param_modes, relative_base, i, outputs)
    # input()
    return L, outputs, i+size, halted, input_signals, relative_base

def change_direction(current_direction, movement):
    if current_direction == 'UPUP':
        if movement == 0:
            return 'LEFT'
        else:
            return 'RIGHT'
    elif current_direction == 'DOWN':
        if movement == 0:
            return 'RIGHT'
        else:
            return 'LEFT'
    elif current_direction == 'LEFT':
        if movement == 0:
            return 'DOWN'
        else:
            return 'UPUP'
    elif current_direction == 'RIGHT':
        if movement == 0:
            return 'UPUP'
        else:
            return 'DOWN'
    else:
        print('BIG OOF')

def move(current_pos):
    current_direction = current_pos.direction
    x, y = current_pos.x, current_pos.y
    if current_direction == 'UPUP':
        current_pos = current_pos._replace(y=y+1)
    elif current_direction == 'DOWN':
        current_pos = current_pos._replace(y=y-1)
    elif current_direction == 'LEFT':
        current_pos = current_pos._replace(x=x-1)
    elif current_direction == 'RIGHT':
        current_pos = current_pos._replace(x=x+1)
    else:
        print('BIG OOF')
    return current_pos

def amplify(L):
    global current_pos
    c1 = ([], L[:], 0, 0)
    
    comps = [c1]
    outputs = []
    while comps:
        inputs, cmds, pointer, relative_base = comps.pop(0)
        new_inputs = inputs
        cmds, output, pointer, halted, inputs, relative_base = run(cmds, new_inputs, pointer, relative_base)
        # print('*'*80, output, '*'*80)
        outputs.extend(output)
        if len(outputs) % 2 == 0:
            new_color, movement = outputs[-2], outputs[-1]
            new_direction = change_direction(current_pos.direction, movement)
            current_pos = current_pos._replace(direction=new_direction)
            positions[current_pos._replace(direction='YEE')] = new_color
            current_pos = move(current_pos)
        if not halted:
            comps.append((inputs, cmds, pointer, relative_base))
        else:
            break
    return outputs

with open('input.txt') as f:
    line = f.readline()
    L = list(map(int, line.split(',')))
        
    outputs = amplify(L)
    # print(positions)
    print(len(positions))
    
        
    
        
# 44292


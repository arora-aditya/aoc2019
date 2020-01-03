from collections import defaultdict
from itertools import permutations 

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
            L, index = set_index(L, _index, input_signals.pop(0))
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

def amplify(L):
    c1 = ([2], L[:], 0, 0)
    
    comps = [c1]
    outputs = []
    while comps:
        inputs, cmds, pointer, relative_base = comps.pop(0)
        new_inputs = inputs + outputs
        cmds, output, pointer, halted, inputs, relative_base = run(cmds, new_inputs, pointer, relative_base)
        outputs.extend(output)
        if not halted:
            comps.append((inputs, cmds, pointer, relative_base))
        else:
            break
    return outputs

with open('input.txt') as f:
    line = f.readline()
    L = list(map(int, line.split(',')))
    outputs = []
    print(amplify(L))
        
# 44292


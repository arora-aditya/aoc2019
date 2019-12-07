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
        99: -1,
    }
    param_modes = None
    opcode = int(ins[-2:])
    
    if opcode == 1 or opcode == 2:
        param_modes = [int(ins[2]), int(ins[1]), int(ins[0]),]
    if opcode >= 4:
        param_modes = [int(ins[2]), int(ins[1]), int(ins[0]),]
    size = sizes[opcode]
    return opcode, size, param_modes

def param_mode(L, mode, index):
    if mode == 0:
        return L[L[index]]
    else:
        return L[index]

def diff(before, after, new_i):
    flag = True
    for i in range(len(before)):
        if before[i] != after[i]:
            print(f'index {i} {before[i]} --> {after[i]} {new_i}')
            flag = False
    if flag:
        print(f'--------------- {new_i}')
    

def run(line, phase, input_signal):
    L = list(map(int, line.split(',')))
    i = 0    
    flag = True
    output = None
    while i < len(L):
        opcode, size, param_modes = parse_instruction(str(L[i]))
        before = L[:]
        new_i = None
        if opcode == 99:
            # print('HALT')
            break
        elif opcode == 1:
            # print(f'+{L[i:i+4]}\t{param_mode(L, param_modes[0], i+1)}\t{param_mode(L, param_modes[1], i+2)}')
            L[L[i+3]] = param_mode(L, param_modes[0], i+1) + param_mode(L, param_modes[1], i+2)
        elif opcode == 2:
            # print(f'*{L[i:i+4]}\t{param_mode(L, param_modes[0], i+1)}\t{param_mode(L, param_modes[1], i+2)}')
            L[L[i+3]] = param_mode(L, param_modes[0], i+1) * param_mode(L, param_modes[1], i+2)
        elif opcode == 3:
            # print(f'_{L[i:i+2]}')
            if flag:
                # print(f'PHASE INPUTTED {phase}')
                L[L[i+1]] = phase
                flag = False
            else:
                # print(f'INPUT INPUTTED {input_signal}')
                L[L[i+1]] = input_signal
        elif opcode == 4:
            # print(f'^{L[i:i+2]}')
            output = param_mode(L, param_modes[0], i+1)
            # print('OUTPUT', output)
        elif opcode == 5:
            # print(f'N{L[i:i+3]}')
            if param_mode(L, param_modes[0], i+1) != 0:
                new_i = param_mode(L, param_modes[1], i+2)
        elif opcode == 6:
            # print(f'Z{L[i:i+3]}')
            if param_mode(L, param_modes[0], i+1) == 0:
                new_i = param_mode(L, param_modes[1], i+2)
        elif opcode == 7:
            # print(f'<{L[i:i+4]}')
            if param_mode(L, param_modes[0], i+1) < param_mode(L, param_modes[1], i+2):
                L[L[i+3]] = 1
            else:
                L[L[i+3]] = 0
        elif opcode == 8:
            # print(f'={L[i:i+4]} {param_modes}')
            if param_mode(L, param_modes[0], i+1) == param_mode(L, param_modes[1], i+2):
                L[L[i+3]] = 1
            else:
                L[L[i+3]] = 0
        # diff(before, L, new_i)
        i += size
        if new_i:
            i = new_i
    return output

def inputs():
    li = list(range(5))
    for l in permutations(li):
        yield l

with open('input.txt') as f:
    line = f.readline()
    max_output = -float('inf')
    
    for i in inputs():
        output = 0
        for k in range(5):
            output = run(line, i[k], output)
        max_output = max(max_output, output)
    print(max_output)
        
# 46248

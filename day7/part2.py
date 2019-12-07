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
    

def run(L, input_signals, i=0):
    flag = True
    halted = False
    outputs = []
    while i < len(L):
        opcode, size, param_modes = parse_instruction(str(L[i]))
        before = L[:]
        new_i = None
        if opcode == 99:
            # print('HALT')
            halted = True
            break
        elif opcode == 1:
            # print(f'+{L[i:i+4]}\t{param_mode(L, param_modes[0], i+1)}\t{param_mode(L, param_modes[1], i+2)}')
            L[L[i+3]] = param_mode(L, param_modes[0], i+1) + param_mode(L, param_modes[1], i+2)
        elif opcode == 2:
            # print(f'*{L[i:i+4]}\t{param_mode(L, param_modes[0], i+1)}\t{param_mode(L, param_modes[1], i+2)}')
            L[L[i+3]] = param_mode(L, param_modes[0], i+1) * param_mode(L, param_modes[1], i+2)
        elif opcode == 3:
            # print(f'_{L[i:i+2]}')
            L[L[i+1]] = input_signals.pop(0)
        elif opcode == 4:
            # print(f'^{L[i:i+2]}')
            outputs.append(param_mode(L, param_modes[0], i+1))
            break
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
    return L, outputs, i+size, halted, input_signals

def inputs():
    li = list(range(5, 10))
    for l in permutations(li):
        yield l

def amplify(phases, L):
    [p1, p2, p3, p4, p5] = phases
    c1 = ([p1], L[:], 0)
    c2 = ([p2], L[:], 0)
    c3 = ([p3], L[:], 0)
    c4 = ([p4], L[:], 0)
    c5 = ([p5], L[:], 0)
    
    comps = [c1, c2, c3, c4, c5]
    outputs = [0]
    while comps:
        inputs, cmds, pointer = comps.pop(0)
        new_inputs = inputs + outputs
        cmds, outputs, pointer, halted, inputs = run(cmds, new_inputs, pointer)
        if not halted:
            comps.append((inputs, cmds, pointer))
        else:
            outputs = new_inputs
            break
    return outputs[0]

with open('input.txt') as f:
    line = f.readline()
    L = list(map(int, line.split(',')))
    max_output = -float('inf')
    ans = None
    for i in inputs():
        output = amplify(i, L)
        if max_output < output:
            max_output = output
            ans = i
    print(max_output, ans)
        
# 54163586


from collections import defaultdict

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
    

with open('input.txt') as f:
    line = f.readline()
    L = list(map(int, line.split(',')))
    i = 0    
        
    while i < len(L):
        opcode, size, param_modes = parse_instruction(str(L[i]))
        before = L[:]
        new_i = None
        if opcode == 99:
            print('HALT')
            break
        elif opcode == 1:
            # print(f'+{L[i:i+4]}\t{param_mode(L, param_modes[0], i+1)}\t{param_mode(L, param_modes[1], i+2)}')
            L[L[i+3]] = param_mode(L, param_modes[0], i+1) + param_mode(L, param_modes[1], i+2)
        elif opcode == 2:
            # print(f'*{L[i:i+4]}\t{param_mode(L, param_modes[0], i+1)}\t{param_mode(L, param_modes[1], i+2)}')
            L[L[i+3]] = param_mode(L, param_modes[0], i+1) * param_mode(L, param_modes[1], i+2)
        elif opcode == 3:
            # print(f'_{L[i:i+2]}')
            L[L[i+1]] = 5
        elif opcode == 4:
            # print(f'^{L[i:i+2]}')
            print('OUTPUT', param_mode(L, param_modes[0], i+1))
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
        diff(before, L, new_i)
        i += size
        if new_i:
            i = new_i
# 2808771

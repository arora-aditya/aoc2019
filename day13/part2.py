from collections import defaultdict, namedtuple
from itertools import permutations 
from pprint import pprint as pprint
import os
import time

Point = namedtuple('Point', ['x', 'y', 'direction'])
current_pos = Point(x=0, y=0, direction='UPUP')
joysticks = []
board = [['']*44 for j in range(22)]
SLEEP = 0.001

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
    global board
    global SLEEP
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
            joystick = None
            SLEEP = 0.006
            BALL, PADDLE = ball_paddle(board)
            if BALL > PADDLE:
                joystick = 1
            elif BALL < PADDLE:
                joystick = -1
            else:
                joystick = 1
            force = input()
            if force != '':
                joystick = int(force)
            print(BALL, PADDLE, joystick)
            joysticks.append(joystick)
            L, index = set_index(L, _index, joystick)
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

def tile(val):
    if val == 0:
        return ' '
    elif val == 1:
        return 'H'
    elif val == 2:
        return 'X'
    elif val == 3:
        return '_'
    elif val == 4:
        return 'O'

def ball_paddle(board):
    BALL = None
    PADDLE = None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'O':
                BALL = j
            if board[i][j] == '_':
                PADDLE = j
    return BALL, PADDLE

def amplify(L):
    global SLEEP
    global current_pos
    c1 = ([], L[:], 0, 0)
    
    comps = [c1]
    outputs = []
    count = 0
    scores = [0]
    score = 0
    while comps:
        inputs, cmds, pointer, relative_base = comps.pop(0)
        new_inputs = inputs
        cmds, output, pointer, halted, inputs, relative_base = run(cmds, new_inputs, pointer, relative_base)
        # print('*'*80, output, '*'*80)
        outputs.extend(output)
        if len(outputs) % 3 == 0:
            val, y, x = outputs[-1], outputs[-2], outputs[-3]
            if x == -1 and y == 0:
                score = val
            else:
                board[y][x] = tile(val)
        if not halted:
            comps.append((inputs, cmds, pointer, relative_base))
        else:
            break
        # os.system('clear') 
        for row in board:
            print(''.join(row))
        if score != scores[-1]:
            scores.append(score)
        print(f'*SCORE:{score}')
        time.sleep(SLEEP)
        
    return scores

with open('input.txt') as f:
    line = f.readline()
    L = list(map(int, line.split(',')))
    L[0] = 2
    outputs = amplify(L)
    # print(positions)
    # print('\n'.join([str(x) for x in joysticks]))
    with open('last_run_auto.txt', 'w+') as f:
        f.write('\n'.join([str(x) for x in joysticks]))
    
        
    
        
# 44292


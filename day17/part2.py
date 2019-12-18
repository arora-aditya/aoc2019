import doctest
import itertools
import copy
import networkx as nx
# derivative code of nigelzor



def decode_instr(intcode):
    """
    >>> decode_instr(1002)
    (2, 0, 1, 0)
    >>> decode_instr(1108)
    (8, 1, 1, 0)
    """
    op = intcode % 100
    modes = intcode // 100
    mode_c = modes % 10
    modes = modes // 10
    mode_b = modes % 10
    modes = modes // 10
    mode_a = modes % 10
    return op, mode_c, mode_b, mode_a


class Simulator:
    def __init__(self, program, inputs=None):
        self.program = program
        self.program.extend(0 for _ in range(10000))
        self.ip = 0
        self.rb = 0
        self.inputs = iter(inputs or [])

    def run_to_completion(self, inputs=None):
        if inputs:
            self.inputs = itertools.chain(self.inputs, inputs)
        outputs = []
        while True:
            out = self.simulate()
            if out is None:
                break
            outputs.append(out)
        return outputs

    def run_to_output(self, inputs=None):
        if inputs:
            self.inputs = itertools.chain(self.inputs, inputs)
        return self.simulate()

    def simulate(self):
        while True:
            inst = decode_instr(self.program[self.ip])
            op = inst[0]

            # print('ip={} inst={}'.format(ip, inst))
            def in_arg(n):
                value = self.program[self.ip + n]
                mode = inst[n]
                if mode == 0:
                    return self.program[value]
                elif mode == 1:
                    return value
                elif mode == 2:
                    return self.program[value + self.rb]
                else:
                    raise Exception(f"Invalid mode {mode} at {self.ip}:{self.program[self.ip]}")

            def out_arg(n, value):
                mode = inst[n]
                addr = self.program[self.ip + n]
                if mode == 0:
                    self.program[addr] = value
                elif mode == 2:
                    self.program[addr + self.rb] = value
                else:
                    raise Exception(f"Invalid mode {mode} at {self.ip}:{self.program[self.ip]}")

            if op == 1:
                a = in_arg(1)
                b = in_arg(2)
                out_arg(3, a + b)
                self.ip += 4
            elif op == 2:
                a = in_arg(1)
                b = in_arg(2)
                out_arg(3, a * b)
                self.ip += 4
            elif op == 3:
                out_arg(1, next(self.inputs))
                self.ip += 2
            elif op == 4:
                a = in_arg(1)
                self.ip += 2
                return a
            elif op == 5:
                a = in_arg(1)
                b = in_arg(2)
                if a != 0:
                    self.ip = b
                else:
                    self.ip += 3
            elif op == 6:
                a = in_arg(1)
                b = in_arg(2)
                if a == 0:
                    self.ip = b
                else:
                    self.ip += 3
            elif op == 7:
                a = in_arg(1)
                b = in_arg(2)
                out_arg(3, int(a < b))
                self.ip += 4
            elif op == 8:
                a = in_arg(1)
                b = in_arg(2)
                out_arg(3, int(a == b))
                self.ip += 4
            elif op == 9:
                a = in_arg(1)
                self.rb += a
                self.ip += 2
            elif op == 99:
                return
            else:
                raise Exception(f"Invalid opcode {op} at {self.ip}:{self.program[self.ip]}")

def display(screen):
    miny = int(min(v.imag for v in screen.keys()))
    maxy = int(max(v.imag for v in screen.keys()))
    minx = int(min(v.real for v in screen.keys()))
    maxx = int(max(v.real for v in screen.keys()))

    for y in range(miny, maxy + 1):
        print(y, end='\t')
        y *= 1j
        for x in range(minx, maxx + 1):
            print(screen.get(x + y, ' '), end='')
        print()

DIRECTIONS = {
    'D' : 1j,
    'R' : 1,
    'L' : -1,
    'U' : -1j,
}

def invert_ordering(ordering):
    di = {}
    for key, val in ordering.items():
        di[val] = key
    return di

def compress(path):
    prev = path[0]
    ans = []
    i = 0
    rotation = 'L'
    prev_direction, count = 'U', 0
    
    INVERTED_DIRECTIONS =  invert_ordering(DIRECTIONS)

    ROTATE = {
            ('U', 'R'): 'R',
            ('U', 'L'): 'L',
            ('R', 'D'): 'R',
            ('R', 'U'): 'L',
            ('D', 'L'): 'R',
            ('D', 'R'): 'L',
            ('L', 'U'): 'R',
            ('L', 'D'): 'L',
    }
    
    while i < len(path):
        count = 0
        while i + count < len(path) and path[i] == path[i+count]:
            count += 1
        ans.extend(
            [ROTATE[(
                    prev_direction, 
                    INVERTED_DIRECTIONS[path[i]]
                )], 
                str(count)
            ]
        )
        prev_direction = INVERTED_DIRECTIONS[path[i]]
        i = i + count
    return ','.join(ans)

def main():
    with open('input.txt') as f:
        initial_program = [int(x) for x in f.readlines()[0].split(',')]

    initial_program[0] = 2
    map = {}

    pending = []
    pending.append((0, Simulator(initial_program.copy())))
    y,x = 0,0
    count = 0
    
    start = -1
    
    while pending:
        position, program = pending.pop()
        subprogram = copy.deepcopy(program)
        try:
            response = subprogram.run_to_output()
        except Exception as e:
            # exception raised when it demands output when I have none
            break
        for i, num in enumerate([response]):
            if num == 10:
                y += 1j
                x = 0
            elif num == 46:
                map[y + x] = chr(num) 
                x += 1
            elif num == 35:
                map[y + x] = chr(num)
                x += 1
            else:
                if count == 0:
                    map[y + x] = chr(num)
                    start = y + x
                else:
                    map[y + x] = chr(num)
                count += 1
                flag = True
                x += 1            
        pending.append((subprogram.ip, subprogram))
        
    map[start] = '#'
    pos = start
    
    path = []
    
    direction = -1
    count = 0
    while map.get(pos, '?'):
        count += 1
        if map.get(pos, '?') != '#':
            prev_direction = direction
            pos -= prev_direction
            for key, new_direction in DIRECTIONS.items():
                if map.get(pos + new_direction, '?') == '#' and new_direction != -1 * prev_direction:
                    direction = new_direction
                    break
            if direction == prev_direction:
                break
            count = 0
            pos += new_direction
        path.append(direction)
        pos += direction
    
    path.pop(0)

    path = compress(path)
    
    MAIN = "A,B,B,C,C,A,A,B,B,C"
    A = "L,12,R,4,R,4"
    B = "R,12,R,4,L,12"
    C = "R,12,R,4,L,6,L,8,L,8"
    inputs = list(ord(x) for x in MAIN + "\n" + A + "\n" + B + "\n" + C + "\n\n\n\n")
    
    pending.append((0, Simulator(initial_program.copy(), inputs)))
    
    while pending:
        position, program = pending.pop()
        subprogram = copy.deepcopy(program)
        # try:
        response = subprogram.run_to_completion()
        y,x = 0,0
        print(response[-1])

if __name__ == "__main__":
    doctest.testmod()
    main()
    
# 923017
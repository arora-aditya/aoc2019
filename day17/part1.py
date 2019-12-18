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


def main():
    with open('input.txt') as f:
        initial_program = [int(x) for x in f.readlines()[0].split(',')]
    
    map = [['']*59 for i in range(39)]
    
    pending = []
    pending.append((0, Simulator(initial_program.copy())))
    while pending:
        position, program = pending.pop()
        subprogram = copy.deepcopy(program)
        response = subprogram.run_to_completion()
        y,x = 0,0
        for i, num in enumerate(response):
            if num == 10:
                y += 1
                x = 0
            elif num == 46:
                map[y][x] = '.' 
                x += 1
            elif num == 35:
                map[y][x] = '#' 
                x += 1
            else:
                map[y][x] = 'X'
                x += 1
        for i in range(-1, len(map[0])):
            print(str(i).ljust(3, ' '), end='')
        print('')
        for i, row in enumerate(map):
            print(str(i).rjust(2, '0'), ''.join([str(x)+'  ' for x in row]))
        
        deltas = [[0, -1], [1, 0], [0, 1], [-1, 0]]
        su = 0
        for j, row in enumerate(map):
            for i, val in enumerate(row):
                if map[j][i] == '#':
                    ct = 0
                    for [dj, di] in deltas:
                        if j + dj < 0 or i + di < 0 or j + dj >= len(map) or i + di >= len(row):
                            break
                        else:
                            
                            if map[j+dj][i+di] == '#':
                                ct += 1
                            else:
                                break
                    if ct == 4:
                        su += j*i
        print(su)    
        # print(len(response), (len(response)-1)/60)

# 6672

if __name__ == "__main__":
    doctest.testmod()
    main()
    
# 272
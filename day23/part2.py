import doctest
import itertools
import copy
import networkx as nx
from collections import defaultdict
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
            if type(out) == type(True):
                break
            outputs.append(out)
        self.out = outputs

    def run_to_output(self, inputs=None):
        if inputs:
            self.inputs = itertools.chain(self.inputs, inputs)
        return self.simulate()
        
    def simulate(self):
        while True:
            inst = decode_instr(self.program[self.ip])
            op = inst[0]

            # print(f'ip={self.ip} inst={inst}')
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
                try:
                    out_arg(1, next(self.inputs))
                except:
                    return False
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
                return True
            else:
                raise Exception(f"Invalid opcode {op} at {self.ip}:{self.program[self.ip]}")

        
def main():
    with open('input.txt') as f:
        initial_program = [int(x) for x in f.readlines()[0].split(',')]
    
    computers = {}
    
    for i in range(50):
        computers[i] = Simulator(initial_program.copy(), inputs=[i])
        computers[i].run_to_completion()
    
    p1, p2 = None, None
    
    while True:
        Q = defaultdict(list)
        if all(not len(computers[i].out) for i in range(50)) and p1:
            computers[0].run_to_completion(inputs=[*p1])
            if p2 and p1[1] == p2[1]: break
            p2 = p1
        for i in range(50):
            while computers[i].out:
                d, x, y = computers[i].out[:3]
                del computers[i].out[:3]
                if d == 255: p1 = (x, y)
                else: Q[d] += [x, y]
        if 255 in Q:
            break
        for i in range(50):
            computers[i].run_to_completion(inputs=Q.get(i, [-1]))
    
    print(p1[1])

# 14370

if __name__ == "__main__":
    doctest.testmod()
    main()
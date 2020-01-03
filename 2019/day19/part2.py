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


def test_point(x, y, program, map):
    subprogram = Simulator(program.copy(), inputs=[x, y])
    response = subprogram.run_to_output()
    map[x + y*1j] = response
    return response

def main():
    with open('input.txt') as f:
        initial_program = [int(x) for x in f.readlines()[0].split(',')]
    
    map = {}
    
    size = 100
    x, y = 0, 0
    while True:
        if y >= size - 1:
            if test_point(x + size - 1, y - size + 1, initial_program, map):
                x, y = x, y - size + 1
                break

        i = 0
        passed = False
        while not (passed := test_point(x + i, y + 1, initial_program, map)) and i <= 10:
            i += 1
        
        if passed:
            x = x + i
        y = y + 1
    print(x*10000 + y)
        
# 9231141

if __name__ == "__main__":
    doctest.testmod()
    main()
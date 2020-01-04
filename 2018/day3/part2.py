from collections import Counter

class Fabric:
    def __init__(self, line='#123 @ 3,2: 5x4\n'):
        if line is not None:
            line = line.split(' ')
            self.claim_no = int(line[0][1:])
            self.top_left = list(map(int, line[2][:-1].split(',')))
            width, height = list(map(int, line[3].split('x')))
            self.width = width
            self.height = height
            cs = []
            for i in range(self.top_left[0], self.top_left[0] + width):
                for j in range(self.top_left[1], self.top_left[1] + height):
                    cs.append((i, j))
            self.coordinates = set(cs)
        else:
            self.claim_no = None
            self.top_left = None
            self.width = None
            self.height = None
    
    def __str__(self):
        return (f'C: {self.claim_no} TL: {self.top_left} ' + 
            f'W: {self.width} H: {self.height} CS: {list(sorted(self.coordinates))}')
        
    def __and__(self, other):
        f = Fabric(None)
        f.coordinates = self.coordinates & other.coordinates
        return f
    
    def __or__(self, other):
        f = Fabric(None)
        f.coordinates = self.coordinates | other.coordinates
        return f

with open("input.txt", "r") as f:
    lines = f.readlines()
    fabrics = []
    for line in lines:
        fabrics.append(Fabric(line))
    
    for i in range(len(fabrics)):
        this = set()
        for j in range(len(fabrics)):
            if i != j:
                this |= (fabrics[i] & fabrics[j]).coordinates
        if len(this) == 0:
            print(fabrics[i])
# 560
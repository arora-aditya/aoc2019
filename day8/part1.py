from collections import defaultdict
from itertools import permutations 


with open('input.txt') as f:
    line = [int(x) for x in f.readline()]
    L = len(line)
    W, H = 25, 6
    S = H*W
    min_zeros, ans = float('inf'), None
    for i in range(L//S):
        layer = line[i*S:(i+1)*S]
        num_zeros, num_ones, num_twos = layer.count(0), layer.count(1), layer.count(2)
        if num_zeros < min_zeros:
            min_zeros = num_zeros
            ans = num_ones * num_twos
    print(ans)
        
# 1206

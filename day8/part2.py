from collections import defaultdict
from itertools import permutations 
import numpy as np
from pprint import pprint as print
from PIL import Image

def get_pixel(row):
    for i in row:
        if i < 2:
            return i

with open('input.txt') as f:
    line = [int(x) for x in f.readline()]
    L = len(line)
    W, H = 25, 6
    S = H*W
    layers = []
    for i in range(L//S):
        layer = line[i*S:(i+1)*S]
        layers.append(layer)
        # print(len(layer), num_zeros, num_ones, num_twos )
    ans = layers[-1]
    transposed = np.transpose(layers)
    for i in range(len(transposed)):
        ans[i] = get_pixel(transposed[i])
    # print(len(test[0]))
    # print(test[0])
    ans = [ans[j*W:(j+1)*W] for j in range(H)]
    print(ans)
    im = Image.fromarray(np.array(ans).reshape((H,W)).astype('uint8')*255)
    im.save('answer_part2.png')
    
# EJRGP

import doctest
import itertools
import copy
from collections import defaultdict
import networkx as nx
from pprint import pprint
from enum import Enum

class Deck:
    def __init__(self, total):
        self.deck = list(range(total))
    
    def cut(self, cut):
        self.deck = self.deck[cut:] + self.deck[:cut] 
    
    def deal_with_increment(self, increment):
        le = len(self.deck)
        new_deck = [None]*le
        empty = False
        current_position = 0
        while not empty:
            try:
                card = self.deck.pop(0)
                new_deck = new_deck[:current_position] + [card] + new_deck[current_position+1:]
                current_position += increment
                current_position %= le
                empty = False
            except:
                empty = True
        self.deck = new_deck[:]

    def deal_with_new_stack(self):
        self.deck = self.deck[::-1]

class State(Enum):
    CUT = 1
    DEAL_NEW_STACK = 2
    DEAL_INCREMENT = 3

def parse_file(filename):
    string_to_state = {
        'deal with increment': State.DEAL_INCREMENT,
        'deal into new': State.DEAL_NEW_STACK,
        'cut': State.CUT,
    }
    with open(filename) as f:
        lines = []
        for line in f.readlines():
            line = line.split(' ')
            state = string_to_state[' '.join(line[:-1])]
            val = None
            if state != State.DEAL_NEW_STACK:
                val = int(line[-1])
            lines.append((state, val,))
        return lines
            
        
TEST = 'input_test_part1.txt'
REAL = 'input.txt'

def main():
    deck = Deck(10007)
    
    inputs = parse_file(REAL)
    
    for i, (state, val) in enumerate(inputs):
        print(i, end='\r')
        if state == State.CUT:
            deck.cut(val)
        elif state == State.DEAL_NEW_STACK:
            deck.deal_with_new_stack()
        else:
            deck.deal_with_increment(val)

    print(deck.deck.index(2019))
    

if __name__ == "__main__":
    main()
    

import sys
sys.path.append('..')
from utils.imports import *
'''
import matplotlib.pyplot as plt
import numpy as np
import itertools as iter
import re as re
import math as math
import itertools as it
'''
file = 'test1.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]


#d = data[0]


def find_candidates(springs):
    # group candidates
    candidates = []
    in_group = False
    i = 0
    while i < len(springs):
        if in_group:
            if i == len(springs)-1:
                if d[i] == '.':
                    #print((i,d[i]))
                    in_group = False
                    stop = i-1
                    candidates.append((start, stop))
                else:
                    stop = i
                    candidates.append((start, stop))
            elif d[i] == '.':
                #print((i,d[i]))
                in_group = False
                stop = i-1
                candidates.append((start, stop))        
        else:
#            print((i,d[i]))
            if d[i] != '.':
                in_group=True
                start = i
        i = i + 1 
    return candidates

for d in data:
    springs, groups = d.split(' ')
    groups = [int(g) for g in groups.split(',')]
    candidates = find_candidates(springs)
    print('--------')
    print(springs)
    print(candidates)
    print(len(springs))
    print(groups)
    #print(len(candidates)<=len(groups))
'''
Längden på varje group och candidate säger nåt om kombinationerna, 
Om man har en grupp som är lika lång som candidate så är man klar. 

Om en candidadet börjar eller slutar med # så måste man lägga ut gruppen över start/slut. 
Dessa två är det första man gör för att reducera problemet. Baserat på det tidigare så får man krympa candidate så man inte får dubbla #. 

? Hur hantera de olika alternativen. Nåt träd? 

problemet kan lösas för varje candidate. Antal kombos fås genom produkten av canidatealternativen
Som sagt ovan. Först kollar man slut och början. Om de är något bestämt så gör man candiate mindre. 
Sedan måste man skapa olika alternativ oc hålla reda på dem.
'''

d = data[1]

springs, groups = d.split(' ')
groups = [int(g) for g in groups.split(',')]
candidates = find_candidates(springs)
print(springs)
print(candidates)
print(len(springs))
print(groups)
springs = '.#??.???#.#?#'
groups = [1,2,3]
candidates = [[1,3], [5,8], [10,12]]
arrs = [[springs[:candidates[0][0]]]]
# måste tänke ut en struktur för alternativen,. jag kommer inte få ordning på det annars. 

for candidate in candidates:
    if springs[candidate[0]]=='#':
        one_arr =  ['#' for i in range(candidate[1]-candidate[0]+1)]
print(arrs)

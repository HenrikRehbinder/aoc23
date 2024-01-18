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

group_sizes kommer i den ordningen som de listas.
'''

d = data[1]

springs, groups = d.split(' ')
group_sizes = [int(g) for g in groups.split(',')]
candidates = find_candidates(springs)
print(springs)
print(candidates)
print(len(springs))
print(groups)
#springs = '.#??.???#.#??????#'
#springs = list(springs)
#group_sizes = [1,2,3]
#candidates = [[1,3], [5,8], [10,17]]
'''
arrs = [[springs[:candidates[0][0]]]]
# måste tänke ut en struktur för alternativen,. jag kommer inte få ordning på det annars. 
i = 1

candidate = candidates[i]
group_size = 3

ind = candidates[0][0]
spring_alternatives = [dict((
    ('springs',[s for s in springs]),
    ('ind', ind),
    ('candidates', candidates),
    ('ok', True)
    ))]
'''

class SpringAlternative:
    def __init__(self, springs, ind, rem_candidates, rem_groups):
        self.springs = springs[ind:]
        self.decided_springs = []
        self.candidates = [[c[0]-ind, c[1]-ind] for c in rem_candidates]
        self.groups = rem_groups
        self.children = []
        self.ok = True


    def test_status(self):
        if len(self.candidates) == 0:
            self.ok = True
        elif (
            (len(self.candidates) == 1) and 
            (sum(self.groups)>(self.candidates[1] - self.candidates[0]+1))
            ):
                self.ok = False


    def make_alternatives(self):
        alt_ind = []
        if self.springs[self.candidates[0][0]] == '#':
            next_ind = self.groups[0]+1 # for the necessary '.'
            alt_ind.append(next_ind)
            self.decided_springs.append(['#' for i in range(self.groups[0])])
        else:
            shift = 0
            while shift + self.groups[0] <= self.candidates[0][1]:
                self.decided_springs.append(
                    ['.' for i in range(shift)] + 
                    ['#' for i in range(self.groups[0])]
                    )
                shift += 1
        for ds in self.decided_springs:
            self.children.append(SpringAlternative(
               self.springs, len(ds), self.candidates[1:], self.groups[1:]
            ))
        
#            if next_ind + self.groups[1] <= self.candidates[0][1] and 
##                
##            self.children.append(SpringAlternative(
  #              self.springs, ind, self.candidates[1:], self.groups[1:]
  #          ))
  #          if man kan stoppa in en till grupp i candidate... 
  #      inds = [3, 4, 5]

   ##     for ind in inds:
    #        print(self.springs)
    #        print(self.candidates[1:])
    #        print(self.groups[1:])
    #        alt = SpringAlternative(
     #           self.springs, ind, self.candidates[1:], self.groups[1:]
      #      )
      #      self.children.append(alt)
    def print_me(self):
        print(''.join(self.springs))
        for d in self.decided_springs:
            print(''.join(d))
        print(self.candidates)
        print(self.groups)
        print(len(self.children))


#springs = [s for s in '#??.???#.#??????#']
alternatives = SpringAlternative(
    springs, candidates[0][0], candidates, group_sizes
    )
print('============================')
alternatives.print_me()

#alternatives.make_alternatives()
#alternatives.print_me()
##for alt in alternatives.children:
#    alt.print_me()




#def for_group(group_size, unknown, known):

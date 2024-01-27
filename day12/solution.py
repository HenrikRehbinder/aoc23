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
#file = 'input.txt'
task2 = True
with open(file) as file:
    data = [s.strip() for s in file.readlines()]



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
    if task2:
        long_springs = ''
        long_groups = []
        for i in range(5):
            long_springs += springs
            long_groups += groups
        springs = long_springs
        groups = long_groups
    #candidates = find_candidates(springs)
    #print('--------')
    #print(springs)
    #print(candidates)
    #print(len(springs))
    #print(groups)
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



# Ska SpringAlternatives börja med att städa upp . tex eller ska den som skapar SA ha koll på det. 
# Känns renast att SpringAlternatives fixar sånt. Men SpringAlternative får förutsätta att alla
# index är preppade. Den som skapar en SA får ordna det. SpringAlternative förutsätter att första 
# kan vara #. Att grupper måste separeras av . får den som skapar hantera. Det ställer krav på
# att när man initierar SA så har man stegat fram tillräckligt. 
class SpringAlternative:
    def __init__(self, springs, groups, from_level):
        self.springs = springs
        self.decided_springs = [] 
        self.groups = groups
        self.level = from_level + 1
        self.children = []
        self.status = None
        self.test_status()
        #print(f'status: {self.status}')

        if self.status == 'Ok':
            self.make_alternatives()
 #       if self.status == 'Done':
 #           self.decided_springs = ''.join(['.' for i in range(len(self.springs))])
    


    def test_status(self):
        slots = [x for x in self.springs.split('.') if x!='']
        #print(self.springs)
        #print(slots)
        if slots == []:
            max_group_len = 0
        else:
            max_group_len = max([len(s) for s in slots])

        next_cand_length = 0
        found_first = False
        for i, s in enumerate(self.springs):
            if s in '#?':
                if found_first:
                    next_cand_length += 1
                else:
                    found_first = True
                    next_cand_length += 1
            else:
                if found_first:
                    break
                else:
                    pass
        #print(f'next_cand_length: {next_cand_length}')
        if len(self.groups) == 0 and ('#' not in self.springs):
            self.status = 'Done'
            # Här måste man hänga på lite .... om det finns plats kvar. 
        elif len(self.groups) == 0 and ('#' in self.springs):
            self.status = 'Wrong'
        elif len(self.groups) > 0 and max_group_len < self.groups[0]: #(next_cand_length < self.groups[0]):
            self.status = 'Wrong'
        else:
            self.status = 'Ok'

    def is_ok(self, s, g_l, shift):
 #       print(f's: {s}')
        g_l + shift
 #       print(f'g_l: {g_l}')
 #       print(f'shift: {shift}')
        if shift + g_l > len(s):
  #          print('shift too big')
            return -1
        elif '.' not in s[shift:shift+g_l]:
            match = True
   #         print('match')
            not_preceeding = True
            if shift > 0:
                if s[shift-1] == '#':
                    not_preceeding = False
#                    print('preceeding')
 #           else:
#                print('beginning')
            not_trailing = True
            if shift + g_l < len(s):
               if s[shift + g_l] == '#':
                    not_trailing = False
  #                  print('trailing')
        else: 
            match = False
   #         print('no match')

        return match and not_preceeding and not_trailing
        
 
    def make_alternatives(self):
        shift = 0
        #ind = ''.join(['    ' for i in range(self.level-1)])
        #print(ind + f'alternatives for level: {self.level}')
        while shift + self.groups[0] <= len(self.springs):
            #print(ind + '---')
           # print(ind + f'shift: {shift}') 
            if self.is_ok(self.springs, self.groups[0], shift):
                #print(ind + f'shift: {shift} ok')
                d_s = ['.' for i in range(shift)] + ['#' for i in range(self.groups[0])]
                if shift + self.groups[0] < len(self.springs):
                    d_s = d_s + ['.']
                d_s = ''.join(d_s)
    #            print(d_s)
                self.decided_springs.append(d_s)
                #print(ind + '-> child')
                self.children.append(SpringAlternative(self.springs[len(d_s):], self.groups[1:], self.level))
            #else:
                #print(ind + f'shift: {shift} not ok')
            shift += 1
      

    def print_me(self):
        print(''.join(self.springs))
        for d in self.decided_springs:
            print(d)
        print(self.groups)
        print(len(self.children))
    
    
    def concatenate_alternatives(self):
        if len(self.children) == 0:
            alt_list = ['']
            ok_list = [self.status == 'Done']
        else:
            alt_list = []
            ok_list = []
            for d_s, child in zip(self.decided_springs, self.children):
                alts, oks = child.concatenate_alternatives()
                for alt, ok in zip(alts, oks):
                    alt_list.append(d_s + alt)
                    ok_list.append(ok)
        return (alt_list, ok_list) 
    

    def list_ok_alternatives(self):
        alts, oks = self.concatenate_alternatives()
        ok_alts = [alt for alt, ok in zip(alts, oks) if ok]
        return ok_alts


    def print_all(self):
        print('--')
        #print(self.decided_springs)
        #print('--')
        for par, child in zip(self.decided_springs, self.children):
            print(par)
            child.print_all()


print('============================')
tot_alts = 0
for d in data[:4]:
    print('----------------------')
    springs, groups = d.split(' ')
    group_sizes = [int(g) for g in groups.split(',')]
    if task2:
        long_springs = ''
        long_group_sizes = []
        for i in range(5):
            long_springs += springs + '?'
            long_group_sizes += group_sizes 
        springs = long_springs[:-1]
        group_sizes = long_group_sizes

    #print(springs)
    #print(groups)
    print('Record')
    print(springs + str(group_sizes))
    alternatives = SpringAlternative(
        springs, group_sizes, 0
        )
    print('Alternatives')
    ok_alts = alternatives.list_ok_alternatives()
    # Check that alternatives have right group lenghts. 
    
    #group_lengths = [len(x) for x in [alt.split('.') for alt in ok_alts] if x!=[]]
    duplicates = len(set(ok_alts)) != len(ok_alts)
    if duplicates: print('duplicates')
    num_faulty = 0
    for a in ok_alts:
        #print(a)
        group_lengths = [len(g) for g in a.split('.') if g!='']
        faulty_group_lengths = group_lengths != alternatives.groups
        faulty_hash = np.any(np.array([s for s in alternatives.springs])[np.argwhere(np.array([s for s in a])=='#')]=='.')
        faulty_dot = np.any(np.array([s for s in alternatives.springs])[np.argwhere(np.array([s for s in a])=='.')]=='#')
        if faulty_group_lengths:
            gl = ' wrong_group_length'
        else:
            gl = ' '    

        if faulty_hash:
            gh = ' wrong_hash'
        else:
            gh = ' '

        if faulty_dot:
            gd = ' wrong_dot'
        else:
            gd = ' '
        if faulty_group_lengths or faulty_hash or faulty_dot:
            num_faulty +=1
        #if duplicate:
        #    du = ' dup'
        #print(a + gl + gh + gd)
#        if faulty_group_lengths: print(group_lengths)
#        if group_lengths != alternatives.groups:
#            print(a+' wrong_group lenght')
#            print(group_lengths)
 #       else:
 #           print(a+' right group lengths')
        #print(num_faulty)
    print(f'Num alts: {len(ok_alts) - num_faulty}')
    tot_alts += len(ok_alts) - num_faulty

print(f'Ans 1: {tot_alts}')
print('Ans 1: 6958 is correct')

#alternatives.make_alternatives()
#alternatives.print_me()


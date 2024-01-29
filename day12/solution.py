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
 


class SpringAlternative:
    def __init__(self, springs, groups, from_level):
        self.springs = springs
        self.decided_springs = [] 
        self.groups = groups
        self.level = from_level + 1
        self.children = []
        self.status = None
        self.test_status()
 
        if self.status == 'Ok':
            self.make_alternatives()
    
    def test_enough_space(self, springs, groups):
        if self.springs != '':
            #print(self.springs)
            spring_array = np.array([s for s in self.springs])
            #print(spring_array)
            #print(spring_array=='.')
        
            num_non_dots = len(spring_array) - sum(spring_array == '.')
            num_of_hash = sum(self.groups)
            needed_spring_length = sum(self.groups) + len(self.groups) - 1
            if (num_non_dots < num_of_hash) or (needed_spring_length > len(self.springs)):
                enough_space = 'False'
            else:
                enough_space = 'True'
        else:
            enough_space = 'False'
        return enough_space


    def test_status(self):
        '''if self.springs != '':
            #print(self.springs)
            spring_array = np.array([s for s in self.springs])
            #print(spring_array)
            #print(spring_array=='.')
        
            num_non_dots = len(spring_array) - sum(spring_array == '.')
            num_of_hash = sum(self.groups)
            needed_spring_length = sum(self.groups) + len(self.groups) - 1
            if (num_non_dots < num_of_hash) or (needed_spring_length > len(self.springs)):
                enough_space = 'False'
            else:
                enough_space = 'True'
        else:
            enough_space = 'False'
        '''
        enough_space = self.test_enough_space(self.springs, self.groups)

        slots = [x for x in self.springs.split('.') if x!='']
        if slots == []:
            max_group_len = 0
        else:
            max_group_len = max([len(s) for s in slots])

        if len(self.groups) == 0 and ('#' not in self.springs):
            self.status = 'Done'
            # Här måste man hänga på lite .... om det finns plats kvar. 
        elif len(self.groups) == 0 and ('#' in self.springs):
            self.status = 'Wrong'
        elif not(enough_space):
            self.status = 'Wrong'
        elif len(self.groups) > 0 and max_group_len < self.groups[0]: 
            self.status = 'Wrong'
        else:
            self.status = 'Ok'


    def is_ok(self, s, g_l, shift):
        if shift + g_l > len(s):
            return -1
        elif '.' not in s[shift:shift+g_l]:
            match = True
            not_preceeding = True
            if shift > 0:
                if s[shift-1] == '#':
                    not_preceeding = False
            not_trailing = True
            if shift + g_l < len(s):
               if s[shift + g_l] == '#':
                    not_trailing = False
        else:
            match = False

        return match and not_preceeding and not_trailing
        
 
    def make_alternatives(self):
        shift = 0
        while shift + self.groups[0] <= len(self.springs):
            #d_s = ['.' for i in range(shift)] + ['#' for i in range(self.groups[0])]
            if self.is_ok(self.springs, self.groups[0], shift):
                #and self.test_enough_space(self.springs[len(d_s):], self.groups[1:])
                
                d_s = ['.' for i in range(shift)] + ['#' for i in range(self.groups[0])]
                if shift + self.groups[0] < len(self.springs):
                    d_s = d_s + ['.']
                d_s = ''.join(d_s)
                self.decided_springs.append(d_s)
                self.children.append(SpringAlternative(self.springs[len(d_s):], self.groups[1:], self.level))
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
        for par, child in zip(self.decided_springs, self.children):
            print(par)
            child.print_all()


print('============================')
tot_alts = 0
for data_point, d in enumerate(data):
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

    print(f'Record {data_point+1}/{len(data)}')
    print(springs + str(group_sizes))
    alternatives = SpringAlternative(
        springs, group_sizes, 0
        )
    print('Alternatives')
    ok_alts = alternatives.list_ok_alternatives()
    
    duplicates = len(set(ok_alts)) != len(ok_alts)
    if duplicates: print('duplicates')
    num_faulty = 0
    for a in ok_alts:
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
    print(f'Num alts: {len(ok_alts) - num_faulty}')
    tot_alts += len(ok_alts) - num_faulty

print(f'Ans 1: {tot_alts}')
print('Ans 1: 6958 is correct')



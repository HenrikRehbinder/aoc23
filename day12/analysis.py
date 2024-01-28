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
file = 'input.txt'
task2 = True
with open(file) as file:
    data = [s.strip() for s in file.readlines()]


for n, d in enumerate(data):
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
    
    spring_array = np.array([s for s in springs])
    num_of_dots = sum(spring_array == '.')
    num_of_hashes = sum(spring_array == '#')
    spring_len = len(springs)
    groups_len = sum(groups) + len(groups)-1
    num_of_groups = len(groups)
    if num_of_dots == 0:
        print(f'No dots {n}: sl: {spring_len} vs gl: {groups_len} vs n# {num_of_hashes} vs ng {num_of_groups}')


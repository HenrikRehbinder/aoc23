import sys
sys.path.append('..')
from utils.imports import *

FILE = 'input.txt'
patterns = []
with open(FILE) as file:
    data = [s.strip() for s in file.readlines()]

p = []
for d in data:
    if d != '':
        p.append(list(d))
    else:
        patterns.append(np.array(p))
        p = []
patterns.append(np.array(p))


def find_reflection(pattern, task):
    found = False
    _, n_cols = pattern.shape
    for r in range(1, n_cols):
        min_cols = min((n_cols - r, r))
        left = pattern[:,:r]
        right = pattern[:,r:]
        flipped_right = np.fliplr(right)
        left = left[:,-min_cols:]
        flipped_right = flipped_right[:,-min_cols:]
        #print(left)
        #print(flipped_right)
        if task == 1:
            if np.all(left==flipped_right):
                found = True
                break
        if task == 2:
            if sum(sum(left!=flipped_right))==1:
                found = True
                break
    if found:
        return r
    else:
        return 0


ans1 = 0
for i, pattern in enumerate(patterns):
    c = find_reflection(pattern, 1)
    r = find_reflection(pattern.T, 1)
    #print(i, r, c)
    ans1 += c + 100*r

print(f'Ans1: {ans1}')
print('41859 correct')


ans2 = 0
for i, pattern in enumerate(patterns):
    c = find_reflection(pattern, 2)
    r = find_reflection(pattern.T, 2)
    #print(i, r, c)
    ans2+= c + 100*r

print(f'Ans2: {ans2}')
print('30842 correct')

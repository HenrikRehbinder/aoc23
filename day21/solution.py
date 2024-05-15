import sys
sys.path.append('..')
from utils.imports import *
file = 'input.txt'
n_steps = 64

with open(file) as file:
    data = [s.strip() for s in file.readlines()]

map = {'.': 0, '#': 1, 'S': 2}
#garden = np.array(data)
#garden = np.empty((len(data[0]), len(data)), dtype=str)
##for row, d in enumerate(data):
#    for col, tile in enumerate(d):
#        garden[row, col] = tile
garden = []
for d in data:
    garden.append(list(d))


def update_garden(garden):
    n_rows = len(garden)
    n_cols = len(garden[0])
    start_pos = []
    for row in range(n_rows):
        for col in range(n_cols):
            if garden[row][col] == 'O':
                start_pos.append([row, col])
    #print(len(start_pos))
    for r, c in start_pos:
        garden[r][c] = '.'
        for diff in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            new_pos = [r + diff[0], c + diff[1]]
            if 0 <= new_pos[0] < n_rows and 0 <= new_pos[1] < n_cols:
                #print(new_pos)
                if garden[new_pos[0]][new_pos[1]] != '#':
                    garden[new_pos[0]][new_pos[1]] = 'O'
    return garden

if True:
    n_rows = len(garden)
    n_cols = len(garden[0])
    start = []
    for row in range(n_rows):
        for col in range(n_cols):
            if garden[row][col] == 'S':
                garden[row][col] = 'O'
    #start = start[0]
    #garden[start[0]][start[1]] = 'O'
    for i in range(n_steps):
        #print(f'step {i}')
        garden = update_garden(garden)
        #p = garden
        #p[start[0]][start[0]] = 'S'
        #for pp in p: print(pp)
        #for g in garden: print(g)

nO = 0
for g in garden:
    for gg in g:
        if gg == 'O':
            nO += 1

print(f'ans1: {nO}, correct is 3795')

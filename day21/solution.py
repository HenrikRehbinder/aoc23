import sys
sys.path.append('..')
from utils.imports import *
import itertools
from tqdm import tqdm
file = 'input.txt'
n_steps = 64

with open(file) as file:
    data = [s.strip() for s in file.readlines()]

map = {'.': 0, '#': 1, 'S': 2}

garden_basis = []
for d in data:
    garden_basis.append(list(d))


def update_garden(garden):
    n_rows = len(garden)
    n_cols = len(garden[0])
    start_pos = []
    for row in range(n_rows):
        for col in range(n_cols):
            if garden[row][col] == 'O':
                start_pos.append([row, col])
    for r, c in start_pos:
        garden[r][c] = '.'
        for diff in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
            new_pos = [r + diff[0], c + diff[1]]
            if 0 <= new_pos[0] < n_rows and 0 <= new_pos[1] < n_cols:
                if garden[new_pos[0]][new_pos[1]] != '#':
                    garden[new_pos[0]][new_pos[1]] = 'O'
    return garden

n_rows = len(garden_basis)
n_cols = len(garden_basis[0])
start = []
for row in range(n_rows):
    for col in range(n_cols):
        if garden_basis[row][col] == 'S':
            garden_basis[row][col] = 'O'


class Garden():
    def __init__(self, garden_block):
        self.garden_block = garden_block
        self.n_rows = len(garden_block)
        self.n_cols = len(garden_block[0])
        self.start_pos = []
        for row in range(n_rows):
            for col in range(n_cols):
                if self.garden_block[row][col] == 'O':
                    self.start_pos.append([row, col])
                    self.garden_block[row][col] = '.'

    def get_garden(self, row, col):
        return self.garden_block[row % self.n_rows][col % self.n_cols]


    def update(self):
       # new_start_pos = []
        #new_start_pos = [
        #    self.tmpfun(r, c, new_start_pos) for r, c in self.start_pos
        #]
        new_pos = [[r + diff[0], c + diff[1]] for r, c in self.start_pos for diff in [[1, 0], [-1, 0], [0, 1], [0, -1]]]
        #print(new_pos)
        new_pos.sort()
        #print(new_pos)
        new_pos = list(k for k,_ in itertools.groupby(new_pos))
        #if len(new_pos) > 0:
        new_start_pos = [[newp[0], newp[1]] for newp in new_pos if self.get_garden(newp[0], newp[1]) != '#']
        #for newp in new_pos:
        #    if self.get_garden(newp[0], newp[1]) != '#':
        #        new_start_pos.append([newp[0], newp[1]])
        #for r, c in self.start_pos:
        #    for diff in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        #        new_pos = [r + diff[0], c + diff[1]]
        #        if not new_pos in new_start_pos and self.get_garden(new_pos[0], new_pos[1]) != '#':
        #            new_start_pos.append([new_pos[0], new_pos[1]])
        self.start_pos = new_start_pos


garden = Garden(garden_basis)
ext_garden = []
for row in range(-n_rows, 2*n_rows):
    g = []
    for col in range(-n_cols, 2*n_cols):
        #print(row, col)
        g.append(garden.get_garden(row, col))
    ext_garden.append(g)
print('garden_basis')
for g in garden_basis:
    print(''.join(g))

print('ext_garden')
for g in ext_garden:
    print(''.join(g))
n = 26501365
n_steps = 1000
steps = [6, 10, 50, 100, 500, 1000, 5000]
x = []
y = []
x = list(range(n_steps))
def tmp(garden):
    garden.update()
    return len(garden.start_pos)

#y = [tmp(garden) for _ in tqdm(range(n_steps))]
for i in range(n_steps):
    garden.update()
#    if i+1 in steps: print('*')
    print(f'In exactly {i+1} steps, he can reach {len(garden.start_pos)} garden plots.')
    y.append(len(garden.start_pos))

js = [6+j*10 for j in range(len(x)) if 6+j*10<len(x)]
js = [j*2 for j in range(len(x)) if 2*j<len(x)]
jss = [j*2+1 for j in range(len(x)) if 2*j+1<len(x)]

x610 = [x[j] for j in js]
y610 = [y[j] for j in js]
x2 = [x[j] for j in js]
x21 = [x[j] for j in jss]
y2 = [y[j] for j in js]
y21 = [y[j] for j in jss]

plt.figure(clear=True, num='y(x)/y(x-1)')
plt.plot(x2[:-1], [y2[i+1]/y2[i] for i in range(len(y2)-1)])
plt.grid(True)
plt.show()

plt.figure(clear=True, num='y(x)')
plt.plot(x, y)
plt.plot(x2, y2, c='r')
plt.plot(x21, y21, c='g')
plt.grid(True)
plt.show()

plt.figure(clear=True, num='ydiff(x)')
#plt.plot(x[:-1], np.diff(y) )
plt.plot(x2[:-1], np.diff(y2), c='r')
plt.plot(x21[:-1], np.diff(y21), c='g')
plt.grid(True)
plt.show()


#nO = 0
#for g in garden.start_pos:
#    for gg in g:
#        if gg == 'O':
#            nO += 1

#print(f'ans1: {nO}, correct is 3795')

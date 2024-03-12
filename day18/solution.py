import sys
sys.path.append('..')
from utils.imports import *
file = 'test1.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]


directions = {
    'U': np.array((-1, 0)),
    'D': np.array((1, 0)),
    'L': np.array((0, -1)),
    'R': np.array((0, 1))
}
holes = [np.array([0, 0])]
instructions = []
for d in data:
    dire, length, color = d.split(' ')
    instructions.append({'dir': dire, 'length': length, 'color': color})
    for i in range(int(length)):
        holes.append(holes[-1]+directions[dire])

num_rows = max([h[0] for h in holes]) + 1
num_cols = max([h[1] for h in holes]) + 1

chart = np.array([['.' for col in range(num_cols)] for row in range(num_rows)])
for hole in holes:
    chart[hole[0], hole[1]] = '#'

for row in chart:
    print(''.join(row))

# seems right up to here.



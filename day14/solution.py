import sys
sys.path.append('..')
from utils.imports import *
#import matplotlib as mpl
#mpl('qt')
file = 'input.txt'
#file = 'test1.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]

data = np.array([[d for d in dat] for dat in data])

def tilt(data):
    moved_total = []
    n_rows, n_cols = data.shape
    c_len = n_rows
    for column in data.T:
        #print('==================')
        #print(column)
        rounded = np.argwhere(column=='O').squeeze()
        if rounded.shape == ():
            rounded = np.array([rounded])
        cubes = np.argwhere(column=='#').squeeze()
        if cubes.shape == ():
            cubes = np.array([cubes])
        moved = np.array(['.' for i in range(c_len+1)])
        base_pos = 0
        for cube in np.hstack((cubes,[c_len])):
            num_rounded = sum((base_pos <= rounded)*(rounded < cube))
            for i in range(num_rounded):
                moved[i + base_pos] = 'O'
            base_pos = cube+1
            moved[cube] = '#'
        #print(moved[:-1])
        moved_total.append(moved[:-1])       

    moved_total = np.array(moved_total)
    return moved_total.T

moved_total = tilt(data)

ans1 = 0
n_rows, _ = data.shape
for row_num, row in enumerate(moved_total):
    ans1 += (n_rows-row_num)*sum(row=='O')

print(f'Answ1: {ans1}')
print('109661 is correct')


n = 1000000000
n_small = 1000
moved_cycle = data
weights = []
for i in range(n_small):
    moved_north = tilt(moved_cycle)
    moved_west = tilt(moved_north.T).T
    moved_south = np.flipud(tilt(np.flipud(moved_west)))
    moved_cycle = np.flipud(tilt(np.flipud(moved_south.T))).T
    weight = 0
    n_rows, _ = data.shape
    for row_num, row in enumerate(moved_cycle):
        weight += (n_rows-row_num)*sum(row=='O')
    weights.append(weight)

# find period
mw = max(weights[200:])
period = np.diff(np.argwhere(np.array(weights[200:])==mw).squeeze())[-1]
print(period)

num_periods = math.floor(n/period)
offset = n-period*num_periods

index = n-period*math.ceil((n-n_small)/period)-1


print(f'Answ2: {weights[index]}')
print('90176 is correct')

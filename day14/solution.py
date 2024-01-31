import sys
sys.path.append('..')
from utils.imports import *
file = 'input.txt'
#file = 'test1.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]

data = np.array([[d for d in dat] for dat in data])

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

ans1 = 0
for row_num, row in enumerate(moved_total.T):
    ans1 += (n_rows-row_num)*sum(row=='O')

print(f'Answ1: {ans1}')
uppgift 2: Gör om ovantstående till en funktion. Sen ropa på den 4 ggr via 
fliplr och flipud
det kommer nog att visa sig att det hela tar för lång tid men att någon 
cykel återkommer. 
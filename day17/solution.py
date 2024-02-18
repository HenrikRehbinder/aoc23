import sys
sys.path.append('..')
from utils.imports import *
file = 'test1.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]

data_arr = []
for da in data:
    data_arr.append([int(d) for d in da ])



def move(pos, dir):
    return pos + dir


def in_blocks(pos, blocks):
    if pos[0] >= 0 and pos[1] >= 0 and pos[0] < blocks['n_rows'] and pos[1] < blocks['n_cols']:
        return True
    else:
        return False


def turns(dir):
    if dir[0] == 0:
        return [np.array([1, 0]), np.array([-1, 0])]
    else:
        return [np.array([0, 1]), np.array([0, -1])]


def new_states(x, blocks):
    #dirs = np.array([[1, 0], [0, 1],[-1, 0], [0, -1]])
    new = []
    # Start criteria, we know that num_moves=0 here
    if np.all(x['dir'] == np.array([0, 0])):
        for dir in np.array([[1, 0], [0, 1],[-1, 0], [0, -1]]):
            m = move(x['pos'], dir)
            if in_blocks(m, blocks):
                new.append({
                    'pos': m,
                    'dir': dir,
                    'num_moves': x['num_moves']+1
                    })
    else:
        if x['num_moves'] < 3:
            for dir, t in zip([x['dir']] + turns(x['dir']), [False, True, True]):
                #print((dir, x['dir']))
                m = move(x['pos'], dir)
                if t:
                    num_moves = 0
                else:
                    num_moves = x['num_moves'] + 1
                if in_blocks(m, blocks):
                    new.append({
                        'pos': m,
                        'dir': dir,
                        'num_moves': num_moves
                })
        else:
            for dir in turns(x['dir']):
                #print((dir, x['dir']))
                m = move(x['pos'], dir)
                if in_blocks(m, blocks):
                    new.append({
                        'pos': m,
                        'dir': dir,
                        'num_moves': 0
                        })
    return new



def terminated(x, blocks):
    return np.all(x['pos'] == np.array([blocks['n_rows']-1, blocks['n_cols']-1]))


def cost(x, blocks):
    return blocks['cost'][x['pos'][0], x['pos'][1]]


def V_fun(x, blocks, indent):
    #....
    print(indent + 'entering V with ')
    print(f'{indent}{x}')
    if terminated(x, blocks):
        print(f'{indent}terminated, cost {cost(x, blocks)}')
        return cost(x, blocks)
    else:
        
        n_states = new_states(x, blocks) 
        print(f'{indent}num of new_states: {len(n_states)}')
        costs = []
        this_cost = cost(x, blocks)
        i = 0
        for n_state in n_states: 
            print(f'{indent}{(i, n_state)}')
            costs.append(this_cost + V_fun(n_state, blocks, indent+' '))
            i += 1
        print(indent+f'exiting V, cost {min(costs)}')
        return min(costs)

print('SMALLER')
n = 3
data_arr = np.array(data_arr)[:n, :n]
# action a: en förflyttning (alltså en ny pos)
# state x: koordinater, riktning, num_of_moves (antal förflyttningar i en rikting)
tmp = [None for col in range(data_arr.shape[1])]
V = [tmp for row in range(data_arr.shape[0])]
V = np.array(V)
V[-1,-1] = data_arr[-1,-1]

blocks = {
    'cost': data_arr,
    'n_rows': data_arr.shape[0],
    'n_cols': data_arr.shape[1],
    'V': V
}
initial_state = {
    'pos': np.array([0, 0]),
    'dir': np.array([0, 0]),
    'num_moves': 0
}

ans1= V_fun(initial_state, blocks, '') - cost(initial_state, blocks)

#ans1= V(initial_state, blocks)

print(f'Ans1: {ans1}')



if False:
    tests = [
        {'pos':[0,0], 'dir': np.array([0, 0]), 'num_moves': 0},
        {'pos':[0,3], 'dir': np.array([0,1]), 'num_moves': 2},
        {'pos':[0,3], 'dir': np.array([0,1]), 'num_moves': 3},
        {'pos':[0,12], 'dir': np.array([0,1]), 'num_moves': 2},
        {'pos':[0,12], 'dir': np.array([0,1]), 'num_moves': 3},
        {'pos':[12,12], 'dir': np.array([0,1]), 'num_moves': 2},
        {'pos':[12,12], 'dir': np.array([1,0]), 'num_moves': 2}
        ]
    for test in tests:
        print(test)
        print(new_states(test, blocks))
        print('---')

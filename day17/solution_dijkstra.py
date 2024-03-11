import sys

from dijkstar import Graph, find_path


sys.path.append('..')
from utils.imports import *
file = 'input.txt'
test = 2
with open(file) as file:
    data = [s.strip() for s in file.readlines()]
data_arr = []
for da in data:
    data_arr.append([int(d) for d in da])

data_arr = np.array(data_arr)

#print('SMALLER')
#n = 4
#data_arr = data_arr[:n, :n]

#data_arr = np.array([
#    [1, 2, 3],
#    [1, 1, 5],
#    [4, 1, 2]
#    ])
graph = Graph(
)


def move(pos, dir):
    return pos + dir


def in_blocks(pos, blocks):
    if pos[0] >= 0 and pos[1] >= 0 and pos[0] < blocks['n_rows'] and pos[1] < blocks['n_cols']:
        return True
    else:
        return False


def is_final(pos, blocks):
    if pos[0] == blocks['n_rows']-1 and pos[1] == blocks['n_cols']-1:
        return True
    else:
        return False


def turns(dir):
    if dir[0] == 0:
        return [np.array([1, 0]), np.array([-1, 0])]
    else:
        return [np.array([0, 1]), np.array([0, -1])]


def make_new_states(x, blocks):
    if test == 1:
        max_cons_moves = 3
        min_cons_moves = 0
#        moves = [1, 2, 3]
    if test == 2:
        max_cons_moves = 10
        min_cons_moves = 4
 #       moves = [3, 4, 5, 6, 7, 8, 9, 10]
    new = []
    if is_final(x['pos'], blocks):
        pass
    else:
        if np.all(x['dir'] == np.array([0, 0])):
            dirs = np.array([[1, 0], [0, 1]])
            turneds = [False, False]
        elif x['num_moves'] == max_cons_moves:
            dirs = turns(x['dir'])
            turneds = [True, True]
        elif x['num_moves'] < min_cons_moves:
            dirs = [x['dir']]
            turneds = [False]
        else:
            dirs = [x['dir']] + turns(x['dir'])
            turneds = [False, True, True]
        for dir, turned in zip(dirs, turneds):
            m = move(x['pos'], dir)
            if turned:
                num_moves = 1
            else:
                num_moves = x['num_moves'] + 1
            if is_final(m, blocks):
                num_moves = min_cons_moves
                dir = np.array((0, 0))
            if in_blocks(m, blocks):
                new.append({
                    'pos': m,
                    'dir': dir,
                    'num_moves': num_moves
                    })
    return new


def make_key(state):
    d = state['dir']
    if np.all(state['dir'] == [0, 0]):
        d_str='N'
    elif np.all(state['dir']==[1,0]):
        d_str = 'd'
    elif np.all(state['dir']==[-1,0]):
        d_str = 'u'
    elif np.all(state['dir']==[0,-1]):
        d_str = 'l'
    elif np.all(state['dir']==[0,1]):
        d_str = 'r'
    return (
        str(state['pos'][0]) + 
        str(state['pos'][1]) + 
        d_str + 
        str(state['num_moves'])
        )
    

def cost(x, blocks):
    return blocks['cost'][x['pos'][0], x['pos'][1]]


def node_from_state(state):
    return (state['pos'][0], state['pos'][1], state['dir'][0], state['dir'][1], state['num_moves'])


blocks = {
    'cost': data_arr,
    'n_rows': data_arr.shape[0],
    'n_cols': data_arr.shape[1],
}

n_rows = blocks['n_rows']
n_cols = blocks['n_cols']

initial_state = {
    'pos': np.array([0, 0]),
    'dir': np.array([0, 0]),
    'num_moves': 0
    }
end_state = {
    'pos': np.array([n_rows-1, n_cols-1]),
    'dir': np.array([0, 0]),
    'num_moves': 4
}

if test == 1:
    moves = [1, 2, 3]
if test == 2:
    moves = [3, 4, 5, 6, 7, 8, 9, 10]


for new_state in make_new_states(initial_state, blocks):
    graph.add_edge(node_from_state(initial_state), node_from_state(new_state), cost(initial_state, blocks))

for row in range(blocks['n_rows']):
    for col in range(blocks['n_cols']):
        if row == 0 and col == 0:
            pass
        elif row == blocks['n_rows']-1 and col == blocks['n_cols']-1:
            pass
        else:
            dirs = [np.array([-1, 0]), np.array([1, 0]), np.array([0, -1]), np.array([0, 1])]
            max_num_moves = moves[-1]
            for dir in dirs:
                for n in range(max_num_moves):
                    num_moves = n+1
                #for num_moves in moves:
                    state = {'pos': (row, col), 'dir': dir, 'num_moves': num_moves}
#                    print('----')
#                    print(state)
#                    print(node_from_state(state))
                    new_states = make_new_states(state, blocks)
                    for new_state in new_states:
 #                       print(new_state)
 #                       print(node_from_state(new_state))
                        graph.add_edge(node_from_state(state), node_from_state(new_state), cost(state, blocks))

for key, val in graph.items():
    if key[0] == 0 and key[1] == 0:
        print('---')
        print(key)
        print(val)


path = find_path(graph, node_from_state(initial_state), node_from_state(end_state))

display = False
if display:
    display_path = data_arr.astype('str')
    for node in path.nodes:
        dir = str(node[2])+str(node[3])
        if dir == '-10': d = '^'
        elif dir == '10': d = 'v'
        elif dir == '01': d = '>'
        elif dir == '0-1': d = '<'
        else: d = '*'
        display_path[node[0], node[1]] = d
    for row in display_path:
        print(''.join(row))

print(f'Ans: {path.total_cost + cost(end_state, blocks)-cost(initial_state, blocks)} Correct 1: 936')




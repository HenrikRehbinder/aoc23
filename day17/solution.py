import sys
sys.path.append('..')
from utils.imports import *
file = 'test1.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]

data_arr = []
for da in data:
    data_arr.append([int(d) for d in da ])

data_arr = np.array(data_arr)
#print('SMALLER')
#n = 4
#data_arr = data_arr[:n, :n]
if False:
    data_arr = np.array([
        [1, 2, 3],
        [1, 1, 5],
        [4, 1, 2]
        ])


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


def make_new_states(x, blocks):
    new = []
#    if np.all(x['dir'] == np.array([0, 0])):
#        dirs = np.array([[1, 0], [0, 1],[-1, 0], [0, -1]])
#        turneds = [False, False, False, False] #Need to update 
    if x['num_moves'] == 3:
        dirs = turns(x['dir'])
        turneds = [True, True]
    else:
        dirs = [x['dir']] + turns(x['dir'])
        turneds = [False, True, True]
    for dir, turned in zip(dirs, turneds):
        m = move(x['pos'], dir)
        if turned:
            num_moves = 0
        else:
            num_moves = x['num_moves'] + 1
        if in_blocks(m, blocks):
            new.append({
                'pos': m,
                'dir': dir,
                'num_moves': num_moves
                })
    return new


def terminated(x, blocks):
    print(x['pos'][0])
    print(x['pos'][1])
    return V[x['pos'][0], x['pos'][1]] is not None


def make_key(state):
    d = state['dir']
    if np.all(state['dir']==[0,0]):
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


def V_fun_old(x, blocks, indent):
    #....
    print(indent + 'entering V with ')
    print(f'{indent}{x}')
    if terminated(x, blocks):
        print(f'{indent}terminated, cost {cost(x, blocks)}')
        return V[x['pos'][0], x['pos'][1]]
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
        V[x['pos'][0], x['pos'][1]] = min(costs)
        return min(costs)

'''
def V_fun(x, blocks, indent, V_bound, acc_cost, start_state):
    #....
    n_states = new_states(x, blocks) 
    #print(f'{indent}num of new_states: {len(n_states)}')
    this_cost = cost(x, blocks)
    i = 0
    for n_state in n_states: 
     #   print(f'{indent}{(i, n_state)}')
        if terminated(n_state, blocks):
            new_acc_cost = acc_cost + V[n_state['pos'][0], n_state['pos'][1]]
            #if new_acc_cost < V_bound:
            V[start_state['pos'][0], start_state['pos'][1]] = min(
                V[start_state['pos'][0], start_state['pos'][1]], new_acc_cost
            )
        else:
            new_acc_cost = acc_cost + cost(n_state, blocks)
            if new_acc_cost >= V[start_state['pos'][0], start_state['pos'][1]]:
                pass
            else:
                V_fun(n_state, blocks, indent+' ', 
                      V_bound, new_acc_cost, start_state)
'''


def V_fun(x, blocks, indent, V_bound, acc_cost, start_state):
    x_key = make_key(x)
    print(f'{indent}at {x_key}, v_bound {V_bound}')
    try:
        V_val = V[x_key]
        print(f'{indent}Using V table at {x_key} with val {V_val}')
        #return V_val
    except: # pylint: disable=bare-except
        c = cost(x, blocks)
        print(f'{indent}c: {c}')

        if c >= V_bound:
            print(f'{indent}c:{c} >= V_bound:{V_bound}->return:{V_bound+c+1}')
            V_val = V_bound+c+1
        else:
            new_states = make_new_states(x, blocks) 
            print(f'{indent}Evaluating new states at {make_key(x)}: {[make_key(ns) for ns in new_states]}')
              
            V_vals = []
            best_V = V_bound
            for new_state in new_states: 
                print(f'{indent}{make_key(new_state)}')
                # Här måste jag väl uppdatera best_V ? 
                # Jag skickar ibland in best_V-c = 0, så det är något fel.
                # Jag tror inte jag tänker rätt här
                # print(f'{indent}c {c} before V call')
                V_new_state = V_fun(
                    new_state, blocks, indent + '--', best_V-c, acc_cost, start_state
                    )
                print(f'{indent}Vns {V_new_state}')
                #print(f'{indent}c {c} after V call')

                print(f'{indent}settled c+V {c+V_new_state} at {make_key(x)} from {make_key(new_state)}')
                best_V = min((best_V, c + V_new_state))
                #V_vals.append(V_new_state)
            #print(f'V_vals {}')
            V_val = best_V
            print(f'{indent}writing V at {x_key} with val {V_val} based on minimization')
            V[x_key] = V_val
    return V_val


def print_V_at_pos(pos_str):
    for key, val in V.items():
        if key[:2] == pos_str:
            print((key, val))

blocks = {
    'cost': data_arr,
    'n_rows': data_arr.shape[0],
    'n_cols': data_arr.shape[1],
}
# action a: en förflyttning (alltså en ny pos)
# state x: koordinater, riktning, num_of_moves (antal förflyttningar i en rikting)
V_b = sum(sum(blocks['cost']))
#tmp = [None for col in range(data_arr.shape[1])]

dummy_end = {
    'pos': [blocks['n_rows']-1, blocks['n_cols']-1],
    'dir': np.array((1,0)),
    'num_moves': 0
}

end_cost = cost(dummy_end, blocks)
#V = {
  #  make_key(dummy_end): end_cost 
  #  }
V={}
for dir in [np.array([1, 0]), np.array([0, 1])]:#,np.array([-1, 0]),np.array([0, -1])]:
    for num_moves in [0, 1, 2, 3]:
        V[make_key({
            'pos': [blocks['n_rows']-1, blocks['n_cols']-1],
            'dir': dir,
            'num_moves': num_moves
        })] = end_cost

#tmp = [V_b for col in range(data_arr.shape[1])]
#V = [tmp for row in range(data_arr.shape[0])]
#V = np.array(V)
#V[-1, -1] = data_arr[-1,-1]
print('Initial V')
print(V)
#V[2, 1] = 5
#V[1, 2] = 6
#V[1, 1] = 7
n_rows = blocks['n_rows']
#for rc, l in zip(reversed(range(blocks['n_rows']-1)), range(2, blocks['n_rows']+1)):'
initial_state_d = {
    'pos': np.array([0, 0]),
    'dir': np.array([1, 0]),
    'num_moves': 0
    }
initial_state_r = {
    'pos': np.array([0, 0]),
    'dir': np.array([0, 1]),
    'num_moves': 0
    }
print(' ')
print('down')
ans1_d = V_fun(initial_state_d, blocks, '', V_b, cost(initial_state_d, blocks), initial_state_d)
print(ans1_d)
for key, val in V.items():
    print((key, val))
print_V_at_pos('00')


print(' ')
print('right')
ans1_r = V_fun(initial_state_r, blocks, '', V_b, cost(initial_state_r, blocks), initial_state_r)
print(ans1_r)
for key, val in V.items():
    print((key, val))
print('V at pos 00')    
print_V_at_pos('00')


#print('skunt, var kommer 00l0 ifrån? den ska ju inte ge något V')
V={}
for dir in [np.array([1, 0]), np.array([0, 1])]:#,np.array([-1, 0]),np.array([0, -1])]:
    for num_moves in [0, 1, 2, 3]:
        V[make_key({
            'pos': [blocks['n_rows']-1, blocks['n_cols']-1],
            'dir': dir,
            'num_moves': num_moves
        })] = end_cost

for rc in reversed(range(n_rows-1)):
    print(f'rc: {rc}')

    #print(f'l: {l}')   
    for j in range(rc+1, n_rows):
        print(f'j:{j}')
        print((rc,j))
        for num in [0, 1,2, 3]:
            initial_state = {
                'pos': np.array([rc, j]),
                'dir': np.array([0, 0]),
                'num_moves': num
                }
        #    print(initial_state['pos'])
            V_fun(initial_state, blocks, '', V_b, cost(initial_state, blocks), initial_state)
        #print(V)
        #print((j,rc))
            initial_state = {
                'pos': np.array([j, rc]),
                'dir': np.array([0, 0]),
                'num_moves': num
                }
#            print(initial_state['pos'])
            V_fun(initial_state, blocks, '', V_b, cost(initial_state, blocks), initial_state)
 #           print(V)
    print((rc,rc))
    initial_state = {
       'pos': np.array([rc, rc]),
        'dir': np.array([0, 0]),
        'num_moves': 0
        }
    print(initial_state['pos'])
    V_fun(initial_state, blocks, '', V_b, cost(initial_state, blocks), initial_state)
    print(V)

#ans1= V(initial_state, blocks)
print(V)
print(blocks['cost'])
#print(f'Ans1: {ans1}')
initial_state = {
    'pos': np.array([2, 2]),
    'dir': np.array([0, 0]),
    'num_moves': 0
    }
# print('Fan. Dels är svaret för högt. Dels så har jag missat något fundamentalt. Jag kan inte bara landa i en evakluerad V eftersom jag måste ta hänsyn till att jag kanske redan kört för långt i samma rikting. ')
# print('Om optimal path från en V börjar med tex tre raka så måste jag svänga in i den')


# if False:
#     tests = [
#         {'pos':[0,0], 'dir': np.array([0, 0]), 'num_moves': 0},
#         {'pos':[0,3], 'dir': np.array([0,1]), 'num_moves': 2},
#         {'pos':[0,3], 'dir': np.array([0,1]), 'num_moves': 3},
#         {'pos':[0,12], 'dir': np.array([0,1]), 'num_moves': 2},
#         {'pos':[0,12], 'dir': np.array([0,1]), 'num_moves': 3},
#         {'pos':[12,12], 'dir': np.array([0,1]), 'num_moves': 2},
#         {'pos':[12,12], 'dir': np.array([1,0]), 'num_moves': 2}
#         ]
#     for test in tests:
#         print(test)
#         print(new_states(test, blocks))
#         print('---')


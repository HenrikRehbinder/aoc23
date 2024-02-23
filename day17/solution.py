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
        #print('*')
        for dir in np.array([[1, 0], [0, 1],[-1, 0], [0, -1]]):
            m = move(x['pos'], dir)
        #    print(m)
            if in_blocks(m, blocks):
         #       print('***')
                new.append({
                    'pos': m,
                    'dir': dir,
                    'num_moves': x['num_moves']+1
                    })
    else:
        #print('**')
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
    return V[x['pos'][0], x['pos'][1]] is not None
    #return np.all(x['pos'] == np.array([blocks['n_rows']-1, blocks['n_cols']-1]))


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

# Börja med rad/kolonn närmast slutet 
# Ta ett steg i varje riktning och håll inkrementera kostnaden. När en av dem terminerar
    # har vi en max(V(state))kan vi stänga ner de andra om de får en kostnad högre 
    
# Jag kan inte bygga upp det nerifrån höger (eftersom det kan finnas bättre lösningar när problemet blir större)
# En idé är att hålla koll på ackumulerad kostnad när man traverserar.
# Det här ska ju bara vara att göra - vad gör jag för fel?!
# Det är ju out of the box dynp. Det måste vara fel i V_fun 
print('SMALLER')
n = 8
data_arr = np.array(data_arr)[:n, :n]
blocks = {
    'cost': data_arr,
    'n_rows': data_arr.shape[0],
    'n_cols': data_arr.shape[1],
}
# action a: en förflyttning (alltså en ny pos)
# state x: koordinater, riktning, num_of_moves (antal förflyttningar i en rikting)
V_b = sum(sum(blocks['cost']))
#tmp = [None for col in range(data_arr.shape[1])]
tmp = [V_b for col in range(data_arr.shape[1])]
V = [tmp for row in range(data_arr.shape[0])]
V = np.array(V)
V[-1, -1] = data_arr[-1,-1]
print('Initial V')
print(V)
#V[2, 1] = 5
#V[1, 2] = 6
#V[1, 1] = 7
n_rows = blocks['n_rows']
#for rc, l in zip(reversed(range(blocks['n_rows']-1)), range(2, blocks['n_rows']+1)):
   
for rc in reversed(range(n_rows-1)):
    print(f'rc: {rc}')

    #print(f'l: {l}')   
    for j in range(rc+1, n_rows):
        print(f'j:{j}')
        print((rc,j))
        initial_state = {
            'pos': np.array([rc, j]),
            'dir': np.array([0, 0]),
            'num_moves': 0
            }
        print(initial_state['pos'])
        V_fun(initial_state, blocks, '', None, cost(initial_state, blocks), initial_state)
        print(V)
        print((j,rc))
        initial_state = {
            'pos': np.array([j, rc]),
            'dir': np.array([0, 0]),
            'num_moves': 0
            }
        print(initial_state['pos'])
        V_fun(initial_state, blocks, '', None, cost(initial_state, blocks), initial_state)
        print(V)
    print((rc,rc))
    initial_state = {
       'pos': np.array([rc, rc]),
        'dir': np.array([0, 0]),
        'num_moves': 0
        }
    print(initial_state['pos'])
    V_fun(initial_state, blocks, '', None, cost(initial_state, blocks), initial_state)
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
print('Fan. Dels är svaret för högt. Dels så har jag missat något fundamentalt. Jag kan inte bara landa i en evakluerad V eftersom jag måste ta hänsyn till att jag kanske redan kört för långt i samma rikting. ')
print('Om optimal path från en V börjar med tex tre raka så måste jag svänga in i den')


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

from utils.imports import *
file = 'input.txt'
file = 'test2.txt'
file = 'test3.txt'
file = 'input.txt'

with open(file) as file:
    pipe_map = [s.strip() for s in file.readlines()]

for i, d in enumerate(pipe_map):
    j = d.find('S')
    if j != -1:
        B = (i, j)
        break

pipe_map[i] = pipe_map[i][:j]+'B'+pipe_map[i][j+1:]


"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
"""

pipe_dirs = {
    '|': 'NS',
    '-': 'EW',
    'L': 'NE',
    'J': 'NW',
    '7': 'SW',
    'F': 'SE',
    '.': 'xx'
}

dist_map = -np.ones((len(pipe_map), len(pipe_map[0])))

dist_map[B] = 0


steps = {
    'N': np.array((-1, 0)),
    'E': np.array((0, 1)),
    'S': np.array((1, 0)),
    'W': np.array((0, -1))
}


def reverse(pipedir):
    reversing = {
        'W': 'E',
        'E': 'W',
        'N': 'S',
        'S': 'N',
        'x': 'x'
    }
    return reversing[pipedir[0]]+reversing[pipedir[1]]


def transfer(pipe_dir, direction):
    i = reverse(pipe_dir).find(direction)
    if i != -1:
        valid = True
        direction = pipe_dir[1-i]
    else:
        valid = False
        direction = None
    return valid, direction


def take_step(direction, pos, pipe_map, dist_map):
    dist = dist_map[pos]
    (nrow, ncol) = steps[direction] + pos
    if nrow < 0 or nrow > dist_map.shape[0]-1 or ncol < 0 or ncol > dist_map.shape[1]-1:
        return -1, None
    else:
        pipe = pipe_map[nrow][ncol]
        if pipe == 'B':
            return -2, None
        else:
            valid, direction = transfer(pipe_dirs[pipe], direction)
            if valid:
                dist += 1
                if dist_map[nrow, ncol] == -1 or dist_map[nrow, ncol] > dist:
                    dist_map[nrow, ncol] = dist
                return (nrow, ncol), direction
            else:
                return -1, None

#        dist_map[nrow, ncol] = max(dist_map[nrow, ncol], )


#s = take_step("E", S, pipe_map, dist_map)
directions = 'NESW'
real_directions = []
for direction in directions:
    x = dist_map
    pos, _ = take_step(direction, B, pipe_map, x)
    if pos != -1:
        real_directions.append(direction)

#print(real_directions)
pos = B
poss = [pos]
direction = real_directions[0]
directions = [direction]
while pos != -2:
    pos, direction = take_step(direction, pos, pipe_map, dist_map)
    #print(direction)
    directions.append(direction)
    poss.append(pos)
    #print(dist_map)

#print(f'Ans 1: {math.ceil(max(dist_map[dist_map > -1])/2)}')
print(f'Ans 1: {(len(directions)-1)/2}')


def print_pipes(pipe_map):
    for pm in pipe_map:
        print(pm)

# print_pipes(pipe_map)

# 'Ide: Man gör en 2d-array som representerar delen mellan pipes. Den kan vara öppen eller stängd.' 
#      Det blir nog en graf och kanske ska man testa ett grafbibliotek\\
#          https://networkx.org/documentation/stable/tutorial.html kanske. Borde finnas en kortaste-vägensökning i den. \\
##            (för 1an) Kanske nån sorts subgraf kan användas. Det verkar ju troligt att Pipes blir länkar mellan tiles eller så.
#            ')
print('1')
poss[-1] = poss[0]

#loop_rows, loop_cols = np.where(dist_map > -1)
#loop_nodes = [(r, c) for r, c in zip(loop_rows, loop_cols)]
loop_nodes = poss[:-1]

encl_cand = np.where(dist_map == -1)
encl_cand = [[r, c] for r, c in zip(encl_cand[0], encl_cand[1])]
# TODO: Jag antar här att kanten är kandidat. Så behöver det inte vara.
print(f'map size {dist_map.shape}')
print('2')
#input('press')
def grow(node, loop_nodes, n_rows, n_cols):
    edge_patch = False
    patch = [np.array(node)]
    ended = False
    dirs = np.array(((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)))
    i = 0
    while not ended:
        #print(f'grow_step: {i}')
        #print(f'patch size: {len(patch)}')
        j = len(patch)
        for dir in dirs:
            test_node = patch[i] + dir
            if (
                    test_node[0] >= 0 and test_node[0] < n_rows and test_node[1] >= 0 and test_node[1] < n_cols
                    and not np.any(np.all(test_node == loop_nodes, axis=1))
                    and not np.any(np.all(test_node == patch[:j], axis=1))
            ):
                patch = np.vstack((patch, test_node))
                if not edge_patch:
                    if test_node[0] == 0 or test_node[0] == n_rows-1 or test_node[1] == 0 or test_node[1] == n_cols-1:
                        edge_patch = True

        if i == len(patch)-1:
            ended = True
        i = i + 1
#        print('*')
#        print(i)
#        print(len(patch))
        #if i == 20:
        #    break
    return [(p[0],p[1]) for p in patch], edge_patch

print('3')

n_rows, n_cols = dist_map.shape
# Add nodes to grid. Extend outside, and then between
#  012            012345
# 0qwe           0.......
# 1asd  goes to  1.q.w.e.
#                2.......
# 2zxc           3.a.s.d.
#                4.......
#                5.z.x.c.
#               .......
# 0->1,  1->3
# nrows, ncols -> nrows*2+1, ncols*2+1
# loop_nodes. Index transforms with i->i*2+1. Add one between
# (i,j),(i,j+1) -> (2i+1, 2j+1),(2i+1,2j+2),(2i+1,2j+2)
# then grow the outer rim
# Need to know original candidates.


def new_ind(i):
    return 2 * i + 1


def extend_loop_nodes(loop_nodes):
    ln = loop_nodes[0]
    ext_loop_nodes = [
        (new_ind(ln[0]), new_ind(ln[1]))
    ]
    for ln in loop_nodes[1:]+[loop_nodes[0]]:
        last_node = ext_loop_nodes[-1]
        next_next_node = (new_ind(ln[0]), new_ind(ln[1]))
        if next_next_node[0] == last_node[0]:
            if last_node[1] < next_next_node[1]:
                d = 1
            else:
                d = -1
            intermediate_node = (last_node[0], last_node[1]+d)
        else:
            if last_node[0] < next_next_node[0]:
                d = 1
            else:
                d = -1
            intermediate_node = (last_node[0]+d, last_node[1])
        ext_loop_nodes.append(intermediate_node)
        #print(intermediate_node)
        ext_loop_nodes.append(next_next_node)
    ext_loop_nodes = ext_loop_nodes[:-1]
    return ext_loop_nodes

#print(loop_nodes)
#print('ext')
ext_loop_nodes = extend_loop_nodes(loop_nodes)
#print(ext_loop_nodes)

def encl_candidates_original(dist_map):
    indices = np.argwhere(dist_map == -1)
    mapped_ind = []
    for ind in indices:
        mapped_ind.append((new_ind(ind[0]), new_ind(ind[1])))
    return mapped_ind

encl_cand_old_grid = encl_cand
encl_cand_original = encl_candidates_original(dist_map)
encl_cand = []
pipe_disp = []
for row in range(2*n_rows+1):
    pd = []
    for col in range(2*n_cols+1):
        if not (row, col) in ext_loop_nodes:
            encl_cand.append((row, col))
            pd.append('o')
        else:
            pd.append('*')
    pipe_disp.append(''.join(pd))

#[print(pd) for pd in pipe_disp]



#-----------
#if False:
patches = []
edge_patches = []
rem_cand = encl_cand   #Här är felet. Måste utöka, eller ev bara loopa över kanten (smart)
i = 0
while len(rem_cand) > 0:

    patch, edge_patch = grow(rem_cand[0], ext_loop_nodes, n_rows*2+1, n_cols*2+1)
    patches.append(patch)
    edge_patches.append(edge_patch)
    old_cand = rem_cand
    rem_cand = []
    for enc in old_cand:
        if not np.any(np.all(np.array(enc) == patch, axis=1)):
            rem_cand.append(enc)
    i = i + 1

print('4')

print((n_rows*2+1)*(n_cols*2+1))
n = 0
for patch in patches:
    n += len(patch)
n += len(ext_loop_nodes)
print(n)

ill_map = {}
for ln in ext_loop_nodes:
    ill_map[ln] = 'x'
for patch, edge_patch in zip(patches, edge_patches):
    if edge_patch:
        m = 'O'
    else:
        m = 'I'
    for p in patch:
        ill_map[p] = m


illu = []
for row in range(n_rows*2+1):
    ill = []
    for col in range(n_cols*2+1):
        ill.append(ill_map[(row, col)])
    illu.append(''.join(ill))
#for ill in illu:
    #print(ill)

# hitta alla index för encl_cand_original som också finns i edge patches.
# dessa index kan man sen gå in i encl_cand_org_grid
# räcker med att räkna index
total_inner = []
for patch, edge_patch in zip(patches, edge_patches):
    if not edge_patch:
        total_inner += patch

inner = 0
for p in encl_cand_original:
    if ((np.array(p) == np.array(total_inner)).sum(axis=1) == 2).any():
        inner += 1

print(f'inner: {inner}')

'''
def remove_patch_encl(patch, encl):
    for p in patch:
        i = np.argwhere(((np.array(encl) == p).sum(axis=1) == 2))
        if i.shape[0] == 1:
            encl.pop(i[0][0])
    return encl



encl = encl_cand
for patch, edge_patch in zip(patches, edge_patches):
    if edge_patch:
        encl = remove_patch_encl(patch, encl)
    #print(encl)

#######################
patch_vis = np.ones((2*n_rows+1, 2*n_cols+1))
for p in patch:
    patch_vis[p[0], p[1]] = 0
print(patch_vis)


pipe_disp = []
for p in pipe_map:
    pipe_disp.append((''.join(p)).replace('.', 'x'))
#[print(p) for p in pipe_disp]

pipe_list = []
for p in pipe_disp:
    pipe_list.append([pp for pp in p])
for patch, edge in zip(patches, edge_patches):
    if edge:
        s = '0'
    else:
        s = 'I'
    for p in patch:
        pipe_list[p[0]][p[1]] = s

pipe_disp = []
for p in pipe_list:
    pipe_disp.append((''.join(p)))
[print(p) for p in pipe_disp]
'''


'''
tot_contained = 0
for j in [i for i, ep in enumerate(edge_patches) if ep == False]:
    print(j)
    tot_contained += len(patches[j]) #len(np.unique(patches[j], axis=0))

#path_starters = [ec for encl_cand if (ec[0]==0 or ec[-1]==n_rows)
# grow path
def crosses_loop(c1, c2, loop_nodes):
    c1_ind = np.where(np.sum(c1 == loop_nodes, axis=1) == 2)[0][0]
    c2_ind = np.where(np.sum(c2 == loop_nodes, axis=1) == 2)[0][0]
    return abs(c1_ind-c2_ind)==1



p = [0, 0]


dirs = np.array(((1, 0), (0, 1), (0, -1), (-1, 0),))

edge_patch = False
path = [np.array(p)]
ended = False
i = 0
while not ended:
    print(f'grow_step: {i}')
    print(f'patch size: {len(patch)}')
    j = len(path)
    for dir in dirs:
        test_node = path[i] + dir
        inside = test_node[0] >= 0 and test_node[0] < n_rows-1 and test_node[1] >= 0 and test_node[1] < n_cols-1
        allready_found = np.any(np.all(test_node == patch[:j], axis=1))
        if dir[0] == 0:
            c1 = path[i] + np.array([1, 0])
            c2 = path[i] + np.array([0, 1])
        else:
            c1 = path[i] + np.array([0, 1])
            c2 = path[i] + np.array([1, 0])
        cross = crosses_loop(c1, c2, loop_nodes)
        if inside and not allready_found and not cross:

            patch = np.vstack((patch, test_node))
                if not edge_patch:
                    if test_node[0] == 0 or test_node[0] == n_rows - 1 or test_node[1] == 0 or test_node[
                        1] == n_cols - 1:
                        edge_patch = True

        if i == len(patch) - 1:

print(f'Answ2: {tot_contained}')



  0 1 2 3 4 5 
  . . . . . .           
   o   o
0 . F - - - -         
     o o
1 .oIo. .             

2 . I . .               

3
4
5
'''


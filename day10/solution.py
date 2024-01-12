from utils.imports import *
import itertools as iter
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

poss[-1] = poss[0]

loop_nodes = poss[:-1]

encl_cand = np.where(dist_map == -1)
encl_cand = [[r, c] for r, c in zip(encl_cand[0], encl_cand[1])]
# TODO: Jag antar här att kanten är kandidat. Så behöver det inte vara.
print(f'map size {dist_map.shape}')
print('2')
#input('press')

def grow2(rem_cand, map, n_rows, n_cols):
    #edge_patch = False
    ended = False
    #dirs = np.array(((1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)))
    dirs = np.array(((1, 0), (0, 1), (0, -1), (-1, 0)))
    i = 0
    patch = [rem_cand[0]]
    map[rem_cand[0]] = '0'
    while not ended:
        #print(f'grow_step: {i}')
        #print(f'patch size: {len(patch)}')
        #j = len(patch)
        for dir in dirs:
            test_node = (patch[i][0] + dir[0], patch[i][1] + dir[1])
            if (
                    test_node[0] >= 0 and test_node[0] < n_rows and test_node[1] >= 0 and test_node[1] < n_cols
                    and not map[test_node] in 'xpOI'
                    #and not map[test_node] == 'p'
            ):
                patch = patch+[test_node]
                map[test_node] = 'O'
                #if not edge_patch:
                #    if test_node[0] == 0 or test_node[0] == n_rows-1 or test_node[1] == 0 or test_node[1] == n_cols-1:
                #        edge_patch = True

        if i == len(patch)-1:
            ended = True
        i = i + 1
#        print('*')
#        print(i)
#        print(len(patch))
        #if i == 20:
        #    break
    return patch, map

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
print('extending loop_nodes')
ext_loop_nodes = extend_loop_nodes(loop_nodes)
#print(ext_loop_nodes)

def encl_candidates_original(dist_map):
    indices = np.argwhere(dist_map == -1)
    mapped_ind = []
    for ind in indices:
        mapped_ind.append((new_ind(ind[0]), new_ind(ind[1])))
    return mapped_ind

#encl_cand_old_grid = encl_cand
#print('mapping encl_cand')
encl_cand_original = encl_candidates_original(dist_map)


map = {}
for row in range(2*n_rows+1):
    for col in range(2*n_cols+1):
        map[(row, col)] = '.'

for p in ext_loop_nodes:
    map[p] = 'x'

rem_cand = []
for r in [0, 2*n_rows]:
    for c in range(2*n_cols+1):
        rem_cand.append((r, c))
for c in [0, 2*n_cols]:
    for r in range(1, 2*n_rows+1):
        rem_cand.append((r, c))

ended = False
while not ended:
    patch, map = grow2(rem_cand, map, n_rows*2+1, n_cols*2+1)
    rem_cand_new = []
    for i, rc in enumerate(rem_cand):
        if map[rc] == '.':
            rem_cand_new.append(rc)
    rem_cand = rem_cand_new
    if len(rem_cand) == 0:
        ended = True

inner = 0
for p in encl_cand_original:
    if map[p] == '.':
        inner += 1

print(f'inner: {inner} 453 is the right answer')

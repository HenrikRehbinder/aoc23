from utils.imports import *
file = 'input.txt'
file = 'test1.txt'

with open(file) as file:
    pipe_map = [s.strip() for s in file.readlines()]

for i, d in enumerate(pipe_map):
    j = d.find('S')
    if j != -1:
        S = (i, j)


"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
pipes = {
    '|': {'from': (0, 1), 'to': (0, -1)},
    '-': {'from': (1, 0), 'to': (-1, 0)},
    'L': {'from': (, ), 'to': (, )},
    '': {'from': (,), 'to': (,)},
    '': {'from': (,), 'to': (,)},
    '': {'from': (,), 'to': (,)},
}
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
dist_map = np.empty((len(pipe_map), len(pipe_map[0])))

dist_map[S] = 0


steps = {
    'N': np.array((1, 0)),
    'E': np.array((0, 1)),
    'S': np.array((-1, 0)),
    'W': np.array((0, -1))
}
def take_step(direction, pos, pipe_map, dist_map):
    dist = dist_map[pos]
    (nrow, ncol) = steps[direction] + pos
    pipe = pipe_map[nrow][ncol]
    if direction in pipe_dirs[pipe]:  Här ska man kolla båda riktningarna. E matchar EW
    Det kanske är bra att använda (0,1), då kan man byta tecken och jämföra båda. Kanske
    med nåt abs eller parallelkoll.
        return (nrow, ncol)
    else:
        return -1

#        dist_map[nrow, ncol] = max(dist_map[nrow, ncol], )


def print_pipes(pipe_map):
    for pm in pipe_map:
        print(pm)

print_pipes(pipe_map)

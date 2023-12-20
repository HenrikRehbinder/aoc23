from utils.imports import *
file = 'input.txt'
#file = 'test1.txt'

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

print(real_directions)
pos = B
direction = real_directions[0]
directions = [direction]
while pos != -2:
    pos, direction = take_step(direction, pos, pipe_map, dist_map)
    print(direction)
    directions.append(direction)
    #print(dist_map)

#print(f'Ans 1: {math.ceil(max(dist_map[dist_map > -1])/2)}')
print(f'Ans 1: {(len(directions)-1)/2}')


def print_pipes(pipe_map):
    for pm in pipe_map:
        print(pm)

#print_pipes(pipe_map)

# 'Ide: Man gör en 2d-array som representerar delen mellan pipes. Den kan vara öppen eller stängd.' 
#      Det blir nog en graf och kanske ska man testa ett grafbibliotek\\
#          https://networkx.org/documentation/stable/tutorial.html kanske. Borde finnas en kortaste-vägensökning i den. \\
##            (för 1an) Kanske nån sorts subgraf kan användas. Det verkar ju troligt att Pipes blir länkar mellan tiles eller så.
#            ')
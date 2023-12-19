from utils.imports import *
file = 'test1.txt'
file = 'input.txt'

with open(file) as file:
    data = [s.strip() for s in file.readlines()]
seeds = [int(s) for s in data[0].split(': ')[1].split(' ')]

maps = []
vals = False
for d in data[2:]:
    if 'map' in d:
        map = {}
        tmp = d.split(' ')[0].split('-')
        map['to'] = tmp[2]
        map['from'] = tmp[0]
        #vals = True
        map['vals'] = []
    elif d == '':
        maps.append(map)
    else:
        map['vals'].append([int(r) for r in re.findall(r'\d+', d)])

def seed_to_loc(maps, seed):
    s = seed
    for map in maps:
        d = s
        for m in map['vals']:
            if m[1] <= s < m[1] + m[2]:
                d = s + (m[0]-m[1])
        s = d
    return s


def loc_to_seed(maps, loc):
    d = loc
    for map in reversed(maps):
        s = d
        for m in map['vals']:
            if m[0] <= d < m[0] + m[2]:
                s = d - (m[0]-m[1])
        d = s
    return d

locs = [seed_to_loc(maps, s) for s in seeds]

print(f'answer 1: {min(locs)}')

# Det här är nog inte nödvändigt.
starts = np.array([seeds[i] for i in range(0, len(seeds), 2)])
steps = np.array([seeds[i+1] for i in range(0, len(seeds), 2)])
idx = np.argsort(starts)
starts = list(starts[idx])
steps = list(steps[idx])
new_starts = [starts[0]]
new_stops = [starts[0] + steps[0]]
for j, start in enumerate(starts[1:]):
    i = j + 1
    if starts[i] <= new_stops[-1]:
        new_stops[-1] = starts[i] + steps[i]
    else:
        new_starts.append(starts[i])
        new_stops.append(starts[i] + steps[i])




def in_seeds(new_starts, new_stops, s):
    found = False
    for start, stop in zip(new_starts, new_stops):
        #print((start, s, stop))
        if start <= s < stop:
            found = True
            break
    return found

l = 0
while not in_seeds(new_starts, new_stops, loc_to_seed(maps, l)):
    l += 1

print(l)

from utils.imports import *
file = 'input.txt'
#file = 'test2.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]

instr = data[0]

network = {}
for d in data[2:]:
    node = {}
    source, lr = d.split(' = ')
    l, r = lr[1:-1].split(', ')
    network[source] = {'L': l, 'R': r}


start_nodes = []
stop_nodes = []
for key, val in network.items():
    if key[2] == 'A':
        start_nodes.append(key)
    if key[2] == 'Z':
        stop_nodes.append(key)

steps = 0
done = False
li = len(instr)
sources = start_nodes

on_z = []
while not done:
    ins = instr[steps % li]
    sources = [network[s][ins] for s in sources]
    steps += 1
    z = [s[2] == 'Z' for s in sources]
    for channel, zz in enumerate(z):
        if zz:
            on_z.append([start_nodes[channel], steps])
    if steps == 1000000:
        done = True
print(f'Answ2: {steps}')

on_z = np.array(on_z)
z_stat = {}
for s in start_nodes:
    z = on_z[on_z[:, 0] == s][:, 1].astype('int')
    zd = np.diff(z)
    z_stat[s] = (z, zd)

for s in start_nodes:
    print('*')
    print(s)
    print((z_stat[s][0][0:10]))
    print((z_stat[s][1][0:10]))
print(f'Answ2: {math.lcm(**[z_stat[s][1][-1] for s in start_nodes])}')

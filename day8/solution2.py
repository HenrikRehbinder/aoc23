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
#traverse_instr = 0
li = len(instr)
sources = start_nodes
while not done:
    ins = instr[steps % li]
    sources = [network[s][ins] for s in sources]
    print(sources)
    steps += 1
    if all([s[2] == 'Z' for s in sources]):
        done = True
    #if steps==1001: break

print(f'Answ2: {steps}')


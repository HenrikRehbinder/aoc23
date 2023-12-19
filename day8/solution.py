from utils.imports import *
file = 'input.txt'
#file = 'test1.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]

instr = data[0]

network = {}
for d in data[2:]:
    node = {}
    source, lr = d.split(' = ')
    l, r = lr[1:-1].split(', ')
    network[source] = {'L': l, 'R': r}

steps = 0
done = False
traverse_instr = 0
li = len(instr)
source = 'AAA'
while not done:
    source = network[source][instr[steps % li]]
    steps += 1
    if source == 'ZZZ':
        done = True

print(f'Answ: {steps}')

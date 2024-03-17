import sys
sys.path.append('..')
from utils.imports import *
file = 'input.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]

workflows = {}
space = False
row = 0
d = data[row]
while not space:
    d = data[row]
    name, flow = d.split('{')
    flow = flow[:-1].split(',')

    row = row + 1
    d = data[row]
    space = d == ''
    workflows[name] = flow

states = []
for d in data[row+1:]:
    state_str = d[1:-1].split(',')
    state = {}
    for s in state_str:
        tag, num = s.split('=')
        state[tag] = int(num)
    states.append(state)

def process_state(state, workflow):
    x = state['x']
    m = state['m']
    a = state['a']
    s = state['s']
    #print((x,m,a,s))
    for flow in workflow:
        sp = flow.split(':')
        if len(sp) == 1:
            #print('1')
            #print(sp)
            return sp
        else:
            #print('2')
            test = sp[0]
            res = sp[1]
            #print((test, res, eval(test)))
            if eval(test):
                return res

ans = 0
for state in states:
    #print(state)
    accepted = False
    rejected = False
    workflow_sequence = ['in']
    while not (accepted or rejected):
        next_workflow = process_state(state, workflows[workflow_sequence[-1]])
        #print(next_workflow)
        if type(next_workflow) is not str:
            next_workflow = next_workflow[0]
        workflow_sequence.append(next_workflow)
        accepted = next_workflow == 'A'
        rejected = next_workflow == 'R'
    #print(workflow_sequence)
    if accepted:
        ans += state['x'] + state['m'] + state['a'] + state['s']
print(ans)



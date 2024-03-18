import sys
sys.path.append('..')
from utils.imports import *
file = 'test1.txt'
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
print(f'Ans: {ans} 377025 correct for the first task')


#def add_one_step(step_name, workflows):
def add_logic(rules):
#workflow = workflows['qqz']
    conditions = [s.split(':')[0] for s in rules[:-1]]
    tmp_c = []
    for c in conditions:
        #print(c)
        if '>' in c:
            c = c.replace('>', '<=')
        elif '<' in c:
            c = c.replace('<', '>=')
        else:
            print('elände')
        tmp_c.append(c)
        tmp_c.append(' and ')
    #print(tmp_c)

    conditions.append(f'{"".join(tmp_c[:-1])}')
    next_workflows = [s.split(':')[1] for s in rules[:-1]] + [rules[-1]]
    extended_rules = []
    for cond, next in zip(conditions, next_workflows):
        extended_rules.append(cond + ':' + next)
    return extended_rules

for name, rules in workflows.items():
    workflows[name] = add_logic(rules)


def add_one_step(rule, workflows):
    new_rule_list = []
    cond, next = rule.split(':')
    if next in ['A', 'R']:
        new_rule_list = [rule]
    else:
        for rule in workflows[next]: 
            new_rule_list.append(cond + ' and ' + rule)
    return new_rule_list

test = add_one_step(workflows['in'][1], workflows)
print(test)

wf = workflows['in']
def extend_workflow(wf, workflows):
    t = []
    for part in wf:
        wf_list = add_one_step(part, workflows)
        for x in wf_list:
            t.append(x)
    return t

def extend_list(wfs, workflows):
    extended = []
    for wf in wfs:
        print('wf: ' + wf)
        wf_ext = extend_workflow(wf, workflows)
        for x in wf_ext:
            extended.append(x)
    return extended

wf_list = workflows['in']
all_AR = False
while not all_AR:
    wf_list = extend_workflow(wf_list, workflows)
    nexts = [rule.split(':')[-1] for rule in wf_list]
    all_AR = True
    for next in nexts:
        if not next in ['A', 'R']:
            all_AR = False
            break

terminating = []
for wf in wf_list:
    cond, res = wf.split(':')
    if res == 'A':
        terminating.append(cond)
var_names = ['a', 'x', 'm', 's']
bounds = []
for t in terminating:
    conditions = t.split(' and ')
    lower = {}
    for v in var_names:
        lower[v] = [1]
    higher = {}
    for v in var_names:
        higher[v] = [4000]

    for cond in conditions:
        for v in var_names:
            if cond[0] == v:
                if '>=' in cond:
                    lower[v].append(int(cond[3:]))
                elif '<=' in cond:
                    higher[v].append(int(cond[3:]))
                elif '>' in cond:
                    lower[v].append(int(cond[2:])+1)
                else:
                    higher[v].append(int(cond[2:])-1)

    d = {}
    for v in var_names:
        d[v] = (max(lower[v]), min(higher[v]))
    bounds.append(d)

for b in bounds:
    print(b)

combinations = 0
for b in bounds:
    c = 1
    for v in var_names:
        c *= b[v][1] - b[v][0] + 1
    combinations += c
print(combinations)

# Man kanske ska först skapa alla workflow sequences som kan förekomma. 
# Varje sån mappar väl till en uppsättning olikheter. 

#workflow_sequences = ['in']





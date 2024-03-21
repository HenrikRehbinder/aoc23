import sys
sys.path.append('..')
from utils.imports import *
from functions import *
import itertools

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
    state['size'] = 1
    states.append(state)


ans = 0
for state in states:
    ans += eval_state(state, workflows, 1)

print(f'Ans: {ans} 377025 correct for the first task')



# Find partitioning limits of variables
var_names = ['a', 'x', 'm', 's']
'''print('1')
limits = {}
centers = {}
widths = {}
for v in var_names:
    limits[v] = [1, 4000]
    centers[v] = []
    widths[v] = []
# här skapar jag en massa onödigt.
for key, rules in workflows.items():
    for rule in rules:
        s_rule = rule.split(':')
        if len(s_rule) == 2:
            var, limit = s_rule[0].replace('<', '.').replace('>', '.').replace('=', '').split('.')
            limits[var].append(int(limit))
            '''
'''
print('2')
#limits = {}
#for var in var_names:
#    limits[var] = [1, 10, 15, 20]
#old_limits = limits

partitioning = {}
for var in var_names:
    lims = sorted(limits[var])
    limits[var] = lims
    centers[var] = [[int((lu+ll)/2), int(lu-ll-1)] for lu, ll in zip(lims[1:], lims[:-1])]
    centers[var][0][1] += 1
    centers[var][-1][1] += 1

    #widths[var] = [int((lu-ll)) for lu, ll in zip(lims[1:], lims[:-1])]
    x = []
    for i, l in enumerate(limits[var][1:-1]):
        x.append(centers[var][i])
        x.append((l, 1))
    x.append(centers[var][-1])
    partitioning[var] = x

print(f'Number of partitions {len(partitioning["a"])*len(partitioning["x"])*len(partitioning["m"])*len(partitioning["s"])}')
'''

old_workflows = workflows.copy()

for name, rules in workflows.items():
    workflows[name] = add_logic(rules)



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


red_limits = {}

for var in var_names:
    red_limits[var] = [1, 4000]
for term in terminating:
    u, l = find_eq_limits(term)
    for var in var_names:
        tmp = red_limits[var] + [u[var], l[var]]
        red_limits[var] = list(set(tmp))
for var in var_names:
    red_limits[var] = sorted(red_limits[var])
#limits = {}
centers = {}
#widths = {}
#for v in var_names:
#    limits[v] = [1, 4000]
#    centers[v] = []
 #   widths[v] = []

red_partitioning = {}
for var in var_names:
    lims = sorted(red_limits[var])
    red_limits[var] = lims
    # centers is bad name. It's center and width
    centers[var] = [[int((lu+ll)/2), int(lu-ll-1)] for lu, ll in zip(lims[1:], lims[:-1])]
    centers[var][0][1] += 1
    centers[var][-1][1] += 1

    #widths[var] = [int((lu-ll)) for lu, ll in zip(lims[1:], lims[:-1])]
    x = []
    for i, l in enumerate(red_limits[var][1:-1]):
        x.append(centers[var][i])
        x.append((l, 1))
    x.append(centers[var][-1])
    red_partitioning[var] = x

p = len(red_partitioning["a"])*len(red_partitioning["x"])*len(red_partitioning["m"])*len(red_partitioning["s"])

print(f'Number of reduced partitions {p}')

term_limits = []
for term in terminating:
    u, l = find_eq_limits(term)
    tmp = {}
    for var in var_names:
        tmp[var] = [l[var], u[var]]
    term_limits.append(tmp)

new_strs = []
for tl in term_limits:
    s = ''
    for var in var_names:
        s = s + f'{tl[var][0]}<={var}<={tl[var][1]} and '
    new_strs.append(s[:-5])


print(len(term_limits))
insides = []
for i, term in enumerate(term_limits):
    for compare in term_limits[:i] + term_limits[i+1:]:
        if inside(term, compare):
            insides.append(i)
            break

inters = np.zeros((len(term_limits), len(term_limits)))

check = []
for row, term1 in enumerate(term_limits):
    for col, term2 in enumerate(term_limits):
        if intersect(term1, term2):
            inters[row, col] = 1
            check.append([row,col])

int_row = []
non_int_row = []
for i, row in enumerate(inters):
    if sum(row) == 1:
        non_int_row.append(i)
    else:
        int_row.append(i)

# testa våra limits.
A = []
for term in term_limits:
    state = {}
    for var in 'xmas':
        state[var] = int(np.mean(term[var]))
    A.append(eval_state(state, workflows, 1))
'''
siz = 0
p = 0
for term, expr in zip(term_limits, new_strs):
    print(p/len(term_limits)*100)
    tmp_limits = {}
    for var in var_names:
        var_lim = term[var]
        tmp_limits[var] = [vv for vv in red_limits[var] if term[var][0] <= vv <= term[var][1]]
    print(term)
    #print(tmp_limits)
    for a in tmp_limits['a']:
        for x in tmp_limits['x']:
            for m in tmp_limits['m']:
                for s in tmp_limits['s']:
                    if eval(expr):
                        siz += 1
    #for c in itertools.product(*tmp_limits.values()):
    #    x = c[0]
    #    m = c[1]
    #    a = c[2]
    #    s = c[3]
    #    if eval(expr):
    #        siz += 1
    p += 1

'''

if False:
    #print(limits)
    #print(partitioning)
    print('3')
    from tqdm import tqdm
    ans2 = 0
    n = 0
    for c in itertools.product(*red_partitioning.values()):
        if n%1000 == 0:
            print(f'{n/p*100}%')
        #state = {}
        #size = 1
        x = c[0][0]
        m = c[1][0]
        a = c[2][0]
        s = c[3][0]
        #for i, var in enumerate(var_names):
        #    state[var] = c[i][0]
        #    size *= c[i][1]
        #state['size'] = size
        #A = False
        for term in new_strs:
            #expression = "math.sin(v['x']) * v['y']"
            exp_as_func = eval('lambda: ' + term)
            #a = new_state_eval(state, term)
            if exp_as_func():
                #size = c[0][1] * c[1][1] * c[2][1] * c[3][1]

                ans2 += c[0][1] * c[1][1] * c[2][1] * c[3][1]
                break
        n += 1

    print(f'Ans: {ans2} 167409079868000 correct for the second task')
    print(f'I have {ans2-167409079868000} too many')
    print(f'I have {167409079868000-ans2} too few')


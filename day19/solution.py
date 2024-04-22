import sys
sys.path.append('..')
from utils.imports import *
from functions import *
import copy
import itertools

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
    state['size'] = 1
    states.append(state)


ans = 0
for state in states:
    ans += eval_state(state, workflows, 1)

print(f'Ans: {ans} 377025 correct for the first task')

def find_wf_type(flow):
    nexts = np.array([cond.split(':')[-1] for cond in flow])
    #nexts.append(flow[-1])
    if np.all(nexts == 'A'):
        return 'AA'
    elif np.all(nexts == 'R'):
        return 'RR'
    elif sum(nexts == 'A') + sum(nexts == 'R') == len(nexts):
        return 'AR'
    else:
        return 'C'

for n,f in workflows.items(): print((n,f))
wf_types = [find_wf_type(flow) for name, flow in workflows.items()]
for term_type in ['AA', 'RR', 'AR', 'C']:
    print((term_type, sum(np.array(wf_types) == term_type)))
print('---')


def remove_terminators(workflows):
    wf_types = [find_wf_type(flow) for name, flow in workflows.items()]

    removed = False
    simple_terminators = {}
    for name, flow in workflows.items():
        wf_type = find_wf_type(flow)
        if wf_type in ['AA', 'RR']:
            simple_terminators[name] = wf_type
            removed = True
    for name, term_type in simple_terminators.items():
        del workflows[name]

    for term_name, term_type in simple_terminators.items():
        replacer = None
        if term_type == 'AA':
            replacer = 'A'
        elif term_type == 'RR':
            replacer = 'R'
        if replacer is None:
            pass
        else:
            for wf_name, flow in workflows.items():
                #print('Här har jag en bug. Jag måste ersätta bara när flow innehåller exakt term_name')
                for i, f in enumerate(flow):
                    fsplit = f.split(':')
                    if fsplit[-1] == term_name:
                        fsplit[-1] = replacer
                    if len(fsplit) == 1:
                        flow[i] = fsplit[0]
                    elif len(fsplit) == 2:
                        flow[i] = ''.join([fsplit[0], ':', fsplit[1]])
                    else:
                        print('Error')
                #flow = [f.replace(term_name, replacer) for f in flow]
                workflows[wf_name] = flow

    return workflows, removed

print(len(workflows))
removed = True
while removed:
    workflows, removed = remove_terminators(workflows)
    print(len(workflows))


new_wf_types = [find_wf_type(flow) for name, flow in workflows.items()]

for term_type in ['AA', 'RR', 'AR', 'C']:
    print((term_type, sum(np.array(new_wf_types) == term_type)))



# Find partitioning limits of variables
var_names = ['a', 'x', 'm', 's']
'''
limits = {}
centers = {}
widths = {}
for v in var_names:
    limits[v] = [1, 4000]
    centers[v] = []
    widths[v] = []
print('1')

# här skapar jag en massa onödigt.
for key, rules in workflows.items():
    for rule in rules:
        s_rule = rule.split(':')
        if len(s_rule) == 2:
            var, limit = s_rule[0].replace('<', '.').replace('>', '.').replace('=', '').split('.')
            limits[var].append(int(limit))


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
# det här var nog onödigt
#old_workflows = workflows.copy()

# Det är nog rätt hit. Däremot så skulle man ju kanke vilja ändra logik
# bara för de som inte är AR

# Det som kommer nedan funkar fortfarande inte - det blir för många partitioner.
# Alternativet är då att bygga upp partitionerna när man traverserar flödet.
# I varje steg så måste man då göra en partition och märka upp om varje komponent är
# R, A eller U(ndecided). De som är U tar man vidare. Om vi låter en komponent vara
# en hyperkub så måste man då dela upp OR-villkoret i sådana. Ett sätt att göra detta på
# är att man först identifierar limits i varje steg. Baserat på dessa (och de limits man kommer
# in i steget med så skapar man de hyperkuber som limits definierar. De som kommer
# från de n-1 första villkoren har sina villkor givna av flow. De andra ges av sista villkoret.
# Låter ju ganska bra. Hur representerar man det här då.
# ('xrl', ['x>3598:khp', 'm>284:lbp', 'm<100:R', 'xq'])
# Komponenter jag behöver:
# - find_limits. Den är ju trivial om man bara ska ha siffrorna. Behöver man ">"?
# class HyperCube(limits)
# - limits,
#  - termination: R, A or U
#  - split(flow) -> [hypercube]
# limits: {'a': [23,45], ...} Alla villkor i wf är givna som olikheter. Men eftersom OR-villkoret
# kommer ge likheter så måste vi antingen
#  1) Hantera olikheter/likheter
#  2) Låta alla limits vara likheter och sen analysera dessa separat för att se om de ska tas bort eller inte.
#  2an är enklare och det borde inte bli så komplext. Hursomhelst så är det ett bra första skott och i värsta
#
# fall får jag gå tillbaka. Det är ju en potens lägre av ordo.
# Innan jag drar iväg i det här så skulle man vilja veta hur lång den långsta kedjan av uppdelningar blir.
# Kollade på wf-list, ser ut som 15 steg.
outer_limits = {}
for var in var_names:
    outer_limits[var] = [1, 4000]

def make_cubes(flow):
    limits = outer_limits.copy()
    print(limits)
    for f in flow[:-1]:
        cond, next = f.split(':')
        var = cond[0]
        ineq = cond[1]
        limit = int(cond[2:])
        if ineq == '<':
            limit = limit - 1
        else:
            limit = limit + 1
        limits[var].append(limit)
    print(limits)
    #for var in var_names:
    #    l = limits[var].sort()
    #    limits[var] = l
    return limits
def parse_step(step):
    cond_next_workflow = step.split(':')
    if len(cond_next_workflow) == 1:
        next_workflow = cond_next_workflow[0]
        ineq = None
        var = None
        val = None
    else:
        cond = cond_next_workflow[0]
        next_workflow = cond_next_workflow[1]
        ineq = cond[1]
        var, val = cond.split(ineq)
        val = int(val)

        if ineq == '<':
            val = val - 1
        else:
            val = val + 1
        ineq = ineq + '='
    return var, ineq, val, next_workflow

def split_block(limits, step, step_history):
    var, ineq, val, next_workflow = parse_step(step)
    if var is None:
        next_block = HyperCube(limits, next_workflow, step_history)
        block_complement = None
    else:
        if limits[var][0] <= val <= limits[var][1]:
            next_block_limits = copy.deepcopy(limits)
            complement_block_limits = copy.deepcopy(limits)
            #print('new cube', next_block_limits)
            if ineq == '<=':
                next_block_limits[var][1] = val
                complement_block_limits[var][0] = val + 1
            else:
                next_block_limits[var][0] = val
                complement_block_limits[var][1] = val - 1
            next_block = HyperCube(next_block_limits, next_workflow, step_history)
            block_complement = HyperCube(complement_block_limits, 'T', step_history)
        else:
            print('found dead end')
            next_block = None
            block_complement = None
    return next_block, block_complement


'''    
    flow_ineq = {}
    for f in flow[:-1]:
        cond, next = f.split(':')
        var = cond[0]
        ineq = cond[1]
        limit = int(cond[2:])
        if ineq == '<':
            limit = limit - 1
        else:
            limit = limit + 1
        #?
'''


class HyperCube:
    def __init__(self, limits, workflow_name, step_history):
        self.limits = limits
        self.wf_name = workflow_name
        self.variables = 'xmas'
        self.containing = []
        self.step_history = step_history + ':' + self.wf_name
        print('*** Creating object ***')
        print(self.wf_name)
        print(self.limits)
        if self.wf_name not in ['R', 'A', 'T']:
            self.find_hcs_inside()
        for hc in self.containing:
            print(hc.wf_name)
        self.size = 1
        for var in self.variables:
            self.size *= self.limits[var][1]-self.limits[var][0]+1


    def get_all_blocks(self):
        print('get_blocks for ', self.wf_name)
        all_blocks = self.containing
        for block in self.containing:
            if block.wf_name not in ['A', 'R', 'T']:
                print('getting - ', block.wf_name)
                new_blocks = block.get_all_blocks()
                for n_b in new_blocks:
                    all_blocks.append(n_b)
                #all_blocks = list(np.array(all_blocks).flatten())
            else:
                print('stopping - ', block.wf_name)

        print([b.wf_name for b in all_blocks])
        return list(np.array(all_blocks).flatten())

    def find_hcs_inside(self):
        #if self.wf_name not in ['R', 'A']:
        limits = copy.deepcopy(self.limits)
        for step in workflows[self.wf_name]:
            next_block, temp_block = split_block(limits, step, self.step_history)
            if next_block is not None:
                self.containing.append(next_block)
                if temp_block is not None:
                    limits = copy.deepcopy(temp_block.limits)

'''
    def find_hcs_inside_old(self, flow):
        # jag måste göra en partitionering baserat på limits.
        hcs = []
        for step in flow[:-1]:
            #extract limiting variable and value
            cond, termination = step.split(':')
            ineq = cond[1]
            var, val = cond.split(ineq)
            val = int(val)

            if ineq == '<':
                val = val - 1
            else:
                val = val + 1
            # check if val is in current cube and define limits for new hc and create
            if self.limits[var][0] <= val <= self.limits[var][1]:
                hc_limits = copy.deepcopy(self.limits)
                print('new cube', hc_limits)
                if ineq == '<':
                    hc_limits[var][1] = val
                else:
                    hc_limits[var][0] = val
                hcs.append(HyperCube(hc_limits, termination))
            print('Jag har inte hanterat or-varianten - alltså den sista i flow.')
            # Det är nog det jag börjat med nedan.
            self.containing = hcs

        #partitioning_limits = self.find_ineq(flow)
        # partitioning limits är en {'x':[[l1,l2], [l2,l3], 'm':[],...}
        #hcs = []
        ##for cube in itertools.product(*partitioning_limits.values()):
        #3    hcs.append(HyperCube(limits, ))
        #return find_hcs
'''
    #def is_inside(self, ):
#flow = workflows['in']
#hc = HyperCube(outer_limits, 'in')
#hc.find_hcs_inside(flow)

#b, bc = split_block(outer_limits, workflows['in'][0])
#print(b.limits)
#print(bc.limits)
#a, ac = split_block(outer_limits, workflows['in'][1])
#print(a.limits)
#print(ac.limits)

in_block = HyperCube(outer_limits, 'in', '')
#in_block.find_hcs_inside()
all_blocks = in_block.get_all_blocks()
ans2 = 0
num_A = 0
print('=============================================')

for block in all_blocks:
    if block.wf_name in ['A', 'R']:
        if block.wf_name == 'A':
            print('*****')
            print(block.wf_name, block.size, block.step_history)
            print(block.limits)
            #print(block.size)
            #print(block.step_history)
            ans2 += block.size
            num_A += 1

print(f'Answer {ans2}, correct for test 1 is 167409079868000')
print(f'ans2-true = {ans2-167409079868000}')
print(f'A: {num_A}')

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

'''
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
'''

'''
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
    '''


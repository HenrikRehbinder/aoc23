import sys
sys.path.append('..')
from utils.imports import *
from functions import *
import copy
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

print('--------')
for name, flow in workflows.items():
    print(name, flow)
print('--------')


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


var_names = 'xmas'

outer_limits = {}
for var in var_names:
    outer_limits[var] = [1, 4000]


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
        print(step)
        print(var, ineq, val, next_workflow)
    return var, ineq, val, next_workflow

def split_block(limits, step, step_history):
    var, ineq, val, next_workflow = parse_step(step)
    #print(var, ineq, val, next_workflow)
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
        if self.wf_name == 'A':
            self.size = 1
            for var in self.variables:
                self.size *= self.limits[var][1]-self.limits[var][0]+1
        else:
            self.size = 0

    def get_A_sizes(self):
        if len(self.containing) > 0:
            return sum([c.get_A_sizes() for c in self.containing])
        else:
            return self.size

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
        print(f'find hcs inside of *{self.wf_name}*')
        print(workflows[self.wf_name])
        #if self.wf_name not in ['R', 'A']:
        limits = copy.deepcopy(self.limits)
        for step in workflows[self.wf_name]:
            print(step)
            next_block, temp_block = split_block(limits, step, self.step_history)
            if next_block is not None:
                self.containing.append(next_block)
                if temp_block is not None:
                    limits = copy.deepcopy(temp_block.limits)
        for block in self.containing:
            print(block.wf_name)
        print('---done---')


in_block = HyperCube(outer_limits, 'in', '')

ans2 = in_block.get_A_sizes()



print(f'Answer {ans2}, correct for test 1 is 167409079868000, for real 135506683246673')
print(f'ans2-true_test = {ans2-167409079868000}')
print(f'ans2-true_input = {ans2-135506683246673}')


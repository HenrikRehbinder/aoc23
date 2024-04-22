var_names = ['a', 'x', 'm', 's']
def new_state_eval(state, cond):
    x = state['x']
    m = state['m']
    a = state['a']
    s = state['s']
    return eval(cond)

def inside(cond1, cond2):
    ins = True
    for x in cond2['x']:
        for m in cond2['m']:
            for a in cond2['a']:
                for s in cond2['s']:
                    if not (
                            cond1['x'][0] < x < cond1['x'][1] and
                            cond1['m'][0] < m < cond1['m'][1] and
                            cond1['a'][0] < a < cond1['a'][1] and
                            cond1['s'][0] < s < cond1['s'][1]
                    ):
                        ins = False
                        break
    return ins

def intersect(cond1, cond2):
    #cond2 has one corner inside of cond1
    def inter(cond_a, cond_b):
        ins = 0
        for x in cond_b['x']:
            for m in cond_b['m']:
                for a in cond_b['a']:
                    for s in cond_b['s']:
                        if (
                                cond_a['x'][0] <= x <= cond_a['x'][1] and
                                cond_a['m'][0] <= m <= cond_a['m'][1] and
                                cond_a['a'][0] <= a <= cond_a['a'][1] and
                                cond_a['s'][0] <= s <= cond_a['s'][1]
                        ):
                            ins += 1
        return ins
    ins = inter(cond1, cond2) + inter(cond2, cond1)
    if ins >= 1:
        return 1
    else:
        return 0


def add_logic(rules):
#workflow = workflows['qqz']
    conditions = [s.split(':')[0] for s in rules[:-1]]
    tmp_c = []
    #replacers = {'>=': '<', '<=': '>', '>': '<=', '<': '>='}
    for c in conditions:
        #print(c)
        if '>' in c:
            c = c.replace('>', '<=')
        elif '<' in c:
            c = c.replace('<', '>=')
        else:
            print('fan')
        #print(c)
        tmp_c.append(c)
        tmp_c.append(' and ')

    conditions.append(f'{"".join(tmp_c[:-1])}')
    next_workflows = [s.split(':')[1] for s in rules[:-1]] + [rules[-1]]
    extended_rules = []
    for cond, next in zip(conditions, next_workflows):
        extended_rules.append(cond + ':' + next)
    return extended_rules


def add_one_step(rule, workflows):
    new_rule_list = []
    print(rule)
    cond, next = rule.split(':')
    if next in ['A', 'R']:
        new_rule_list = [rule]
    else:
        for rule in workflows[next]:
            new_rule_list.append(cond + ' and ' + rule)
    return new_rule_list



def extend_workflow(wf, workflows):
    t = []
    for part in wf:
        #print(part)
        wf_list = add_one_step(part, workflows)
        for x in wf_list:
            t.append(x)
    return t

def extend_list(wfs, workflows):
    extended = []
    for wf in wfs:
        #print('wf: ' + wf)
        wf_ext = extend_workflow(wf, workflows)
        for x in wf_ext:
            extended.append(x)
    return extended

def find_eq_limits(cond_str):
    var_names = ['a', 'x', 'm', 's']
    uppers = {}
    lowers = {}
    for var in var_names:
        uppers[var] = 4000
        lowers[var] = 1
    conds = cond_str.split(' and ')
    for cond in conds:
        if '=' in cond:
            eq = True
        else:
            eq = False
        cond = cond.replace('=', '')
        if '<' in cond:
            rel = '<'
        else:
            rel = '>'
        var, lim = cond.split(rel)
        if rel == '<':
            if not eq:
                cand = int(lim)-1
            else:
                cand = int(lim)
            uppers[var] = min((uppers[var], cand))
        else:
            if not eq:
                cand = int(lim)+1
            else:
                cand = int(lim)
            lowers[var] = max((lowers[var], cand))
    return uppers, lowers


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

def eval_state(state, workflows, task):
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
        if task == 1:
            return state['x'] + state['m'] + state['a'] + state['s']
        else:
            return state['size']
    else:
        return 0

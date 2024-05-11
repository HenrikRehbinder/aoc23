import sys
import math as math
sys.path.append('..')
from utils.imports import *

file_name = 'input.txt'
with open(file_name) as file:
    data = [s.strip() for s in file.readlines()]


class FlipFlop:
    '''
    Flip-flop modules (prefix %) are either on or off; they are initially off. If a flip-flop module receives
    a high pulse, it is ignored and nothing happens. However, if a flip-flop module receives a low pulse, it
    flips between on and off. If it was off, it turns on and sends a high pulse. If it was on, it turns off
    and sends a low pulse.
    '''
    def __init__(self, name, output):
        self.name = name
        self.state = 'off'
        self.output_modules = output
        self.last_input = ''
        self.input_modules = []

    def add_input_module(self, input):
        self.input_modules.append(input)

    def get_outputs(self):
        return self.output_modules

    def process(self, input, pulse):
        if pulse == 'low':
            if self.state == 'off':
                self.state = 'on'
            elif self.state == 'on':
                self.state = 'off'
            else:
                print('error')
        self.last_input = pulse


    def send(self):
        if self.last_input == 'high':
            pass
        else:
            if self.state == 'on':
                to_send = 'high'
            else:
                to_send = 'low'
            num_of_pulses[to_send] += len(self.output_modules)
            return {'from': self.name, 'to': self.output_modules, 'pulse': to_send}
#

class Conjunction:
    '''
    Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected
    input modules; they initially default to remembering a low pulse for each input. When a pulse is received, the
    conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs,
    it sends a low pulse; otherwise, it sends a high pulse.
    '''
    def __init__(self, name, output):
        self.name = name
        self.output_modules = output
        self.input_modules = []
        self.last_inputs = {}

    def add_input_module(self, input):
        self.input_modules.append(input)
        self.last_inputs[input] = 'low'

    def get_outputs(self):
        return self.output_modules

    def process(self, input, pulse):
        self.last_inputs[input] = pulse

    def send(self):
        to_send = 'low'
        for i, p in self.last_inputs.items():
            if p == 'low':
                to_send = 'high'
                break
        num_of_pulses[to_send] += len(self.output_modules)
        return {'from': self.name, 'to': self.output_modules, 'pulse': to_send}


class Broadcast:
    '''
    There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to
    all of its destination modules.
    '''
    def __init__(self, name, outputs):
        self.name = name
        self.output_modules = outputs
        self.input_modules = []
        self.last_input = None


    def add_input_module(self, input):
        self.input_modules.append(input)

    def get_outputs(self):
        return self.output_modules

    def process(self, input, pulse):
        self.last_input = pulse

    def send(self):
        to_send = self.last_input
        num_of_pulses[to_send] += len(self.output_modules)
        return {'from': self.name, 'to': self.output_modules, 'pulse': to_send}


class Button:
    '''
    There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to
    all of its destination modules.
    '''
    def __init__(self):
        self.name = 'button'
        self.output_modules = ['broadcaster']
        self.input_modules = None

    def get_outputs(self):
        return self.output_modules

    def send(self):
        to_send = 'low'
        num_of_pulses[to_send] += len(self.output_modules)

        return {'from': self.name, 'to': self.output_modules, 'pulse': to_send}

class Output:
    '''
    There is a single broadcast module (named broadcaster). When it receives a pulse, it sends the same pulse to
    all of its destination modules.
    '''
    def __init__(self, input):
        self.name = 'output'
        self.output_modules = []
        self.input_modules = input
    def get_outputs(self):
        return self.output_modules

    def add_input_module(self, input):
        self.input_modules.append(input)

    def process(self, input, pulse):
        pass

    def send(self):
        pass


num_of_pulses = {'high': 0, 'low': 0}
modules = {}
for d in data:
    typename, outputs = d.replace(' ', '').split('->')
    outputs = outputs.split(',')
    if typename[0] == 'b':
        name = typename
        modules[name] = Broadcast(name, outputs)
    elif typename[0] == '%':
        name = typename[1:]
        modules[name] = FlipFlop(name, outputs)
    elif typename[0] == '&':
        name = typename[1:]
        modules[name] = Conjunction(name, outputs)
if file_name == 'test2.txt':
    button_presses = 4
    modules['output'] = Output(['con'])
elif file_name == 'test1.txt':
    button_presses = 1
else:
    button_presses = 1000
    # this is a hack, or an insight from data. rx doesn't send anything so it act as
    # the Output in test2.txt
    modules['rx'] = Output(['df'])
modules['button'] = Button()
for module_name, module in modules.items():
    for output in module.get_outputs():
        modules[output].add_input_module(module_name)
if file_name == 'input.txt':
    modules['rx'].input_modules = ['df']

def press_button():
    message_q = []
    message_q.append(modules['button'].send())
    q_exec = 0

    while q_exec < len(message_q):
        message = message_q[q_exec]
        for module_name in message['to']:
            modules[module_name].process(message['from'], message['pulse'])
            new_message = modules[module_name].send()
            if new_message is not None:
                message_q.append(new_message)
        q_exec += 1
    return message_q

def find_downstream_modules(name, found):
    dsm = modules[name].output_modules
    all_dsm = []
    found_dsm = list(set(found).union(set(dsm)))
    if len(found_dsm) == len(found):
        all_dsm = found_dsm
    else:
        for m in dsm:
            for ndsm in find_downstream_modules(m, found_dsm):
                all_dsm.append(ndsm)
        all_dsm = list(set(all_dsm))
    return all_dsm


task = 2
if task == 1:
    for p in range(button_presses):
        print(f'Press button ({p+1})')
        message_q, bf = press_button()
        for m in message_q:
            for to in m['to']:
                print(f'{m["from"]} -{m["pulse"]}-> {to}')

    print(num_of_pulses)
    print(f'ans1: {num_of_pulses["high"]*num_of_pulses["low"]} True is 666795063')

else:

# Sista modulen är rx. Hur många knapptryck krävs för att low ska skickas till rx
# Det sägs något om "single low pulse.
# den enda som skickar till rx är df.
# df är en Conjunction och kommer att skicka low om samtliga
# inputs är high.

# Vi gissar att det finns någon sorts periodocitet. Att dfs inputs skickar
# high med viss frekvens och så blir det någon sorts minsta gemensamma divisor eller liknande.
# ['xl', 'ln', 'xp', 'gp'] -> df -> rx
# enligt analysen nedan så är det oberoende nätverk mellan de fyra ut från broadcaster och de fyra in i df.
# Hittar man periodicitet för dessa är man hemma.


    lasts = [m for m in modules['df'].input_modules]
    record = {}
    from tqdm import tqdm

    for last in lasts:
        record[last] = []
    n = 100000

    for i in tqdm(range(n)):
        message_q = press_button()
        # log if message sent to last are 'high'
        for message in message_q:
            if message['from'] in lasts:
                if message['pulse'] == 'high':
                    record[message['from']].append(i)

# Pre peaked into data. # diff is equal, periodicity given.
periods = []
for m, hist in record.items():
    print(m, hist)
for m, hist in record.items():
    d = [hh-h for hh,h in zip(hist[1:], hist[:-1])]
    print(m, d)
    periods.append(d[0])

print(periods)

print(f'ans2: {math.lcm(*periods)} True is 253302889093151')


if False:
    # This shows that there indeed are four subgraphs.
    subgraphs = {}
    for m in modules['broadcaster'].output_modules:
        subgraphs[m] = find_downstream_modules(m,[])

    for m, g in subgraphs.items():
        print(m, len(g), g)
    print(len(find_downstream_modules('broadcaster',[])))

    for m,g in subgraphs.items():
        for mm,gg in subgraphs.items():
            inter = set(g).intersection(set(gg))
            print(m,mm,len(inter), inter, set(g).intersection(set(modules['df'].input_modules)))

    inp = modules['broadcaster'].output_modules
    oup = modules['df'].input_modules
    iomap = {'vl': 'xl', 'cs':'gp', 'cn': 'xp', 'ml': 'ln'}
    print(inp)
    print(oup)
    print(iomap)

    press_button()
    for ou in oup:
        print(modules[ou].last_inputs)


import sys
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
        self.last_input = None
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
#        for m in message_q:
##            print(m)
 #       print(q_exec)
 #       print('----')
        # input()
    if False:
        print('Message list')
        for m in message_q:
            for to in m['to']:
                print(f'{m["from"]} -{m["pulse"]}-> {to}')
        print(' ')
        print(num_of_pulses)


for p in range(button_presses):
    print(f'Press button ({p+1})')
    press_button()

print(num_of_pulses)
print(f'ans1: {num_of_pulses["high"]*num_of_pulses["low"]}')



#print('----')
#modules['broadcaster'].process('button','low')
#modules['broadcaster'].send()
#print('----')
#modules['broadcaster'].process('button','low')
#modules['broadcaster'].send()
#print('----')
#modules['broadcaster'].process('button','low')
#modules['broadcaster'].send()
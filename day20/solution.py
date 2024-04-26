import sys
sys.path.append('..')
from utils.imports import *
file = 'test2.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]


class Module:
    def __init__(self, str):
        typename, outputs = str.replace(' ', '').split('->')
        if typename[0] == 'b':
            self.type = 'bc'
            self.name = typename
            self.state = None
            self.last_received = None
            #self.will_send = True
        elif typename[0] == '%':
            self.type = 'ff'
            self.name = typename[1:]
            self.state = 'off'
        #    self.last_received = []
            #self.will_send = False
        elif typename[0] == '&':
            self.type = 'cj'
            self.name = typename[1:]
            self.state = None
        self.outputs = outputs.split(',')
 #       self.inputs = [] # needed?
        self.last_inputs = {}
        self.last_input = None

    def add_input(self, input):
  #      self.inputs.append(input) # needed?
        self.last_inputs[input] = 'low'
        #self.last_input = input

    def process(self, input, pulse):
        # pulses  = dict(input, pulse)
        self.last_input = input
        if self.type == 'bc':
            self.last_inputs[input] = pulse

        elif self.type == 'ff':
            self.last_inputs[input] = pulse
            if pulse == 'low':
                if self.state == 'off':
                    self.state = 'on'
                elif self.state == 'on':
                    self.state = 'off'
                else:
                    print('error')
        elif self.type == 'cj':
            self.last_inputs[input] = pulse
        elif self.type == 'output':
            pass
        else:
            print('Error')

    def send(self):
        #print(f'In {self.name}, to send *{self.to_send}* to {self.outputs} {self.will_send}')
        if self.type == 'bc':
            to_send = self.last_inputs[self.last_input]
        elif self.type == 'cj':
            to_send = 'low'
            for i, p in self.last_inputs.items():
                if p == 'low':
                    to_send = 'high'
                    break
        elif self.type == 'ff':
            #ff
            if self.last_inputs[self.last_input] == 'high':
                to_send = None
            else:
                #print('state: '+self.state)
                if self.state == 'on':
                    to_send = 'high'
                else:
                    to_send = 'low'
        else:
            to_send = None
        if to_send is not None:
            for output in self.outputs:
                print('send:' + self.name+' -'+to_send+'-> '+output)
                modules[output].process(self.name, to_send)
            for output in self.outputs:
                num_of_pulses[to_send] += 1
                modules[output].send()
            #for output in self.outputs:
             #   modules[output].send()
num_of_pulses = {'high': 0, 'low': 0}
modules = {}
for d in data:
    module = Module(d)
    modules[module.name] = module
modules['output'] = Module(d)
modules['output'].type = 'output'

for module_name, module in modules.items():
    for output in module.outputs:
        modules[output].add_input(module_name)

#modules['broadcaster'].inputs.append('button')

modules['broadcaster'].process('button','low')
modules['broadcaster'].send()
print('----')
modules['broadcaster'].process('button','low')
modules['broadcaster'].send()
print('----')
modules['broadcaster'].process('button','low')
modules['broadcaster'].send()
print('----')
modules['broadcaster'].process('button','low')
modules['broadcaster'].send()
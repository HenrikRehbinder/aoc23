import sys
sys.path.append('..')
from utils.imports import *
file = 'test1.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]


class FlipFlop:
    def __init__(self, name, output):
        self.name = name
        self.state = 'off'
        #    self.last_received = []
            #self.will_send = False
        self.output = output
#        self.last_inputs = {}
        self.last_input = None
        self.input_modules = []

    def add_input_module(self, input):
        self.input_modules.append(input)

    def get_outputs(self):
        return [self.output]

    def process(self, input, pulse):
        # pulses  = dict(input, pulse)
        self.last_input = input
        if pulse == 'low':
            if self.state == 'off':
                self.state = 'on'
            elif self.state == 'on':
                self.state = 'off'
            else:
                print('error')

    def send(self):
        if self.last_input == 'high':
            pass
        else:
            #print('state: '+self.state)
            if self.state == 'on':
                to_send = 'high'
            else:
                to_send = 'low'
            num_of_pulses[to_send] += 1
            modules[self.output].process(self.name, to_send)
            modules[self.output].send()


class Conjunction:
    def __init__(self, name, output):
        #typename, outputs = str.replace(' ', '').split('->')
        self.name = name
        self.output = output
        self.input_modules = []
        self.last_inputs = {}
    def add_input_module(self, input):
        self.input_modules.append(input)
        self.last_inputs[input] = 'low'

    def get_outputs(self):
        return [self.output]

    def process(self, input, pulse):
        # pulses  = dict(input, pulse)
        #self.last_input = input
        self.last_inputs[input] = pulse

    def send(self):
        #print(f'In {self.name}, to send *{self.to_send}* to {self.outputs} {self.will_send}')
        to_send = 'low'
        for i, p in self.last_inputs.items():
            if p == 'low':
                to_send = 'high'
                break
        num_of_pulses[to_send] += 1
        modules[self.output].process(self.name, to_send)
        modules[self.output].send()

class Broadcast:
    def __init__(self, name, outputs):
        # typename, outputs = str.replace(' ', '').split('->')
        self.name = name
        self.outputs = outputs
        self.input_modules = []
        self.last_input = None


    def add_input_module(self, input):
        self.input_modules.append(input)
        #self.last_input = ''

    def get_outputs(self):
        return self.outputs

    def process(self, input, pulse):
        # pulses  = dict(input, pulse)
        self.last_input = pulse
        #self.last_inputs[input] = pulse


    def send(self):
        #print(f'In {self.name}, to send *{self.to_send}* to {self.outputs} {self.will_send}')
        #to_send = self.last_input
        for output in self.outputs:
            print('send:' + self.name+' -'+self.last_input+'-> '+output)
            modules[output].process(self.name, self.last_input)
        for output in self.outputs:
            print('*')
            num_of_pulses[self.last_input] += 1
            modules[output].send()
        #for output in self.outputs:
         #   modules[output].send()

# Jag kanske ska hantera alla skickade pulser i nån sorts kö.
# Då behöver jag inte hantera det i klasserna. Det låter som att det blir enklare


num_of_pulses = {'high': 0, 'low': 0}
modules = {}
for d in data:
    typename, outputs = d.replace(' ', '').split('->')
    outputs = outputs.split(',')
    if typename[0] == 'b':
        name = typename
        modules[name] = Broadcast(name, outputs)
        #self.name = typename
        #self.state = None
        #self.last_received = None
        # self.will_send = True
    elif typename[0] == '%':
        name = typename[1:]
        modules[name] = FlipFlop(name, outputs[0])
    elif typename[0] == '&':
        name = typename[1:]
        modules[name] = Conjunction(name, outputs[0])
#modules['output'] = Här måste jag få till en lösning för test2.

for module_name, module in modules.items():
    for output in module.get_outputs():
        modules[output].add_input_module(module_name)

#modules['broadcaster'].inputs.append('button')

modules['broadcaster'].process('button','low')
modules['broadcaster'].send()

#print('----')
#modules['broadcaster'].process('button','low')
#modules['broadcaster'].send()
#print('----')
#modules['broadcaster'].process('button','low')
#modules['broadcaster'].send()
#print('----')
#modules['broadcaster'].process('button','low')
#modules['broadcaster'].send()
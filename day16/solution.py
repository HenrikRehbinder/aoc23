import sys
sys.path.append('..')
from utils.imports import *
#file_name = 'test1.txt'
file_name = 'input.txt'

with open(file_name) as file:
    data = [s.strip() for s in file.readlines()]

data = np.array([[d for d in dat] for dat in data])


beams = [{
    'num': 0, 
    'status': 'waiting', 
    'start_pos': [0, -1],
    'start_dir': [0, 1],
    'trajectory': []
    }]


class Mirrors():
    def __init__(self, mirrors):
        self.mirrors = mirrors
        self.visits = np.array([['.' for d in dat] for dat in data])
        self.directions = {
            'left': np.array([[False for d in dat] for dat in data]),
            'right': np.array([[False for d in dat] for dat in data]),
            'up': np.array([[False for d in dat] for dat in data]),
            'down': np.array([[False for d in dat] for dat in data]),
            'split': np.array([[False for d in dat] for dat in data])
            }
        self.beams = []
        self.reflections = {
            '/': {
                'left': 'down',
                'right': 'up',
                'up': 'right',
                'down': 'left'
            },
            '\\': {
                'left': 'up',
                'right': 'down',
                'up': 'left',
                'down': 'right'
                },
            '-': {
                'left': 'left',
                'right': 'right',
                'up': 'split',
                'down': 'split'
                },
            '|': {
                'left': 'split',
                'right': 'split',
                'up': 'up',
                'down': 'down'
                },
            '.': {
                'left': 'left',
                'right': 'right',
                'up': 'up',
                'down': 'down'
                  }
        }

    
    def print_visits(self):
        for v in self.visits:
            print(''.join(v))


    def ans1(self):
        return sum(sum(self.visits=='#'))
    

    def add_beam(self, start_pos, start_dir):
        beam = Beam(
            start_pos, start_dir, self#.mirrors, self.beam_visits, self.beam_directions
            )
        self.beams.append(beam)


    def do(self, start_pos, start_dir):
        sp = step(start_dir, start_pos)
        sd = self.reflections[self.mirrors[sp[0], sp[1]]][start_dir]
        if sd == 'split':
            if start_dir in ['left', 'right']:
                new_dirs = ['down', 'up']
            else:
                new_dirs = ['left', 'right']
            for new_dir in new_dirs:
                self.add_beam(sp, new_dir)
        else:
            self.add_beam(sp, sd)
               
        done = False
        i = 0
        while not done: 
            nsb = []
            for j, b in enumerate(self.beams):
                if not b.terminated:
                    nsb.append(j)
            print('----')
            print(nsb)
            if len(nsb)==0:
                done = True
            else:
                beam = self.beams[nsb[0]]
                print('evolving a beam')
                beam_splits, _ = beam.evolve()
                for beam_split in beam_splits:
                    print('adding splits')
                    #Kolla om den är i en loop. Eller kollar man det innan man skapar childrn. 
                    self.add_beam(beam_split[0], beam_split[1])
                    i += 1
                #if i > 40: 
                #    print('debug break')
                #    done=True
               # print(('len(self.beams)', len(self.beams))


       # self.beam_visits = beam.visits
       # print(beam.visits)
       # self.beam_directions = beam.visit_directions#

#        while not beam.status == 'terminated':
#            for child in beam.children:
#                self.add_beam(child.start_pos, child.start_dir)


def step(old_dir, old_pos):
    if old_dir == 'left':
        new_pos = [old_pos[0], old_pos[1] - 1]
    elif old_dir == 'right':
        new_pos = [old_pos[0], old_pos[1] + 1]
    elif old_dir == 'up':
        new_pos = [old_pos[0] - 1, old_pos[1]]
    else:
        new_pos = [old_pos[0] + 1, old_pos[1]]
    return new_pos


class Beam():
    def __init__(self, start_pos, start_dir, mirrors):#, beam_visits, beam_directions):
        self.start_pos = start_pos
        self.start_dir = start_dir
        self.terminated = False # 'not_started', 'split???', 'terminated'
        self.trajectory = [start_pos]
        self.directions = [start_dir]
        self.children = []
        self.mirrors = mirrors
        #self.visits = beam_visits
        #self.visit = beam_directions
                #if self.status == 'not_started':
        #    self.evolve()


    def evolve(self):
        j = 0
        while (not self.terminated) and (j<20):
            self.take_step()
            print(j)
            j += 1
        print('EVOLVED')
        self.trajectory = self.trajectory#[1:] #look out. to remove first out of grid pos. will it fly for child beams
        self.directions = self.directions#[1:]
        return self.children, self.terminated


    def take_step(self):
        old_pos = self.trajectory[-1]
        old_dir = self.directions[-1]
        self.mirrors.visits[old_pos[0], old_pos[1]] = '#'
        self.mirrors.directions[old_dir][old_pos[0], old_pos[1]] = True

        new_pos = step(old_dir, old_pos)
#        if old_dir == 'left':
#            new_pos = [old_pos[0], old_pos[1] - 1]
#        elif old_dir == 'right':
#            new_pos = [old_pos[0], old_pos[1] + 1]
#        elif old_dir == 'up':
#            new_pos = [old_pos[0] - 1, old_pos[1]]
#        else:
#            new_pos = [old_pos[0] + 1, old_pos[1]]
        #print(new_pos)
        escape = (
                (min(new_pos) == -1) or
                (new_pos[0] == self.mirrors.mirrors.shape[0]) or
                (new_pos[1] == self.mirrors.mirrors.shape[1])
                )
        
        if escape:
            print(f'escaped at {new_pos}')
            self.terminated = True
        else:
            mirror = self.mirrors.mirrors[new_pos[0], new_pos[1]]
            new_dir = self.mirrors.reflections[mirror][old_dir]
            loop = (
                self.mirrors.visits[new_pos[0], new_pos[1]] == '#' and
                self.mirrors.directions[new_dir][new_pos[0], new_pos[1]] == True
            )
            print('====')
            print(self.mirrors.visits[new_pos[0], new_pos[1]])
            print(self.mirrors.directions[new_dir][new_pos[0], new_pos[1]])
            print('====')
            if loop:
                print('FOUND LOOP')
            else:
                print('NO LOOP')
            split = (new_dir == 'split')

            if loop:
                self.terminated = True
                print(f'loop at {new_pos} / {new_dir}')

            elif split:
                print(f'split at {new_pos} / {new_dir}')
                self.terminated = True
                self.mirrors.directions[new_dir][new_pos[0], new_pos[1]] = True

                if old_dir in ['left', 'right']:
                    new_dirs = ['down', 'up']
                else:
                    new_dirs = ['left', 'right']
                for new_dir in new_dirs:
                    self.children.append([new_pos, new_dir])
            else:
                print(f'taking standard step to {new_pos} / {new_dir}')
                self.directions.append(new_dir)
                self.trajectory.append(new_pos)

#    def print_visits(self):
#            for visit_row in self.visits:
#                print(''.join([v for v in visit_row]))

mirrors = Mirrors(data)
if file_name == 'test1.txt':
    mirrors.do([0,-1], 'right')
else:
    mirrors.do([0,-1], 'right')

print(f'Ans1: {mirrors.ans1()} - 7046 is the right answer')

'''
Det här ska inte vara så svårt. Jag måste lösa att starta en beam 
utifrån och kunna hantera att det första som händer är split. 
Det enklaste är nog att 
1) Lyft upp reflections till mirrors. Den passar ändå bättre där. 
2. Gör ett litet fulhack för att hantera split i do()
'''

n_rows, n_cols = mirrors.mirrors.shape

best = 0
for row in range(n_rows):
    print(f'row {row}/{n_rows}')
    mirrors = Mirrors(data)
    mirrors.do([row,-1], 'right')
    best = max((best, mirrors.ans1()))
    mirrors = Mirrors(data)
    mirrors.do([row,n_cols], 'left')
    best = max((best, mirrors.ans1()))
    
for col in range(n_cols):
    print(f'col {col}/{n_cols}')

    mirrors = Mirrors(data)
    mirrors.do([-1,col], 'down')
    best = max((best, mirrors.ans1()))
    mirrors = Mirrors(data)
    mirrors.do([n_rows, col], 'up')
    best = max((best, mirrors.ans1()))

print(f'Ans2: {best} 7313 is right')


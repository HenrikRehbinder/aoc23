import sys
sys.path.append('..')
from utils.imports import *
file = 'test1.txt'
with open(file) as file:
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
            'down': np.array([[False for d in dat] for dat in data])
            }
        self.beams = []
    

    def add_beam(self, start_pos, start_dir):
        beam = Beam(
            start_pos, start_dir, self#.mirrors, self.beam_visits, self.beam_directions
            )
        self.beams.append(beam)


    def do(self, start_pos, start_dir):
        self.add_beam(start_pos, start_dir)
        done = False
#        while (not done) and (len(self.beams)<10):
        #i = 0
        while not done: 
            #i<10:
            #print(i)
            #print(len(self.beams))
            print('----')
            #done = True
            nsb = []
            for j, b in enumerate(self.beams):
                if b.status == 'not_started':
                    nsb.append(j)
            print(nsb)
            if len(nsb)==0:
                done = True
            else:
                beam = self.beams[nsb[0]]
                print('hello')
                print(beam)
#            non_started_beams = [i for i,b in enumerateself.beams[i]
            #for beam in self.beams:
                beam_splits, status = beam.evolve()
                #self.visits = beam_visits
                #self.beam_directions = beam_directions
                print(status)
                #print(self.beam_visits)
                for beam_split in beam_splits:
                    #Kolla om den är i en loop. Eller kollar man det innan man skapar childrn. 
                    self.add_beam(beam_split[0], beam_split[1])
            #    i += 1

               # print(('len(self.beams)', len(self.beams))


       # self.beam_visits = beam.visits
       # print(beam.visits)
       # self.beam_directions = beam.visit_directions#

#        while not beam.status == 'terminated':
#            for child in beam.children:
#                self.add_beam(child.start_pos, child.start_dir)



class Beam():
    def __init__(self, start_pos, start_dir, mirrors):#, beam_visits, beam_directions):
        self.start_pos = start_pos
        self.start_dir = start_dir
        self.status = 'not_started' # 'not_started', 'split???', 'terminated'
        self.trajectory = [start_pos]
        self.directions = [start_dir]
        self.children = []
        self.mirrors = mirrors
        #self.visits = beam_visits
        #self.visit = beam_directions
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
        #if self.status == 'not_started':
        #    self.evolve()

    def evolve(self):
        while (self.status != 'terminated'):
            self.take_step()
        self.trajectory = self.trajectory#[1:] #look out. to remove first out of grid pos. will it fly for child beams
        self.directions = self.directions#[1:]
        return self.children, self.status

    def take_step(self):
        # position
        #print(('from', self.trajectory[-1]))
        old_direc = self.directions[-1]
        #print(('dir', direc))
        old_pos = self.trajectory[-1]
        self.mirrors.visits[old_pos[0], old_pos[1]] = '#'
 
        if old_direc == 'left':
            new_pos = [old_pos[0], old_pos[1] - 1]
        elif old_direc == 'right':
            new_pos = [old_pos[0], old_pos[1] + 1]
        elif old_direc == 'up':
            new_pos = [old_pos[0] - 1, old_pos[1]]
        else:
            new_pos = [old_pos[0] + 1, old_pos[1]]
        print(new_pos)
        escape = (
                (min(new_pos) == -1) or
                (new_pos[0] == self.mirrors.mirrors.shape[0]) or
                (new_pos[1] == self.mirrors.mirrors.shape[1])
                )
        if escape:
            self.status = 'terminated'
        else:

        #direction
            mirror = self.mirrors.mirrors[new_pos[0], new_pos[1]]
        #print(mirror)
        #print(new_pos)
            new_dir = self.reflections[mirror][old_direc]
        #print(('new_pos',new_pos))
        #print(min(new_pos))
        #TODO: lösing på gång. Kolla ny(a) rikting(ar) här.
            is_split = (new_dir == 'split')
            if is_split:
                if old_direc in ['left', 'right']:
                    new_dirs = ['down', 'up']
                else:
                    new_dirs = ['left', 'right']
            else:
                new_dirs = [new_dir]

            for new_dir in new_dirs:
                loop = (
                    self.mirrors.visits[new_pos[0], new_pos[1]] == '#' and
                    self.mirrors.directions[new_dir][new_pos[0], new_pos[1]] is True
                )
                if not loop:
                    if is_split:
                        #self.mirrors.visits[new_pos[0], new_pos[1]] = '#'
                        self.children.append([new_pos, new_dir])
                        self.status = 'terminated'
                    else:
                        #self.mirrors.visits[new_pos[0], new_pos[1]] = '#'
                        self.mirrors.directions[old_direc][new_pos[0], new_pos[1]] = True
                        self.directions.append(new_dir)
                        self.trajectory.append(new_pos)
                else:
                    self.status = 'terminated'

#    def print_visits(self):
#            for visit_row in self.visits:
#                print(''.join([v for v in visit_row]))

mirrors = Mirrors(data)
mirrors.do([0,0], 'right')

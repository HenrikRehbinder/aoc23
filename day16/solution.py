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
        self.beam_visits = np.array([['.' for d in dat] for dat in data])
        self.beam_directions = {
            [0, -1]: np.array([[False for d in dat] for dat in data]),
            [0, 1]: np.array([[False for d in dat] for dat in data]),
            [-1, 0]: np.array([[False for d in dat] for dat in data]),
            [1, 0]: np.array([[False for d in dat] for dat in data])
            }
        self.beams = []
    

    def add_beam(self, start_pos, start_dir):
        beam = Beam(
            start_pos, start_dir, self.mirrors, self.beam_visits, self.beam_directions
            )
        self.beams.append(beam)
        self.beam_visits = beam.visits
        self.beam_directions = beam.visit_directions
        while not beam.status == 'terminated':
            for child in beam.children:
                self.add_beam(child.start_pos, child.start_dir)



class Beam():
    def __init__(self, start_pos, start_dir, mirrors, beam_visits, beam_directions):
        self.start_pos = start_pos
        self.start_dir = start_dir
        self.status = 'not_started' # 'not_started', 'split', 'terminated'
        self.trajectory = [start_pos]
        self.directions = [start_dir]
        self.children = []
        self.mirrors = mirrors
        self.visits = beam_visits
        self.visit_directions = beam_directions
        #if self.status == 'not_started':
        #    self.evolve()
    '''
Halli hallå, en beam kan ju gå in i en loop. Det är ett avbrottsvillkor som saknas. Om man är i en pos 
som man redan varit i med samma riktning som förra gången så är man fast. Problemet är att även barn/föräldrar liksom interagerar. Man skulle behöva hålla reda på vilka positioner som besökts och i vilka riktningar. Ett litet problem är att alla beams evolverar parallellt. Det räcker inte att hålla koll på 
barn-föräldrar. Hela släkten hänger ihop. 
Ska man kanske ha en klass Mirrors som har alla beams och var de har varit. 
'''


    def evolve(self):
        while (self.status != 'terminated') and (self.status != 'split'):
            self.take_step()
        self.trajectory = self.trajectory[1:] #look out. to remove first out of grid pos. will it fly for child beams
        self.directions = self.directions[1:]
   
    def take_step(self):
        # position
        print(('from', self.trajectory[-1]))
        dir = self.directions[-1]
        print(('dir', dir))
        new_pos = list(np.array(self.trajectory[-1]) + np.array(dir))
        print(('new_pos',new_pos))
        #print(min(new_pos))
        if (
            (min(new_pos) == -1) or
            new_pos[0] == self.mirrors.shape[0] or
            new_pos[1] == self.mirrors.shape[1]
            ):
            #print(new_pos)
            print('escaped')
            self.status = 'terminated'
        elif (
            self.visits[new_pos[0], new_pos[1]] == '#' and 
            self.visit_directions[dir][new_pos[0], new_pos[1]] == True
            ):
            print('terminated_loop')
            self.status = 'terminated'
        else:
            self.visits[new_pos[0], new_pos[1]] = '#'
            self.visit_directions[dir][new_pos[0], new_pos[1]] = True
            self.trajectory.append(new_pos)

            #direction
            mirror = self.mirrors[new_pos[0], new_pos[1]]
            #print(mirror)
            #print(new_pos)
            if dir[0] == 0:
                dir_type = 'hori'
            else:
                dir_type = 'vert'
           
            if (mirror == '.' or 
                (dir_type=='hori' and mirror=='-') or 
                (dir_type=='vert' and mirror=='|')):
                print(mirror)
                print(dir)
                self.directions.append(dir)
            elif mirror == '/':
                print(('reflection:', mirror))
                self.directions.append([-dir[1], -dir[0]])
            elif mirror == '\\':
                print(('reflection:', mirror))
                self.directions.append([ dir[1],  dir[0]])
            elif (
                dir_type=='hori' and mirror=='|'
                ) or (
                dir_type=='vert' and mirror=='-'
                ):
                self.directions.append(dir)
                
                if dir_type == 'hori':
                    new_dir_1 = [-1, 0]
                    new_dir_2 = [1, 0]
                if dir_type == 'vert':
                    new_dir_1 = [0, -1]
                    new_dir_2 = [0, 1]
                print('split')
                self.status = 'split'
                self.children.append([new_pos, new_dir_1])
                self.children.append([new_pos, new_dir_2])
            

#beam = Beam([0, -1], [0, 1], data)


import sys
sys.path.append('..')
from utils.imports import *
file = 'test1.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]


# expand universe
dots = ''.join(['.' for i in range(len(data[0]))])
exp_data = []
for i, d in enumerate(data):
    exp_data.append(d)
    if d == dots:
        exp_data.append(d)


# find # positions.
def find_stars(d):
    if d.find('#') != -1:
        return [m.start() for m in re.finditer('#', d)]
    else:
        return None


stars = []
for row, d in enumerate(exp_data):
#    print(d)
    cols = find_stars(d)
    if cols != None:
        for col in cols:
            stars.append([row, col])
#    print(cols)
måste expandera rader också. 

def distance(star_1, star_2):
    # inte verifierad, 1an är adhoc
    return(abs(star_1[0] - star_2[0]) + abs(star_1[1] - star_2[1])+1)


print(distance(stars[0], stars[6]))
print(distance(stars[2], stars[5]))
print(distance(stars[7], stars[8]))

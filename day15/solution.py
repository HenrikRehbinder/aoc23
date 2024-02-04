import sys
sys.path.append('..')
from utils.imports import *
file = 'input.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]


data = data[0].split(',')

#etermine the ASCII code for the current character of the string.
#Increase the current value by the ASCII code you just determined.
#Set the current value to itself multiplied by 17.
#Set the current value to the remainder of dividing itself by 256.

def increment(cur_val, ch):
    #a = ord(ch)
    #cur_val += a
    #cur_val *= 17
    #cur_val = ((cur_val+ord(ch))*17)%256
    return ((cur_val+ord(ch))*17)%256

def hash(str):
    cur_val = 0
    for s in str:
        cur_val = ((cur_val+ord(s))*17)%256
    return cur_val

ans1 = 0
for d in data:
    ans1 += hash(d)

print(f'Ans1: {ans1}')
print('Correct: 494980')


optic = {}


def modify_optics(optic, d):
    if d[-1] == '-':
        remove = True
        label = d[:-1]
    else:
        remove = False
        label = d[:-2]
        focal_length = int(d[-1])
    box = hash(label)
    if remove:
        if box in optic.keys():
            lens_labels = optic[box]['labels']
            focal_lengths = optic[box]['focal_lengths']
            if label in lens_labels:
                ind = lens_labels.index(label)
                lens_labels.pop(ind)
                focal_lengths.pop(ind)
            if lens_labels == []:
                optic.pop(box, None)
            else:
                optic[box]['labels'] = lens_labels
                optic[box]['focal_lengths'] = focal_lengths
    else:
        if box not in optic.keys():
            optic[box] = {
                'labels': [label],
                'focal_lengths': [focal_length]
                }
        else:
            if label in optic[box]['labels']:
                ind = optic[box]['labels'].index(label)
                optic[box]['focal_lengths'][ind] = focal_length
            else:
                optic[box]['labels']  = optic[box]['labels'] + [label]
                optic[box]['focal_lengths']  = optic[box]['focal_lengths'] + [focal_length]
    return optic

for d in data:
    optic = modify_optics(optic, d)

ans2 = 0
for box, lenses in optic.items():
    #print(box)
    i = 0
    for l, fl in zip(lenses['labels'], lenses['focal_lengths']):
        #print((l, fl))
        #print((box, i, fl, (box+1)*(i+1)*fl))
        ans2 += (box+1)*(i+1)*fl
        i = i+1

print(f'Ans2: {ans2}')
print('Correct: 247933')

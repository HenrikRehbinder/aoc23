from utils.imports import *
#file = 'test1.txt'
file = 'input.txt'

with open(file) as file:
    data = [s.strip() for s in file.readlines()]

for i, d in enumerate(data):
    data[i] = [int(di) for di in d.split(' ')]


def find_next(d):
    red_arr = d
    seq = [d]
    first_seq = 0
    first = 0
    next = d[-1]
    done = False
    while not done:
        red_arr = [red_arr[i+1] - red_arr[i] for i in range(len(red_arr)-1)]
        seq.append(red_arr)
        if all([r == 0 for r in red_arr]):
            done = True
        next += red_arr[-1]
    app_seq = seq
    for i in range(len(seq)):
        j = len(seq)-1-i
        app_seq[j] = [-first_seq + app_seq[j][0]] + app_seq[j]
        first_seq = app_seq[j][0]
        #first += first_seq
    first = app_seq[0][0]
    return next, first, seq, app_seq

nexts = []
firsts = []
seqs = []
app_seqs = []
for i, d in enumerate(data):
    n, f, s, a_s = find_next(d)
    nexts.append(n)
    seqs.append(s)
    firsts.append(f)
    app_seqs.append(a_s)

print(f'Answ 1: {sum([m for m in nexts])}')
print('Answ: 1702218515 is correct!')

print(f'Answ 2: {sum([ff for ff in firsts])}')

if False:
    for i, s in enumerate(app_seqs):
        print(i)
        for ss in s:
            print(ss)
        print(f'next: {nexts[i]}')
        print(f'first: {firsts[i]}')


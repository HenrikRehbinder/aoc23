from utils.imports import *
#file = 'test1.txt'
file = 'input.txt'

with open(file) as file:
    data = [s.strip() for s in file.readlines()]

for i, d in enumerate(data):
    data[i] = [int(di) for di in d.split(' ')]


def find_next(d):
    #print('***')
    #print(d)
    red_arr = d
    #next = d[-1]
#    while np.abs(red_arr).sum() > 0:
    add = 0
    done = False
    #print(red_arr)
    while not done:
        red_arr = [red_arr[i+1] - red_arr[i] for i in range(len(red_arr)-1)]
      #  print(red_arr)
        if len(red_arr) == 1:
            done = True
            print('what?')
            print(red_arr)
            why = 'end'
        else:
            if red_arr[-1] == 0:
            #if all([ra == 0 for ra in red_arr]):
                done = True
                why = '0'
        add += red_arr[-1]
     #   print(add)
    #print(f'd[-1] {d[-1]}')
    #print(f'add {add}')
    return d[-1] + add, why


def find_seq(d):
    #print('***')
    #print(d)
    seq = [d]
    #red_arr = d
    #next = d[-1]
#    while np.abs(red_arr).sum() > 0:
    add = 0
    done = False
    #print(red_arr)
    while not done:
        last = seq[-1]
        red_arr = [last[i+1] - last[i] for i in range(len(last)-1)]
        seq.append(red_arr)
        #print(red_arr)
        if len(red_arr) == 0:
            done = True
        else:
            if all([ra == 0 for ra in red_arr]):
                done = True
    return seq, len(red_arr)


nexts = []
problems = []
for i, d in enumerate(data):
    n = nexts.append(find_next(d))
    if n == -1:
        problems.append(i)
    else:
        nexts.append((i, n))
seqs = []
prob = []
for i, d in enumerate(data):
    seq, n = find_seq(d)
    seqs.append((i, seq, n))
    print((i, n))
    if n == 0:
        prob.append((i,n))

nexts = [find_next(d)[0] for d in data]
whys = [find_next(d)[1] for d in data]

print(f'Answ: {sum([m for m in nexts])}')
print('2588581978 is too high')
print('2357498856 is too high')



d = data[118]
f, a = plt.subplots(1, num=1, clear=True)
n = find_next(d)
plt.plot(range(len(d)), d,'o')
plt.plot([len(d) + 1], [n], '*')


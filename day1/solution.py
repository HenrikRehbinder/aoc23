from utils.imports import *
file = 'input.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]


def replace_strings(d):
    i_s = {
        0: ['zero'],
        1: ['one'],
        2: ['two'],
        3: ['three'],
        4: ['four'],
        5: ['five'],
        6: ['six'],
        7: ['seven'],
        8: ['eight'],
        9: ['nine'],
    }
    int_ind = [[], [], [], [], [], [], [], [], [], []]
    for key, val in i_s.items():
        ind1 = [i for i in range(len(d)) if d.startswith(val[0], i)]
        if len(ind1) > -1:
            int_ind[key]= ind1


    dd = d
    for i, ii in enumerate(int_ind):
         if not (ii == []):
            for ind in ii:
                dd = dd[:ind] + str(i) + dd[ind+1:]
    return dd


second = True
if second:
    new_data = [replace_strings(d) for d in data]
else:
    new_data = data


def find_ints(data):
    cal_nums = [[s for s in d if s.isnumeric()] for d in data]
    cals = [int(c[0]+c[-1]) for c in cal_nums]
    return cals


cals = find_ints(new_data)
answer = sum(cals)
print(answer)



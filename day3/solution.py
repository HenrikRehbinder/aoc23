import numpy as np
import itertools as iter
from utils.imports import *
file = 'input.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]

short = 40
if short > 0:
    nd = []
    for d in data[:short]:
        nd.append(d[:short])
    data = nd

class Mask():
    def __init__(self, data):
        self.data = data
        self.mask = np.zeros((len(data), len(data[0])))
        self.symbol_str  = ''

    def find_symbols(self):
        datastr = ''
        for d in self.data:
            datastr = datastr + d
        symbols = datastr
        for i in range(10):
            symbols = symbols.replace(str(i), '')
        symbols = symbols.replace('.', '')
        symbol_str = ''.join(set(symbols))
        return symbol_str


# find symbols
def find_symbols(data):
    datastr = ''
    for d in data:
        datastr = datastr + d
    symbols = datastr
    for i in range(10):
        symbols = symbols.replace(str(i), '')
    symbols = symbols.replace('.', '')
    symbols = list(set(symbols))
    return symbols


symbols = find_symbols(data)

def multi_split(s, delimiters):
    string = s
    for delimiter in delimiters:
        string = " ".join(string.split(delimiter))
    return string.split()

nums = [multi_split(d, symbols+['.']) for d in data]
symbol_str = ''
for s in symbols:
    symbol_str += s
#syms = [[s for s in d if s in symbol_str] for d in data]

# find symbol indices
sym_ind = []
for i, d in enumerate(data):
    si = []
    for j, s in enumerate(d):
        if s in symbol_str:
            si.append((i,j))
    if not(si == []):
        sym_ind.append(si)
sym_ind = [sii for si in sym_ind for sii in si]
# make mask


def make_mask(sym_ind, data):
    mask = np.zeros((len(data), len(data[0])))
    n_r, n_c = mask.shape
    for si in sym_ind:
        for d_r, d_c in iter.product([-1, 0, 1],[-1, 0, 1]):
            ind_r = si[0] + d_r
            ind_c = si[1] + d_c
            if (ind_r < 0) or (ind_r > n_r - 1):
                print('*')
                print(ind_r)
                print(si)
                ind_r = si[0]
            if (ind_c < 0) or (ind_c > n_c - 1):
                print('*')
                print(ind_c)
                print(si)
                ind_c = si[1]
            mask[ind_r][ind_c] = 1
    return mask


mask = make_mask(sym_ind, data)


def find_valid_numbers(num, d, m):
    found_n = []
    old_nu = ''
    j = 0
    J = 0
    for i, nu in enumerate([str(nn) for nn in np.sort([int(n) for n in num])]):
        if nu == old_nu:
            offset = J
            print(nu)
        else:
            offset = 0
        print((nu, old_nu, offset))
        #d = d[offset:]
        j = d.find(nu, offset)
        J = j + len(nu)
        # print((d[j:J], nu))
        print((nu, m[j:J]))
        if sum(m[j:J]) > 0:
            print((nu, row, offset, j, J))
            found_n.append(int(nu))
        old_nu = nu
    return found_n

nn = []
for row, num in enumerate(nums):
    d = data[row]
    m = mask[row]
    vn = find_valid_numbers(num, d, m)
    print(row, vn)
    nn = nn+vn
print(sum(nn))

# [print(d.replace('.', 'o')) for d in data]
str_m = []
for mm in mask:
     s = ''
     for mmm in mm:
         s += str(int(mmm))
     str_m.append(s)
#
# for d, m in zip(data, str_m):
#     print(d.replace('.', 'o') + ' ' + m)


with open('inputshort.txt', 'w') as f:
    for line in data:
        f.write(f"{line}\n")

with open('mask.txt', 'w') as f:
    for m, d in zip(str_m, data):
        f.write(f"{m} {d}\n")

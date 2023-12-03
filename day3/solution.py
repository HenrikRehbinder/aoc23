import numpy as np
import itertools as iter
from utils.imports import *
file = ('input.txt')
with open(file) as file:
    data = [s.strip() for s in file.readlines()]

short = 0
if short > 0:
    nd = []
    for d in data[:short]:
        nd.append(d[:short])
    data = nd


class Mask():
    def __init__(self, data):
        self.data = data
        self.symbol_str = ''
        self.mask = np.zeros((len(self.data), len(self.data[0]))).astype(int)

    def find_symbols(self):
        datastr = ''
        for d in self.data:
            datastr = datastr + d
        symbols = datastr
        for i in range(10):
            symbols = symbols.replace(str(i), '')
        symbols = symbols.replace('.', '')
        self.symbol_str = ''.join(set(symbols))

    def make_mask(self):
        sym_ind = []
        for row, d in enumerate(data):
            for col, s in enumerate(d):
                if s in self.symbol_str:
                    sym_ind.append((row, col))

        n_r, n_c = self.mask.shape
        for si in sym_ind:
            for d_r, d_c in iter.product([-1, 0, 1], [-1, 0, 1]):
                ind_r = si[0] + d_r
                ind_c = si[1] + d_c
                if (ind_r < 0) or (ind_r > n_r - 1):
                    ind_r = si[0]
                if (ind_c < 0) or (ind_c > n_c - 1):
                    ind_c = si[1]
                self.mask[ind_r][ind_c] = 1

    def find_stars(self):
        stars = []
        for d in self.data:
            npd = np.array([dd for dd in d])
            star_ind = np.where(npd == '*')[0]
            stars.append(list(star_ind))
        return stars



    def get_mask(self):
        return self.mask

    def get_symbols(self):
        return self.symbol_str

    def print_mask(self, row=None):
        if row:
            M = [self.mask[row]]
        else:
            M = self.mask
        M = M.astype(str)
        for m in M:
            print(''.join(m))



class Numbers:
    def __init__(self, data):
        self.data = data
        self.numbers = []
        self.valid_numbers = []
        self.invalid_numbers = []

    def find_numbers_o(self, symbols):
        def multi_split(s, delimiters):
            string = s
            for delimiter in delimiters:
                string = " ".join(string.split(delimiter))
            return string.split()

        self.numbers = [multi_split(d, symbols + '.') for d in self.data]

    def find_numbers(self):
        found_nums = []
        for row, d in enumerate(data):
           # print(row)
            nums_row = self.find_row_numbers(d)
            found_nums.append(nums_row)
        self.numbers = found_nums

    def find_row_numbers(self, d):
        i = 0
        nums_row = []
        while i < len(d):
            if d[i].isnumeric():
                #print(f'i: {i}')
                eow = False
                j = i + 1
                while not eow:
                    #print((i, j))
                    eow = True
                    if j < len(d):
                       if d[j].isnumeric():
                           j = j + 1
                           eow = False
                    #print((i, j))
                nums_row.append((d[i:min(j, len(d))], i, j))
                i = j+1
            else:
                i = i + 1
        return nums_row

    def find_star_nums(self, star):
        star_row, star_col = star
        adj_nums = []
        print(f'star {(star_row, star_col)}')
        print(max(star_row - 1, 0), min(star_row + 1, len(self.numbers) - 1))
        for row in range(max(star_row-1, 0), 1+min(star_row+1, len(self.numbers)-1)):
            num_row = self.numbers[row]
            print(f'row{row}')
            for num in num_row:
                print(num)
                if self.adjacent(num, row, star_row, star_col):
                    adj_nums.append(num[0])
        return adj_nums

    def adjacent(self, num, row, r, c):
        print((num, row, r, c))
        distances = [(r-row)**2 + (c-cc)**2 for cc in range(num[1], num[2])]
        return min(distances) <= 2.01



    def get_numbers(self):
        return self.numbers

    def find_valid_numbers(self, mask):
        self.valid_numbers = []
        self.invalid_numbers = []

        for num_rows, m in zip(self.numbers, mask):
            for num in num_rows:
                if sum(m[num[1]:num[2]]) > 0:
                    self.valid_numbers.append(num[0])
                else:
                    self.invalid_numbers.append(num[0])

    def get_valid_numbers(self):
        return self.valid_numbers

    def get_answer(self):
        a = 0
        for num in self.valid_numbers:
            a += int(num)
        return a

mask = Mask(data)

mask.find_symbols()
mask.make_mask()
the_mask = mask.get_mask()

symbols = mask.get_symbols()

numbers = Numbers(data)
numbers.find_numbers()
numbers.find_valid_numbers(the_mask)
n = numbers.get_valid_numbers()

print(numbers.get_answer())

stars = mask.find_stars()

star_nums = []
for row, star in enumerate(stars):
    #print(f'row {row}')
    #print(star)
    if star != []:
        star_nums.append(numbers.find_star_nums((row, star[0])))
print(star_nums)
ans = 0
for sn in star_nums:
    if len(sn) == 2:
        ans += int(sn[0])*int(sn[1])
print(f'ans2: {ans}')


# def find_numbers(data, symbols):
#     def multi_split(s, delimiters):
#         string = s
#         for delimiter in delimiters:
#             string = " ".join(string.split(delimiter))
#         return string.split()
#
#     return [multi_split(d, symbols+'.') for d in data]
#
# numbers = find_numbers(data, symbols)


#
#
# def find_valid_numbers(num, d, m):
#     found_n = []
#     old_nu = ''
#     j = 0
#     J = 0
#     for i, nu in enumerate([str(nn) for nn in np.sort([int(n) for n in num])]):
#         if nu == old_nu:
#             offset = J
#             print(nu)
#         else:
#             offset = 0
#         print((nu, old_nu, offset))
#         #d = d[offset:]
#         j = d.find(nu, offset)
#         J = j + len(nu)
#         # print((d[j:J], nu))
#         print((nu, m[j:J]))
#         if sum(m[j:J]) > 0:
#             print((nu, row, offset, j, J))
#             found_n.append(int(nu))
#         old_nu = nu
#     return found_n
#
# nn = []
# for row, num in enumerate(nums):
#     d = data[row]
#     m = mask[row]
#     vn = find_valid_numbers(num, d, m)
#     print(row, vn)
#     nn = nn+vn
# print(sum(nn))
#
# # [print(d.replace('.', 'o')) for d in data]
str_m = []
for mm in the_mask:
     s = ''
     for mmm in mm:
         s += str(int(mmm))
     str_m.append(s)
# #
# # for d, m in zip(data, str_m):
# #     print(d.replace('.', 'o') + ' ' + m)
#
#
# with open('inputshort.txt', 'w') as f:
#     for line in data:
#         f.write(f"{line}\n")
#

with open('mask.txt', 'w') as f:
     for m, d in zip(str_m, data):
         f.write(f"{m} {d}\n")



# # symbol_str = ''
# # for s in symbols:
# #     symbol_str += s
# # #syms = [[s for s in d if s in symbol_str] for d in data]
# #
# # # find symbol indices
# # sym_ind = []
# # for i, d in enumerate(data):
# #     si = []
# #     for j, s in enumerate(d):
# #         if s in symbol_str:
# #             si.append((i,j))
# #     if not(si == []):
# #         sym_ind.append(si)
# # sym_ind = [sii for si in sym_ind for sii in si]
# # # make mask
#
#
# # def make_mask(sym_ind, data):
# #     mask = np.zeros((len(data), len(data[0])))
# #     n_r, n_c = mask.shape
# #     for si in sym_ind:
# #         for d_r, d_c in iter.product([-1, 0, 1],[-1, 0, 1]):
# #             ind_r = si[0] + d_r
# #             ind_c = si[1] + d_c
# #             if (ind_r < 0) or (ind_r > n_r - 1):
# #                 print('*')
# #                 print(ind_r)
# #                 print(si)
# #                 ind_r = si[0]
# #             if (ind_c < 0) or (ind_c > n_c - 1):
# #                 print('*')
# #                 print(ind_c)
# #                 print(si)
# #                 ind_c = si[1]
# #             mask[ind_r][ind_c] = 1
# #     return mask
#
#
#
#
# # find symbols
# # def find_symbols(data):
# #     datastr = ''
# #     for d in data:
# #         datastr = datastr + d
# #     symbols = datastr
# #     for i in range(10):
# #         symbols = symbols.replace(str(i), '')
# #     symbols = symbols.replace('.', '')
# #     symbols = list(set(symbols))
# #     return symbols

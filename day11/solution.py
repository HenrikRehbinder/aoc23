import sys
#sys.path.append('..')
from utils.imports import *
file = 'input.txt'
with open(file) as file:
    data_org = [s.strip() for s in file.readlines()]

data = [[ddd for ddd in dd] for dd in data_org]

n_rows = len(data)
n_cols = len(data[0])

stars = np.argwhere(np.array(data) == '#')

star_rows = sorted(list(set(stars[:, 0])))
star_cols = sorted(list(set(stars[:, 1])))

non_star_rows = [row for row in range(n_rows) if not (row in star_rows)]
non_star_cols = [col for col in range(n_cols) if not (col in star_cols)]


def distance2(star_1, star_2, n, non_star_rows, non_star_cols):
    def ax_dist(star_1, star_2, axis, non):
        a_start = min((star_1[axis], star_2[axis]))
        a_end = max((star_1[axis], star_2[axis]))
        a_dist = 0
        for ind in range(a_start + 1, a_end + 1):
            if ind in non:
                a_dist += n
            else:
                a_dist += 1
        return a_dist

    return (
            ax_dist(star_1, star_2, axis=0, non=non_star_rows) +
            ax_dist(star_1, star_2, axis=1, non=non_star_cols)
    )


print((distance2((5,1), (9, 4), n=2, non_star_rows=non_star_rows, non_star_cols=non_star_cols), 9))
print((distance2((9, 0), (9, 4), n=2, non_star_rows=non_star_rows, non_star_cols=non_star_cols), 5))


def acc_distances(stars, n, non_star_rows, non_star_cols):
    dists = []
    for i in range(len(stars)-1):
        for j in range(len(stars)-i-1):
            dists.append(distance2(
                stars[i], stars[j+i+1], n=n, non_star_rows=non_star_rows, non_star_cols=non_star_cols)
            )
    return sum(dists)


print(f'Answ1: {acc_distances(stars, 2, non_star_rows, non_star_cols)}, (9627977 is correct)')
print(f'Answ2: {acc_distances(stars, 1000000, non_star_rows, non_star_cols)}, (644248339497 is correct)')

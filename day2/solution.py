from utils.imports import *
file = ('input.txt')
with open(file) as file:
    data = [s.strip() for s in file.readlines()]


def find_color_vals(draw):
    dr = []
    for ch in ['red', 'green', 'blue']:
        ind = draw.find(ch)
        if ind == -1:
            dr.append(0)
        else:
            dr.append(int(draw.split(ch)[0].split(',')[-1]))
    return dr


def find_colors(d):
    game, draws = d.split(':')
    draws = draws.replace(' ', '').split(';')
    draws_cleaned = [find_color_vals(dr) for dr in draws]
    return draws_cleaned


cleaned_draws = [find_colors(d) for d in data]
maxs = np.array([12, 13, 14])
correct_games = 0
for i, c in enumerate(cleaned_draws):
    if np.sum(np.array(c) > maxs) == 0:
        print(i)
        correct_games += i+1

print(f'Task 1: {correct_games}')

power_sum = 0
for cd in cleaned_draws:
    power_sum += np.prod(np.max(cd, axis=0))

print(f'Task 2: {power_sum}')

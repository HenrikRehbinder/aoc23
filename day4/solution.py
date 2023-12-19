from utils.imports import *
import re

file = 'input.txt'
with open(file) as file:
    data = [s.strip() for s in file.readlines()]

win_num = []
my_num = []
for d in data:
    wi, my = d.split(': ')[-1].split('|')
    wi = [int(w) for w in re.findall(r'\d+', wi)]
    my = [int(m) for m in re.findall(r'\d+', my)]
    win_num.append(wi)
    my_num.append(my)


def find_wins_and_score(win_nums, my_nums):
    wins = [m for m in my_nums if m in win_nums]
    if len(wins) > 0:
        score = np.power(2, len(wins)-1)
    else:
        score = 0
    num_wins = len(wins)
    return wins, score, num_wins


score = 0
card_scores = []
num_of_wins = []
for wn, mn in zip(win_num, my_num):
    w, s, nw = find_wins_and_score(wn, mn)
    card_scores.append(s)
    num_of_wins.append(nw)
    score += s
print(score)

# Part 2

cards = np.ones((len(data), 1))

nc = np.zeros(cards.shape)
for card_num in range(len(cards)):
    new_cards = nc.copy()
    new_cards[:][card_num+1:card_num+1+num_of_wins[card_num]] = cards[card_num]
    cards = cards + new_cards

print(f'Score 2: {int(np.sum(cards))}')

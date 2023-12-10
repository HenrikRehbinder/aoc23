from utils.imports import *
file = 'test1.txt'
#file = 'input.txt'

with open(file) as file:
    data = [s.strip() for s in file.readlines()]

# varje hand ska få ett hand_strength-värde, sen en sekvens av card_strengths
# Kanske göra en klass Hand som kan svara på hand_1.is_stronger_than(hand_2)
# Vid konstruktion tar man reda på handtype (full house etc).

card_order = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
card_order = np.array(list(reversed(card_order)))

hand, bid = data[0].split(' ')


def sort_on_first(arr1, arr2):
    idx = np.argsort(arr1)
    return arr1[idx][::-1], arr2[idx][::-1]


def hand_signature(hand):
    card_vals = [np.argwhere(card_order == h)[0][0] for h in hand]
    cards = np.array(list(set(hand)))
    occ = np.array([hand.count(c) for c in cards])
    occ, cards = sort_on_first(occ, cards)
    test = list(occ)
    if test == [5]:
        return 7, '5oak', card_vals
    elif test == [4, 1]:
        return 6, '4oak', card_vals
    elif test == [3, 2]:
        return 5, 'FH', card_vals
    elif test == [3, 1, 1]:
        return 4, '3oak', card_vals
    elif test == [2, 2, 1]:
        return 3, '2P', card_vals
    elif test == [2, 1, 1, 1]:
        return 2, '1P', card_vals
    elif test == [1, 1, 1, 1, 1]:
        return 1, 'HC', card_vals
    else:
        print('Something wrong')
        print(test)
        print(cards)
        print(hand)
        return None, None, None

game = []
for d in data:
    hand, bid = d.split(' ')
    bid = int(bid)
    hand_strength, hand_type, card_vals = hand_signature(hand)
    game.append({
        'hand': hand,
        'bid': bid,
        'str': hand_strength,
        'type': hand_type,
        'cvals': card_vals
    })
hands = np.array([g['hand'] for g in game])
cvals = np.array([g['cvals'] for g in game])
stres = np.array([g['str'] for g in game])
bids = np.array([g['bid'] for g in game])
idx = np.argsort(stres)[::-1]
cvals = cvals[idx]
stres = stres[idx]
bids = bids[idx]
hands = hands[idx]

# Nu behöver jag inte sortera om listan. Det räcker att skapa rank. Sen kan man göra bid*rank.
def is_better_than(vals1, vals2):
    #return 1 if vals1 better than vals2, else 0
    diff = vals1-vals2
    for d in diff:
     #   print(d)
        if d != 0:
            break

    if d > 0:
        return 1
    else:
        return 0


def intragroup_rank(vals):
    mat = np.zeros((len(vals), len(vals)))
    for i, vals1 in enumerate(vals):
        for j, vals2 in enumerate(vals):
            mat[i][j] = is_better_than(vals1, vals2)
    #print(mat)
    return mat.sum(axis=1)


intra_rank = np.ones(stres.shape)
rank_offset = np.zeros(stres.shape)
#ro = 0
sorted_unique_stres = np.sort(np.unique(stres))
ro = len(stres) - np.count_nonzero(stres == sorted_unique_stres[0]) + 1
ra = 1
for stres_group in sorted_unique_stres:
    #print(f'sg {stres_group}')
    #print(f'ro {ro}')
    idx = np.argwhere(stres == stres_group).squeeze()
    if idx.shape != ():
        in_rank = intragroup_rank(cvals[idx])
        intra_rank[idx] = in_rank
        rank_offset[idx] = ro
    else:
        idx = np.array([idx])
        rank_offset[idx] = ro

    ro = ro - len(idx)


for stres

rank = rank_offset + inter_rank

print(rank)
print((rank*bids).sum())


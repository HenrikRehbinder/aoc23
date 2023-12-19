from utils.imports import *
#file = 'test1.txt'
file = 'input.txt'

with open(file) as file:
    data = [s.strip() for s in file.readlines()]

card_order = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
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


def joker_signature(hand):
    # find jokers
    #hand_strength = 0
    hand_strength, hand_type, hand_vals = hand_signature(hand)
    handarr = np.array([s for s in hand])
    jok_i = np.argwhere(handarr == 'J')
    if len(jok_i) > 0:
        #print(f'jok_i: {jok_i}')
        for replacement in it.product(card_order[1:], repeat=len(jok_i)):
            #print(f'replacement {replacement}')
            for i, r in zip(jok_i, replacement):
                handarr[i] = r
            handstr = ''.join([h for h in handarr])
            strength, h_type, vals = hand_signature(handstr)
            if strength > hand_strength:
                hand_strength = strength
                hand_type = h_type
                #hand_vals = vals Här är felet.
    return hand_strength, hand_type, hand_vals


game = []
for d in data:
    hand, bid = d.split(' ')
    bid = int(bid)
    hand_strength, hand_type, card_vals = joker_signature(hand)
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


def is_better_than(vals1, vals2):
    diff = vals1-vals2
    for d in diff:
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
            mat[i][j] = int(is_better_than(vals1, vals2))
    return mat.sum(axis=1)


rank = np.zeros(stres.shape)
sorted_unique_stres = np.sort(np.unique(stres))
ra = 1
for stres_group in sorted_unique_stres:
    idx = np.argwhere(stres == stres_group).squeeze()
    if idx.shape == ():
        idx = np.array([idx])
    in_rank = intragroup_rank(cvals[idx])
    in_rank_idx = np.argsort(in_rank)
    for i in in_rank_idx:
        rank[idx[i]] = ra
        ra = ra + 1


print(f'Ans2: {int((rank*bids).sum())}')



from utils.imports import *
#file = 'test1.txt'
file = 'input.txt'

with open(file) as file:
    data = [s.strip() for s in file.readlines()]

times = [int(t) for t in re.findall(r'\d+', data[0])]
distances = [int(d) for d in re.findall(r'\d+', data[1])]

# Om man håller nere knappen t enheter på ett lopp som är T långt så kommer man
# s = (T-t)*t. T-t är kvarvarande tid och t är hastigheten man håller. Om t=0 eller T s
# så kommer man ingen vart. I exempel 1 om tex har t=2 så s=(7-2)*2 = 10 vilket stämmr
# med beskrivningen.
# rekordtiderna s ger 2gradsekv s=Tt-tt -> tt-Tt+s med lösningarna s= T/2 +-sqrt(TT/4-s)
# alla heltals t strikt mellan dessa är lösningar.

def winners(T, s):
    low = math.ceil(T/2 - np.sqrt(T*T/4 - s))
    high = math.floor(T/2 + np.sqrt(T*T/4 -s))
    if (T-low)*low == s:
        low = low + 1
    if (T-high)*high == s:
        high = high - 1
    return high-low+1, list(range(low, high+1))

ans_1 = 1
for T, s in zip(times, distances):
    n, ts = winners(T, s)
    ans_1 = ans_1*n
print(f'Ans_1: {ans_1}')


T_long = int(re.findall(r'\d+', data[0].replace(' ', ''))[0])
s_long = int(re.findall(r'\d+', data[1].replace(' ', ''))[0])

n, ts = winners(T_long, s_long)
print(f'Ans_2: {n}')


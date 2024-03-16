import sys
sys.path.append('..')
file = 'input.txt'
task = 2 # 2
with open(file) as file:
    data = [s.strip() for s in file.readlines()]


direction_map = {
    0: 'R',
    1: 'D',
    2: 'L',
    3: 'U'
}


center_x = [0.5]
center_y = [-0.5]
corner_x = []
corner_y = []
dxs = []
dys = []
old_dire = 'U'
directions = []

segments = []
shifts = []
for d in data:
    dire, length, color = d.split(' ')
    if task == 2:
        length = int(color[2:-2], 16)
        dire = int(color[-2], 16)
        dire = direction_map[dire]
    directions.append(dire)
    length = int(length)
    shifts.append(length+1)

    if dire == 'U':
        dx = 0
        dy = 1
        if old_dire == 'R':
            shift_x = -0.5
            shift_y = +0.5
        else:
            shift_x = -0.5
            shift_y = -0.5
    elif dire == 'D':
        dx = 0
        dy = -1
        if old_dire == 'R':
            shift_x = +0.5
            shift_y = +0.5
        else:
            shift_x = +0.5
            shift_y = -0.5
    elif dire == 'L':
        dx = -1
        dy = 0
        if old_dire == 'U':
            shift_x = -0.5
            shift_y = -0.5
        else:
            shift_x = +0.5
            shift_y = -0.5
    elif dire == 'R':
        dx = 1
        dy = 0
        if old_dire == 'D':
            shift_x = +0.5
            shift_y = +0.5
        else:
            shift_x = -0.5
            shift_y = 0.5
    else:
        print('FEL!')
        dx = '#'
        dy = '#'
        shift_x = '#'
        shift_y = '#'
    corner_x.append(center_x[-1] + shift_x)
    corner_y.append(center_y[-1] + shift_y)
    dxs.append(dx)
    dys.append(dy)
    center_x.append(center_x[-1] + dx*length)
    center_y.append(center_y[-1] + dy*length)
    old_dire = dire


corner_x.append(corner_x[0])
corner_y.append(corner_y[0])
for cy1, cy0, cx0, dy in zip(corner_y[1:], corner_y[:-1], corner_x[:-1], dys):
    segments.append(-(cy1-cy0)*cx0)

print(f'ans: {sum(segments)}')
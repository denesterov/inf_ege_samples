# 24201

data = []
with open('26_24201.txt', 'rt') as f:
    N = int(f.readline())
    for ln in f.readlines():
        came, lg, apoint = [int(s) for s in ln.split()]
        if lg:
            lg = 2
        elif apoint > 0:
            lg = 1
        data.append((lg, apoint, came))

data.sort()

t = 420
last_normal = 0
N = 0
for it in data:
    if t > 900:
        break
    if it[0] == 0:
        N += 1
        last_normal = t
    t += 12
print(f'{N=}, {last_normal=}')

f = open('t26-24897.txt')
f.readline()
req = [[int(s) for s in ln.split()] for ln in f.readlines()] # (id, bldg, entr)

req = sorted(req, key=lambda x: (x[1], x[2], x[0]))

streak, max_streak = 1, 1
best_bldg, best_entr = 0, 0
start_id, start_entr, min_start_id = 0, 0, 10**10

for (id0, b0, e0), (id1, b1, e1) in zip(req, req[1:]):
    if b1 == b0 and e1 == e0:
        continue
    if b1 == b0 and e1 == e0 + 1:
        streak += 1
        if streak >= max_streak:
            if start_id < min_start_id or streak > max_streak:
                min_start_id = start_id
                best_bldg, best_entr = b0, start_entr
            max_streak = streak
    else:
        streak = 1
        start_id = id1
        start_entr = e1

print(best_bldg, best_entr, max_streak, min_start_id)

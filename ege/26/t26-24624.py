F = 5
lines = [[int(s) for s in ln.split()] for ln in open('t26-24624.txt').readlines()]

scrN, tickN = lines[0]
screens = {n : (r, s) for (n, r, s) in lines[1:1 + scrN]}

occup = {(scr, row, seat) for (scr, row, seat) in lines[1 + scrN:]}

count = 0
minRow = max(r for (r, _) in screens.values())
for scr, (rows, seats) in screens.items():
    for row in range(1, rows + 1):
        for seat in range(1, seats + 1 - F + 1):
            testSet = [(scr, row, s) for s in range(seat, seat + F)] + \
                [(scr, row + 1, s) for s in range(1, seats + 1)]
            if all(not P in occup for P in testSet):
                count += 1
                minRow = min(minRow, row)

print(minRow, count)

with open('t26_20910.txt', 'rt') as f:
    N, R, S = (int(s) for s in f.readline().split())
    min_row = [R + 1] * S # номер ближайшего занятого ряда для каждого сиденья
    for line in f.readlines():
        ri, si = (int(s) for s in line.split())
        min_row[si - 1] = min(min_row[si - 1], ri)

best_row = 0
best_seat = 0
for si in range(0, S - 1):
    seat1, seat2 = min_row[si], min_row[si + 1]
    row = min(seat1, seat2) - 1
    if row > best_row:
        best_row = row
        best_seat = si + 1

print(f'Row {best_row}, seat {best_seat}')

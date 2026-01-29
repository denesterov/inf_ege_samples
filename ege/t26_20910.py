# 20910

with open('t26_20910.txt', 'rt') as f:
    N, R, S = (int(s) for s in f.readline().split())
    
    seats_min_row = [R + 1] * S # номер ближайшего занятого ряда для каждого сиденья
    for line in f.readlines():
        ri, si = (int(s) for s in line.split())
        # assert ri >= 1 and ri <= R and si >= 1 and si <= S
        seats_min_row[si - 1] = min(seats_min_row[si - 1], ri)

# ищем ближайшии к сцене сидения (там где в seats_min_row наименьший номер ряда)
best_seat_row = 0
best_seat_index = 0
for si in range(0, S - 1):
    seat1, seat2 = seats_min_row[si], seats_min_row[si + 1]
    row = min(seat1, seat2) - 1
    if row > best_seat_row:
        best_seat_row = row
        best_seat_index = si + 1

print(f'Row {best_seat_row}, seat {best_seat_index}')

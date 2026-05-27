data = [[int(s) for s in ln.split()] for ln in open('26_28945.txt').readlines()[1:]]

data = sorted(data, key=lambda row: row[0] + row[1])

curr_end, count = 0, 0
prev_end, far_end = 0, 0 # 2

for beg, dist in data:
    if beg > curr_end:
        prev_end = curr_end ## 2
        curr_end = beg + dist
        count += 1
    if beg > prev_end: ## 2
        far_end = max(far_end, beg + dist) ## 2

print(count, 10000 - curr_end, 10000 - far_end)

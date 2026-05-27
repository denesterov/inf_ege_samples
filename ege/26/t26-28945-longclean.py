data = [[int(s) for s in ln.split()] for ln in open('26_28945.txt').readlines()[1:]]

data = sorted(data, key=lambda row: row[0])

prev_end, far_end, count = 0, 0, 0

for beg, dist in data:
    end = beg + dist
    if beg < prev_end:
        if end < prev_end:
            prev_end = end
        far_end = max(far_end, end)
    else:
        prev_end = end
        far_end = end
        count += 1

print(count, 10000 - far_end)

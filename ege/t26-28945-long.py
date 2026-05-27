data = [[int(s) for s in ln.split()] for ln in open('26_28945.txt').readlines()[1:]]

data = sorted(data)

#for beg, dist in data:
#    print(f'Data: ({beg} - {beg + dist})')

prev_end = 0
prev_beg = 0 # for debug only
far_end = 0
count = 0

for beg, dist in data:
    end = beg + dist
    print(f'Src: ({beg} - {end})')
    if beg < prev_end: # overlap
        if end < prev_end: # new segment is shorter, replace previous
            print(f'Replace #{count}: ({prev_beg} - {prev_end}) -> ({beg} - {end})')
            prev_end = end
            prev_beg = beg
        far_end = max(far_end, end) # keep track of the farthest end
    else: # no overlap, just add new
        prev_end = end
        prev_beg = beg
        far_end = end
        # far_end = max(far_end, end) # keep track of the farthest end
        count += 1
        print(f'New #{count}: ({beg} - {end})')

print(count, 10000 - far_end)

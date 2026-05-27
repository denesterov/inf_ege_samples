lines = [[int(s) for s in ln.split()] for ln in open('t26-23383.txt').readlines()[1:]]
data = sorted(lines, key=lambda x: (x[1], x[0])) # (competitor, ctrl_point)

longest, longest_cp = 0, 0
for (comp0, cp0), (comp1, cp1) in zip(data, data[1:]):
    if (comp1, cp1) == (comp0, cp0):
        continue
    if (comp1, cp1) == (comp0 + 1, cp0):
        length += 1
        if length >= longest:
            if length != longest or longest_cp == 0 or cp0 < longest_cp:
                longest = length
                longest_cp = cp0
    else:
        length = 1

print(longest, longest_cp)

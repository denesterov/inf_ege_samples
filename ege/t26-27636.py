lines = open('t26-27636.txt').readlines()
S, N = [int(s) for s in lines[0].split()]
data = [int(s) for s in lines[1:]]

total, out_count, out_mass = 0, 0, 0

for m in sorted(data):
    total += m
    if total > S:
        out_count += 1
        out_mass += m

print(out_count, out_mass)

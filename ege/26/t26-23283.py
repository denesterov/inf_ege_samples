lines = open('26_23283.txt').readlines()
K = int(lines[0])
data = [[int(s) for s in ln.split()] for ln in lines[2:]]

data.sort()

worker_fin = [0] * K
count = 0
last_worker_idx = 0
for beg, end in data:
    for i in range(K):
        if beg > worker_fin[i]:
            worker_fin[i] = end
            count += 1
            last_worker_idx = i + 1
            break

print(count, last_worker_idx)

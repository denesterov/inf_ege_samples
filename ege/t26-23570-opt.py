f = open('t26-23570.txt')

N, K = (int(s) for s in f.readline().split()) # slots, models num
required_perf = [int(f.readline()) for _ in range(N)]
models_data = [[int(s) for s in f.readline().split()] for _ in range(K)] # perf, price

# без словарей, две сортировки + сдвиг O(N)
models = sorted(models_data)
moveto = 0
for i in range(len(models)):
    if models[moveto][0] != models[i][0]:
        moveto += 1
        models[moveto] = models[i]
models = sorted(models[:moveto + 1], key=lambda x: x[1])

total_cost, max_perf = 0, 0
for minperf in required_perf:
    for perf, price in models:
        if perf >= minperf:
            total_cost += price
            max_perf = max(max_perf, perf)
            break
print(total_cost, max_perf)

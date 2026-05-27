# решение в лоб; медленное, полчаса примерно
lines = open('t26-23570.txt').readlines()

N, K = (int(s) for s in lines[0].split()) # slots, models num
required_perf = [int(s) for s in lines[1 : N + 1]]
models = [[int(s) for s in ln.split()] for ln in lines[N + 1 : N + K + 1]] # perf, price

models.sort(key = lambda p: (p[1], p[0]))

total_cost = 0
max_perf = 0
for idx, minperf in enumerate(required_perf):
    best_price = None
    best_perf = 0
    for perf, price in models:
        if perf < minperf:
            continue
        if best_price is not None and price > best_price: # проскочили
            break
        best_price = price
        best_perf = max(best_perf, perf)
    total_cost += best_price
    max_perf = max(max_perf, best_perf)

    if idx % 2000 == 0: print(f'progress {idx*100//len(required_perf)}')

print(total_cost, max_perf)

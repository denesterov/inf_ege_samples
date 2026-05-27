f = open('t26-23570.txt')

N, K = (int(s) for s in f.readline().split()) # slots, models num
required_perf = [int(f.readline()) for _ in range(N)]
models_data = [[int(s) for s in f.readline().split()] for _ in range(K)] # perf, price

# ищем минимальную цену для мощностей, словари, O(N) + сортировка
models = {}
for perf, price in models_data:
    models[perf] = min(price, models.get(perf, price))
models = sorted(models.items(), key=lambda x: x[1])

S = sum(next(price for perf, price in models if perf >= minperf) for minperf in required_perf)
M = max(next(perf for perf, _ in models if perf >= minperf) for minperf in required_perf)
print(S, M)

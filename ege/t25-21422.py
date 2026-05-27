# 21422

for n in range(1_125_000, 1_125_100):
    first_div = None
    for k in range(17, n // 2 + 1, 10):
        if n % k == 0:
            first_div = k
            break
    if first_div is not None:
        print(n, first_div)

def factors(n):
    res = []
    d = 2
    while n > 1 and d * d <= n:
        if n % d == 0:
            res.append(d)
            n = n // d
        else:
            d += 1
    return res + [n]

print(factors(1), factors(2))

for n in range(8_996_452, 9_020_000):
    f = factors(n)
    if len(f) == 2 and all([str(i).count('3') == 2 for i in f]):
        print(n, max(f))

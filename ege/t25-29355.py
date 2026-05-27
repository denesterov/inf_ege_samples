for a in range(100):
    for b in range(10):
        for c in range(10):
            for d in range(10):
                s = f'89{a:02}6{b}7{c}9{d}'
                n = int(s)
                if n % 9874 == 0:
                    print(n, n // 9874)

data = [[int(s) for s in ln.split()] for ln in open('t26-25363.txt').readlines()[1:]]

arr = [(o, i, True) for i, (o, _) in enumerate(data)] + [(a, i, False) for i, (_, a) in enumerate(data)]
arr.sort()

act_num = 0
used = set()
for _, i, is_O in arr:
    if i not in used:
        used.add(i)

        if len(used) >= len(data):
            print(i + 1, act_num)
            break

        if not is_O:
            act_num += 1

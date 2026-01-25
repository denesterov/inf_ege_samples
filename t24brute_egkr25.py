# 25361

import time

NF = 76

with open('t24.txt', 'rt') as f:
    s = f.read().strip()

# ускорение в ~3 раза
for r in '2468':
    s = s.replace(r, '0')

L = len(s)
m = 1
for i in range(L):
    if s[i] == '0':
        # ВНИМАНИЕ. В разборах ошибки - нет L+1, теряем последний символ строки
        for j in range(i + m, L + 1): # + m - ускорение в 2 раза
            sub = s[i:j]
            if sub.count('F') > NF or sub.count('0') > 1: # условие ускоряет перебор минимум в 10 раз
                break
            if sub.count('F') == NF and sub.count('0') == 1:
                m = max(m, len(sub))
print(m)

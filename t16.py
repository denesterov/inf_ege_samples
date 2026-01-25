# 25355

import sys

# setrecursionlimit позволяет снять лимит рекурсии в 1000 вызовов и посчитать выражение "в лоб"
# но это решение не рекомендуется, оно работает не на всех компьютерах
# и программа просто молча выходит без ошибки
sys.setrecursionlimit(100000)

def F(n):
    if n < 19:
        return 6 * (G(n - 7) - 36)
    else:
        return F(n - 4) + 3580
    
def G(n):
    if n < 248045:
        return G(n + 9) - 4
    else:
        return n / 20 + 28

print(F(673))

# 23762

with open('DEMO_24.txt') as f:
    s = f.read()
NUM_Y = 80
NUM_2025 = 90

# s = '2025YY2025YSDF2025YOOOOOOOOOOYOOOOOOOOOO'
# NUM_Y = 3
# NUM_2025 = 2

M = 0
min_len = 4 * NUM_2025
L = len(s)
for i in range(0, L):
    # добавление max(min_len, M) в range дает столь нужное ускорение перебора
    for j in range(i + max(min_len, M), L + 1): # В разборах ошибка, нет + 1 и можно потерять последний символ строки
        sub = s[i:j]
        yn = sub.count('Y')
        if yn > NUM_Y: # Важное ускорение!
            break
        if sub.count('2025') >= NUM_2025 and yn == NUM_Y:
            M = max(M, len(sub))

print(M)

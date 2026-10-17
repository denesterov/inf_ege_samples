# 23762 	
# Текстовый файл состоит из десятичных цифр и заглавных букв латинского алфавита.
# Определите в прилагаемом файле максимальное количество идущих подряд символов,
# среди которых подстрока 2025 встречается не менее 90 раз и при этом содержится ровно 80 букв Y

# data = '2025YY2025YSDF2025YOOOOOOOOOOYOOOOOOOOOO'
# NUM_Y = 3
# NUM_2025 = 2

with open('DEMO_24.txt') as f:
    data = f.read()
NUM_Y = 80
NUM_2025 = 90

import time
t0 = time.monotonic()

begin = 0
end = 0
L = len(data)
Yn = 0

maxLen = 0
maxStr = ''
while True:
    while end < L:
        if data[end] == 'Y':
            if Yn >= NUM_Y: # останавливаемся перед следующей 'лишней' Y
                break
            Yn += 1
        end += 1
    if Yn < NUM_Y:
        break

    if end - begin > maxLen and data[begin:end].count('2025') >= NUM_2025:
        maxStr = data[begin:end]
        maxLen = end - begin
    
    while begin < end and begin < L:
        if data[begin] == 'Y':
            Yn -= 1
            begin += 1
            break
        begin += 1

print(f'Result: {maxLen}\n{maxStr}')

print(f'Elapsed: {time.monotonic() - t0:.1f}')

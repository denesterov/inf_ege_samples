# 20807

N = 0
for i in range(0, 64):
    for j in range(0, 256):
        #if i == 0 and j == 0:
        #    continue
        #if i == 63 and j == 255:
        #    continue
        # a = f'{172:08b}.{16:08b}.{192+i:08b}.{j:08b}'
        a = bin(172)[2:] + '.' + bin(16)[2:] + '.' + bin(192 + i)[2:] + '.' + bin(j)[2:]
        if a.count('1') % 5 != 0:
            print(f'{a}: {i}/{j}')
            N += 1
print('Result: ', N)

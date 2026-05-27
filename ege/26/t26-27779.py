data = [int(s) for s in open('26_27779.txt').readlines()[1:]]
data.sort(reverse=True)
last = data[0]
cnt = 1
for d in data[1:]:
    if d + 8 <= last:
        cnt += 1
        last = d
print(cnt, last)

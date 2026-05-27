data = {}
total_price = 0
total_goods = 0
with open('26_17643.txt', 'rt') as f:
    for art, price, is_avail in [[int(s) for s in line.split()] for line in f.readlines()[1:]]:
        total_price += price
        total_goods += 1

        sold, avail = data.get((art, price), (0, 0))
        if is_avail:
            avail += 1
        else:
            sold += 1
        data[(art, price)] = (sold, avail)

avg_price = total_price / total_goods

arr = [(sold, price, -avail, art) for (art, price), (sold, avail) in data.items() if price > avg_price]
arr = sorted(arr, reverse=True)

sold, price, avail, art = arr[0]

print(f'Rev: {sold * price}, Avail: {-avail}')

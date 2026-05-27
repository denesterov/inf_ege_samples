data = {}
for ln in open('t26-23383.txt', 'rt').readlines()[1:]:
    competr, cp = (int(s) for s in ln.split())
    if cp in data:
        data[cp].add(competr)
    else:
        data[cp] = {competr}

longest, longest_cp = 0, 0
for cp_idx, participants in data.items():
    compet_list = sorted(list(participants))
    length = 1
    for x, y in zip(compet_list, compet_list[1:]):
        if y == x + 1:
            length += 1
            if length >= longest:
                if length != longest or longest_cp == 0 or cp_idx < longest_cp:
                    longest = length
                    longest_cp = cp_idx
        else:
            length = 1

print(longest, longest_cp)

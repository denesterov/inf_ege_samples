# 23760
# t22.txt получается из ODS файла через Ctr+C, Ctrl+V с последующей заменой разделителей (;) на пробелы ( )

with open('t22.txt', 'rt') as f:
    lines = [[int(s) for s in ln.split()] for ln in f.readlines()]

proc = {}
for ln in lines:
    id = ln[0]
    duration = ln[1]
    deps = ln[2:]
    proc[id] = (duration, deps)

def duration(pid):
    dur, deps = proc[pid]
    if deps != [0]:
        dur += max([duration(ppidd) for ppidd in deps])
    return dur

max_duration = max(duration(pid) for pid in proc.keys())

total_under17 = sum(1 for pid in proc.keys() if duration(pid) <= 17)

print(f'{max_duration=}, {total_under17=}')

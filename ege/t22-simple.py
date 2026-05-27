# 28941 
with open('t22_28941.txt', 'rt') as f:
    proc = [[int(s) for s in ln.split()] for ln in f.readlines()] # id dur deps or 0

def duration(proc_pid):
    for pid, dur, *deps in proc: # pid=proc[0], dur=proc[1], deps=proc[2:]
        if pid == proc_pid:
            if deps != [0]:
                dur += max([duration(id) for id in deps])
            return dur
    return 0

print(max(duration(pid) for pid in [row[0] for row in proc]))

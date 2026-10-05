# 23384

rectsA = [
    (2, 6, 4, 10), # xmin, xmax, ymin, ymax
    (5, 9, 10, 14),
]

rectsB = [
    (10, 16, 15, 21),
    (10, 16, 21, 26),
    (20, 26, 9, 14),
]

def dist(p1, p2):
    return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

def centroid(points):
    mind = None
    c = None
    for pnt in points:
        d = sum(dist(pnt, p) for p in points)
        if mind is None or d < mind:
            mind = d
            c = pnt
    return c

def solve(rects, name, mode):
    clusters = [[] for _ in rects]

    with open(name, 'rt') as f:
        for x, y in [[float(s) for s in ln.split()] for ln in f.readlines()]:
            for ri, (xmin, xmax, ymin, ymax) in enumerate(rects):
                if xmin <= x <= xmax and ymin <= y <= ymax:
                    clusters[ri].append((x, y))
                    break
            else:
                print('Lost point: ', x, y)

    centers = [centroid(points) for points in clusters]

    if mode == 'A':
        print('Px:', int(10000 * sum(x for x, _ in centers)))
        print('Py:', int(10000 * sum(y for _, y in centers)))
    elif mode == 'B':
        print('Q1:', int(10000 * min(dist(c, (0.0, 0.0)) for c in centers)))
        print('Q2:', int(10000 * max(dist(c, (0.0, 0.0)) for c in centers)))

solve(rectsA, '27_A_23384.txt', 'A')
solve(rectsB, '27_B_23384.txt', 'B')

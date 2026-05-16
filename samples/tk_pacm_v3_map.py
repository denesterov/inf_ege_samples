
nodes = {
    'BL': (100, 700),
    'TL': (100, 100),
    'TR': (1100, 100),
    'BR': (1100, 700),
    'TC': (600, 100),
    'BC': (600, 700),

    'M1C': (600, 300),
    'M1L': (100, 300),
    'M1R': (1100, 300),
    'M1RR': (950, 300),

    'M2CC': (450, 500),
    'M2C': (600, 500),
    'M2L': (100, 500),
    'M2R': (1100, 500),
}

edges = [
    ('TL', 'TC'),
    ('TC', 'TR'),
    ('TC', 'M1C'),
    ('BC', 'BL'),
    ('BC', 'BR'),

    ('TL', 'M1L'),
    ('M1L', 'M1C'),
    ('M1R', 'TR'),
    ('M1C', 'M1RR'),

    ('M2L', 'BL'),
    ('M2C', 'BC'),
    ('M2R', 'BR'),
    ('M2L', 'M2CC'),
    ('M2R', 'M2C'),

    ('M1L', 'M2L'),
    ('M1R', 'M2R'),
    ('M1C', 'M2C'),
]


def get_nodes(edge_idx:int):
    n1, n2 = edges[edge_idx]
    return nodes[n1], nodes[n2], n1, n2


def get_links(node_id):
    inc = [(idx, +1) for idx, (n1, _) in enumerate(edges) if n1 == node_id]
    out = [(idx, -1) for idx, (_, n2) in enumerate(edges) if n2 == node_id]
    return inc + out


def debug_draw(tk_canvas):
    for idx, (n1, n2) in enumerate(edges):
        p1, p2 = nodes[n1], nodes[n2]
        tk_canvas.create_line(*p1, *p2, fill='blue')
        tk_canvas.create_text((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2, fill='red', text=f'{n1}-{n2}({idx})')
    for name, (x, y) in nodes.items():
        tk_canvas.create_text(x, y, fill='red', text=name)

# 20907

def victory(x, y):
    return x + y >= 81

#должен выиграть тот, кто делает последний ход
def move(x, y, moves_left):
    new_states = [
        (x + 1, y),
        (x, y + 1),
        (x * 2, y),
        (x, y * 2)
    ]

    if moves_left % 2 == 1:
        # это ход игрока, который должен выиграть
        if any(victory(*st) for st in new_states):
            return True
        if moves_left > 1:
            if any(move(*st, moves_left - 1) for st in new_states):
                return True
        return False
    else:
        # ход игрока, который должен проиграть
        if any(victory(*st) for st in new_states):
            return False
        return all(move(*st, moves_left - 1) for st in new_states)



# 19 + replace `all` with `any` in line 26
for S in range(1, 73):
    if move(7, S, 3) and not move(7, S, 1):
        print('19. S: ', S)

# 20:
for S in range(1, 73):
    if move(7, S, 3) and not move(7, S, 1):
        print('20. S: ', S)

# 21:
for S in range(1, 73):
    if move(7, S, 4) and not move(7, S, 2):
        print('21. S: ', S)

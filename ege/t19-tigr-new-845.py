# 845

def victory(x):
    return x >= 36 and not overflow(x)

def overflow(x):
    return x >= 60

#должен выиграть тот, кто делает последний ход
def move(x, moves_left, anyMovement = False):
    new_states = [
        x + 1,
        x * 2,
        x * 3,
    ]

    if moves_left % 2 == 1:
        # это ход игрока, который должен выиграть
        if any(victory(st) for st in new_states):
            return True
        if moves_left > 1:
            if any(move(st, moves_left - 1, anyMovement) for st in new_states if not overflow(st)):
                return True
        return False
    else:
        # ход игрока, который должен проиграть
        if any(victory(st) for st in new_states):
            return False
        # соперник должен выиграть: all - после любого хода противника; any - после хотя бы одного хода
        quantifier = any if anyMovement else all
        return quantifier(move(st, moves_left - 1, anyMovement) for st in new_states if not overflow(st))



# 19
for S in range(1, 36):
    if move(S, 2) and not move(S, 1):
        print('19. S: ', S)

print('-----')

# 20
for S in range(1, 36):
    if move(S, 3) and not move(S, 1):
        print('20. S: ', S)

print('-----')

# 21:
for S in range(1, 36):
    if move(S, 4) and not move(S, 2):
        print('21. S: ', S)

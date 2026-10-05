#alph = sorted('АКЦЕНТ')
#n = 1
#q = 100000
#for a1 in alph:
#    for a2 in alph:
#        for a3 in sorted('АКЦЕНТ'):
#            for a4 in sorted('АКЦЕНТ'):
#                for a5 in sorted('АКЦЕНТ'):
#                    word = a1 + a2 + a3 + a4 + a5
#                    if n % 2 == 0 and a1 not in 'АЕК' and word.count('Т') >= 1:
#                        q = min(q, n)
#                        break
#                    n += 1
#print(q)


import itertools
n = 1
for w in itertools.product('АЕКНТЦ', repeat=5):
    ww = ''.join(w)
    if n % 2 == 0 and ww[0] not in 'АЕК' and ww.count('Т') >= 1:
        print(n)
        break
    n += 1

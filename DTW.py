import numpy as np
from math import sqrt

def d(a, b):
    return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def tableau_cout_min(x, y):
    M = len(x)
    N = len(y)
    tab = np.zeros((M, N))

    tab[0, 0] = d(x[0], y[0])

    for j in range(1, N):
        tab[0, j] = d(x[0], y[j]) + tab[0, j - 1]

    for i in range(1, M):
        tab[i, 0] = d(x[i], y[0]) + tab[i - 1, 0]

    for i in range(1, M):
        for j in range(1, N):
            tab[i, j] = d(x[i], y[j]) + min(
                tab[i - 1, j],
                tab[i, j - 1],
                tab[i - 1, j - 1],
            )
    return tab


def cout_min(x, y):
    return tableau_cout_min(x, y)[len(x) - 1, len(y) - 1]


def alignement(x, y):
    i = len(x) - 1
    j = len(y) - 1
    if i == 0 and j != 0:
        return alignement(x, y[:-1]) + [(i, j)]

    if j == 0 and i != 0:
        return alignement(x[:-1], y) + [(i, j)]

    if j == 0 and i == 0:
        return [(i, j)]

    else:
        c1 = cout_min(x, y[:-1])
        c2 = cout_min(x[:-1], y)
        c3 = cout_min(x[:-1], y[:-1])

        if min(c1, c2, c3) == c1:
            return alignement(x, y[:-1]) + [(i, j)]

        elif min(c1, c2, c3) == c2:
            return alignement(x[:-1], y) + [(i, j)]

        elif min(c1, c2, c3) == c3:
            return alignement(x[:-1], y[:-1]) + [(i, j)]

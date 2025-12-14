import numpy as np
from math import sqrt


def d(a, b):
    """ Calcule la distance euclidienne entre deux points du plan.

    Args:
        a (tuple | list | ndarray): [x, y] coordonnées du premier point
        b (tuple | list | ndarray): [x, y] coordonnées du second point

    Returns:
        float: distance euclidienne entre les points a et b
    """
    return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def tableau_cout_min(x, y):
    """ Construit le tableau des coûts cumulés minimaux entre deux suites de points.

    Cette fonction calcule une matrice où chaque coefficient correspond au coût
    minimal cumulé pour associer les points de x aux points de y, en utilisant
    une distance euclidienne et des transitions locales (horizontal, vertical,
    diagonale).

    Args:
        x (list | ndarray): [ (x_i, y_i) ] suite de points du premier contour
        y (list | ndarray): [ (x_j, y_j) ] suite de points du second contour

    Returns:
        ndarray: matrice des coûts cumulés minimaux de taille (len(x), len(y))
    """
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
    """ Calcule le coût total minimal d'association entre deux suites de points.

    Cette fonction extrait le coût cumulé minimal final obtenu à partir du
    tableau des coûts cumulés, correspondant à l'association complète des
    points de x avec ceux de y.

    Args:
        x (list | ndarray): [ (x_i, y_i) ] suite de points du premier contour
        y (list | ndarray): [ (x_j, y_j) ] suite de points du second contour

    Returns:
        float: coût total minimal d'association entre x et y
    """
    return tableau_cout_min(x, y)[len(x) - 1, len(y) - 1]


def alignement(x, y):
    """ Détermine un alignement optimal entre deux suites de points.

    Cette fonction reconstruit récursivement un chemin d'alignement optimal
    entre les points de x et de y, en s'appuyant sur les coûts cumulés minimaux.
    L'alignement est donné sous la forme d'une liste de couples d'indices
    correspondant aux associations entre les deux suites.

    Args:
        x (list | ndarray): [ (x_i, y_i) ] suite de points du premier contour
        y (list | ndarray): [ (x_j, y_j) ] suite de points du second contour

    Returns:
        list[tuple]: liste ordonnée de couples (i, j) représentant l'alignement
                     optimal entre x et y
    """
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

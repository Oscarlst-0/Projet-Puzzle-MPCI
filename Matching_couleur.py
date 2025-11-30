import numpy as np
from math import sqrt

"""
DTW pareil qu'Oscar
"""


# def d(a, b):
#     return abs(a - b)


# def d(a, b):
#     return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


def d(a, b):
    return sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


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
        # perso j'aurais pas fais comme ça, j'aurais utiliser le tableau direct au lieu de le recalculer à chaque fois
        c1 = cout_min(x, y[:-1])
        c2 = cout_min(x[:-1], y)
        c3 = cout_min(x[:-1], y[:-1])

        if min(c1, c2, c3) == c1:
            return alignement(x, y[:-1]) + [(i, j)]

        elif min(c1, c2, c3) == c2:
            return alignement(x[:-1], y) + [(i, j)]

        elif min(c1, c2, c3) == c3:
            return alignement(x[:-1], y[:-1]) + [(i, j)]


def alignement_v2(x, y):
    tab = tableau_cout_min(x, y)
    align = []
    i_cur = len(x) - 1
    j_cur = len(y) - 1

    while i_cur != 0 or j_cur != 0:
        align.append((i_cur, j_cur))
        if i_cur == 0:
            j_cur -= 1
        elif j_cur == 0:
            i_cur -= 1
        else:
            if (
                tab[i_cur - 1][j_cur - 1] <= tab[i_cur][j_cur - 1]
                and tab[i_cur - 1][j_cur - 1] <= tab[i_cur - 1][j_cur]
            ):
                i_cur -= 1
                j_cur -= 1
            elif (
                tab[i_cur][j_cur - 1] <= tab[i_cur - 1][j_cur - 1]
                and tab[i_cur][j_cur - 1] <= tab[i_cur - 1][j_cur]
            ):
                j_cur -= 1
            elif (
                tab[i_cur - 1][j_cur] <= tab[i_cur - 1][j_cur - 1]
                and tab[i_cur - 1][j_cur] <= tab[i_cur][j_cur - 1]
            ):
                i_cur -= 1

    align.append((0, 0))
    align.reverse()
    return align


"""
Matching couleur
"""


def get_n_pixels_int(point, rayon, image, masque, d):
    """
    Le but de la fonction est de prendre en entrée un point d'un contour d'une pièce,
    et de renvoyer la liste de tout les pixels qui sont dans la pièce et qui sont à une distance
    inférieure à rayon.
    """
    # Idée : prendre la liste des points à une distance <= rayon du point et ne prendre que les points
    # qui sont aussi des 1 (ou 0) dans le masque de l'image.
    voisins = []
    for pixel in image:
        if d(point, pixel) <= rayon and masque[point] == 1:
            voisins.append(pixel)
    return voisins


def moyenne_couleur(liste_de_points, image):
    """
    Le but de cette fonction est d'à partir d'une liste de point, calculer la moyenne
    des couleurs de cette liste et renvoyer un tuple (R, V, B).
    """
    l_rouge = [image[point[0]][point[1]][0] for point in liste_de_points]
    l_vert = [image[point[0]][point[1]][1] for point in liste_de_points]
    l_bleu = [image[point[0]][point[1]][2] for point in liste_de_points]
    rouge = sum(l_rouge) / len(l_rouge)
    vert = sum(l_vert) / len(l_vert)
    bleu = sum(l_bleu) / len(l_bleu)
    return rouge, vert, bleu


def extraire_couleurs_contour(pièce, image):
    """
    Le but de cette fonction est de prendre un contour (np array Nx2) d'une pièce
    et renvoyer un tableau Nx3 avec pour chaque point du contour la moyenne des couleur autour de ce point (rayon à définir)
    sous la forme R, G, B.
    """
    contour = pièce["contour"]
    tableau = np.zeros(len(contour), 3)
    for i in range(len(contour)):
        point = contour[i]
        voisins = get_n_pixels_int(point, "à définir", image)
        R, V, B = moyenne_couleur(voisins, image)
        tableau[i][0] = R
        tableau[i][1] = V
        tableau[i][2] = B
    return tableau


# je sais pas, pas convaincu :
def matching_bord_couleur(bord, candidats_bords):
    val_min = cout_min(bord, candidats_bords[0])
    i_mini = 0
    for i in range(1, len(candidats_bords)):
        cout = cout_min(bord, candidats_bords[i])
        if cout < val_min:
            val_min = cout
            i_mini = i
    return i_mini, val_min
